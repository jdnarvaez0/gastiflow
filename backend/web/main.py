import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, Request, Form, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from services.database_service import DatabaseService
from services.auth_service import (
    verify_password, get_password_hash, create_access_token, create_refresh_token,
    decode_token, is_trial_exceeded, get_remaining_trial, FREE_TRIAL_INTERACTIONS,
    encode_verification_token, decode_verification_token, REFRESH_TOKEN_EXPIRE_DAYS
)
from services.email_service import EmailService
from services.security_service import (
    get_client_ip, get_user_agent, log_login_attempt, log_registration,
    log_token_refresh, log_logout, log_email_change, log_unauthorized_access,
    log_rate_limit_exceeded
)
from models.expense import ExpenseSchema, Category, TransactionType
from models.user import UserCreate, UserLogin, UserUpdate, UserResponse, Token, RefreshTokenRequest, RefreshTokenResponse

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Gastiflow Web")

# Configure rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Mount static files
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# Create uploads directory for profile pictures
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "uploads", "profile_pictures")
os.makedirs(UPLOADS_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "uploads")), name="uploads")

# Templates
templates = Jinja2Templates(directory="web/templates")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login", auto_error=False)

# Database Service Dependency
def get_db_service():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        # Fallback for local development if not in env
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "postgres")
        db = os.getenv("POSTGRES_DB", "gastiflow")
        port = os.getenv("POSTGRES_PORT", "5432")
        host = os.getenv("POSTGRES_HOST", "localhost")
        db_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    
    return DatabaseService(db_url)

# Auth dependency - gets current user from token
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: DatabaseService = Depends(get_db_service)
):
    if not token:
        return None
    
    payload = decode_token(token)
    if not payload:
        return None
    
    username = payload.get("sub")
    if not username:
        return None
    
    user = db.get_user_by_username(username)
    return user

# Auth dependency - requires authenticated user
async def require_auth(
    token: str = Depends(oauth2_scheme),
    db: DatabaseService = Depends(get_db_service)
):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: DatabaseService = Depends(get_db_service)):
    # Get current date
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    # Fetch data
    monthly_stats = db.get_monthly_stats(current_year, current_month)
    category_stats = db.get_category_stats(current_year, current_month)
    history_stats = db.get_six_month_history()
    recent_expenses = db.get_all_expenses(limit=5) # Reduced to 5 for the "Recent" table
    
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "stats": monthly_stats, 
            "categories": category_stats,
            "history": history_stats,
            "expenses": recent_expenses,
            "current_date": now
        }
    )

@app.get("/add", response_class=HTMLResponse)
def add_expense_form(request: Request):
    return templates.TemplateResponse("add_expense.html", {"request": request})

@app.post("/add")
def add_expense(
    amount: float = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    transaction_type: str = Form(...),
    date: str = Form(...),
    db: DatabaseService = Depends(get_db_service)
):
    user_id = "web_user"
    
    try:
        # Parse date
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
        
        # Create schema
        expense_data = ExpenseSchema(
            amount=amount,
            description=description,
            category=category, # Pydantic will validate against Enum
            transaction_type=transaction_type,
            date=parsed_date
        )
        
        db.create_expense(user_id, expense_data)
        
        return RedirectResponse(url="/", status_code=303)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# --- API Endpoints for Nuxt Frontend ---

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel

# Get environment configuration
environment = os.getenv("ENVIRONMENT", "development")
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Configure allowed origins
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Add production frontend
if "gastiflow.vercel.app" not in allowed_origins:
    allowed_origins.append("https://gastiflow.vercel.app")

# Add configured frontend URL if different
if frontend_url not in allowed_origins:
    allowed_origins.append(frontend_url)

# Only add ngrok in development
if environment == "development":
    ngrok_url = os.getenv("NGROK_URL")
    if ngrok_url and ngrok_url not in allowed_origins:
        allowed_origins.append(ngrok_url)

# Add CORS middleware with strict configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "ngrok-skip-browser-warning"],
)

# Add HTTPS redirect in production
if environment == "production":
    app.add_middleware(HTTPSRedirectMiddleware)

# Add trusted host middleware in production
if environment == "production":
    allowed_hosts_str = os.getenv("ALLOWED_HOSTS", "")
    if allowed_hosts_str:
        allowed_hosts = [host.strip() for host in allowed_hosts_str.split(",")]
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)


# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    if environment == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# ==================== AUTH ENDPOINTS ====================

@app.post("/api/register", response_model=UserResponse)
@limiter.limit("3/hour")
def register(request: Request, user_data: UserCreate, db: DatabaseService = Depends(get_db_service)):
    """Register a new user"""
    # Get client info for logging
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    # Check if username already exists
    existing_user = db.get_user_by_username(user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    if user_data.email:
        existing_email = db.get_user_by_email(user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Hash password and create user
    hashed_password = get_password_hash(user_data.password)
    user = db.create_user(
        username=user_data.username,
        hashed_password=hashed_password,
        email=user_data.email,
        telegram_id=user_data.telegram_id
    )
    
    # Log registration
    log_registration(user.username, user.email, client_ip, user_agent)
    
    # Send verification email if email provided
    if user.email:
        token = encode_verification_token(user.email)
        db.set_email_verification_token(user.id, token)
        EmailService.send_verification_email(user.email, token, user.username)
    
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        telegram_id=user.telegram_id,
        has_gemini_key=bool(user.gemini_api_key),
        interaction_count=user.interaction_count or 0,
        is_active=user.is_active,
        email_verified=user.email_verified,
        full_name=user.full_name,
        profile_picture_url=user.profile_picture_url,
        preferred_currency=user.preferred_currency or "ARS",
        timezone=user.timezone or "America/Bogota",
        language=user.language or "es"
    )


# Add global exception handler for validation errors
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom handler for validation errors to prevent exposing sensitive data
    """
    # Sanitize error messages - never expose password or sensitive fields
    sanitized_errors = []
    sensitive_fields = {'password', 'hashed_password', 'api_key', 'token', 'secret'}
    
    for error in exc.errors():
        error_dict = error.copy()
        
        # Check if error is related to sensitive field
        if 'loc' in error_dict:
            field_path = error_dict['loc']
            # Check if any part of the location path contains sensitive field names
            is_sensitive = any(
                any(sensitive in str(loc).lower() for sensitive in sensitive_fields)
                for loc in field_path
            )
            
            if is_sensitive:
                # Sanitize the error message for sensitive fields
                # We want to keep the specific error message (e.g., "must contain at least one digit")
                # but remove the raw value if it appears. 
                # Pydantic "value_error" often comes as "Value error, <reason>"
                msg = error_dict.get('msg', '')
                if msg.startswith('Value error, '):
                    error_dict['msg'] = msg.replace('Value error, ', '')
                elif msg == 'Value error':
                    # If it's just "Value error", try to find a better message or leave it
                    pass
                
                # Remove the 'ctx' which might contain the actual value
                if 'ctx' in error_dict:
                    del error_dict['ctx']
                # Remove 'input' which contains the submitted value
                if 'input' in error_dict:
                    error_dict['input'] = '***'
        
        sanitized_errors.append(error_dict)
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": sanitized_errors}
    )


@app.post("/api/login", response_model=RefreshTokenResponse)
@limiter.limit("5/minute")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: DatabaseService = Depends(get_db_service)):
    """Login and get access token + refresh token"""
    # Get client info for logging
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    user = db.get_user_by_username(form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        # Log failed attempt
        log_login_attempt(form_data.username, False, client_ip, user_agent)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Log successful login
    log_login_attempt(user.username, True, client_ip, user_agent)
    
    # Create access token (1 hour)
    access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
    
    # Create refresh token (7 days)
    refresh_token = create_refresh_token(data={"sub": user.username, "user_id": user.id})
    
    # Store refresh token in database
    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    db.create_refresh_token(user.id, refresh_token, expires_at)
    
    return RefreshTokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

@app.get("/api/me", response_model=UserResponse)
def get_me(user = Depends(require_auth)):
    """Get current user info"""
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        telegram_id=user.telegram_id,
        has_gemini_key=bool(user.gemini_api_key),
        interaction_count=user.interaction_count or 0,
        is_active=user.is_active,
        email_verified=user.email_verified,
        full_name=user.full_name,
        profile_picture_url=user.profile_picture_url,
        preferred_currency=user.preferred_currency or "ARS",
        timezone=user.timezone or "America/Bogota",
        language=user.language or "es"
    )


@app.post("/api/refresh", response_model=RefreshTokenResponse)
@limiter.limit("10/minute")
def refresh_token(request: Request, token_request: RefreshTokenRequest, db: DatabaseService = Depends(get_db_service)):
    """Refresh access token using refresh token"""
    # Get client info for logging
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    # Decode refresh token
    payload = decode_token(token_request.refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify refresh token exists in database and is not revoked
    db_token = db.get_refresh_token(token_request.refresh_token)
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found or revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user
    username = payload.get("sub")
    user = db.get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Log token refresh
    log_token_refresh(user.username, client_ip, user_agent)
    
    # Revoke old refresh token
    db.revoke_refresh_token(token_request.refresh_token)
    
    # Create new access token
    new_access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
    
    # Create new refresh token
    new_refresh_token = create_refresh_token(data={"sub": user.username, "user_id": user.id})
    
    # Store new refresh token
    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    db.create_refresh_token(user.id, new_refresh_token, expires_at)
    
    return RefreshTokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )


@app.post("/api/logout")
@limiter.limit("10/minute")
def logout(request: Request, user = Depends(require_auth), db: DatabaseService = Depends(get_db_service)):
    """Logout user and revoke all refresh tokens"""
    # Get client info for logging
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    # Revoke all user's refresh tokens
    db.revoke_all_user_tokens(user.id)
    
    # Log logout
    log_logout(user.username, client_ip, user_agent)
    
    return {"message": "Successfully logged out from all devices"}


@app.put("/api/settings", response_model=UserResponse)
@limiter.limit("10/minute")
def update_settings(
    request: Request,
    settings: UserUpdate,
    user = Depends(require_auth),
    db: DatabaseService = Depends(get_db_service)
):
    """Update user settings (email, gemini_api_key, telegram_id)"""
    # Get client info for logging
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    # Handle email change separately if provided
    if settings.email and settings.email != user.email:
        # Check if new email already exists
        existing_email = db.get_user_by_email(settings.email)
        if existing_email and existing_email.id != user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        
        # Send notification to old email
        if user.email:
            EmailService.send_email_change_notification(user.email, user.username)
        
        # Log email change
        log_email_change(user.username, user.email, settings.email, client_ip, user_agent)
        
        # Update email and send verification
        updated_user = db.update_user_email(user.id, settings.email)
        if updated_user:
            token = encode_verification_token(settings.email)
            db.set_email_verification_token(user.id, token)
            EmailService.send_verification_email(settings.email, token, user.username)
    else:
        # Check if telegram_id is being updated and if it's already in use
        if settings.telegram_id and settings.telegram_id != user.telegram_id:
            existing_telegram = db.get_user_by_telegram_id(settings.telegram_id)
            if existing_telegram and existing_telegram.id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Telegram ID already linked to another account ({existing_telegram.username})"
                )
        
        # Update other settings
        updated_user = db.update_user(
            user_id=user.id,
            gemini_api_key=settings.gemini_api_key,
            telegram_id=settings.telegram_id,
            full_name=settings.full_name,
            preferred_currency=settings.preferred_currency,
            timezone=settings.timezone,
            language=settings.language
        )
    
    if not updated_user:
        raise HTTPException(status_code=500, detail="Failed to update settings")
    
    return UserResponse(
        id=updated_user.id,
        username=updated_user.username,
        email=updated_user.email,
        telegram_id=updated_user.telegram_id,
        has_gemini_key=bool(updated_user.gemini_api_key),
        interaction_count=updated_user.interaction_count or 0,
        is_active=updated_user.is_active,
        email_verified=updated_user.email_verified,
        full_name=updated_user.full_name,
        profile_picture_url=updated_user.profile_picture_url,
        preferred_currency=updated_user.preferred_currency or "ARS",
        timezone=updated_user.timezone or "America/Bogota",
        language=updated_user.language or "es"
    )


@app.get("/api/verify-email")
def verify_email(token: str, db: DatabaseService = Depends(get_db_service)):
    """
    Verify email address with token
    
    Query params:
        token: Verification token from email
    """
    # Decode token to get email
    email = decode_verification_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )
    
    # Get user by email
    user = db.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if already verified
    if user.email_verified:
        return {"message": "Email already verified", "already_verified": True}
    
    # Verify email
    success = db.verify_user_email(user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to verify email"
        )
    
    return {"message": "Email verified successfully", "already_verified": False}

@app.post("/api/resend-verification")
@limiter.limit("3/hour")
def resend_verification(request: Request, user = Depends(require_auth), db: DatabaseService = Depends(get_db_service)):
    """
    Resend verification email to current user
    """
    if not user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No email associated with this account"
        )
    
    if user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified"
        )
    
    # Generate new token and send email
    token = encode_verification_token(user.email)
    db.set_email_verification_token(user.id, token)
    success = EmailService.send_verification_email(user.email, token, user.username)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email"
        )
    
    return {"message": "Verification email sent"}

@app.get("/api/email-status")
def get_email_status(user = Depends(require_auth)):
    """
    Get email verification status for current user
    """
    return {
        "email": user.email,
        "email_verified": user.email_verified,
        "has_email": bool(user.email)
    }

# ==================== PROTECTED API ENDPOINTS ====================

@app.get("/api/dashboard")
def api_dashboard(
    user = Depends(get_current_user),
    db: DatabaseService = Depends(get_db_service)
):
    """Get dashboard data - works for both authenticated and unauthenticated users"""
    # Get current date
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    # If user is authenticated, get their data only
    if user:
        user_id = str(user.id)
        monthly_stats = db.get_monthly_stats(user_id, current_year, current_month)
        category_stats = db.get_category_stats(user_id, current_year, current_month)
        history_stats = db.get_six_month_history(user_id)
        recent_expenses = db.get_user_expenses(user_id, limit=5)
    else:
        # For unauthenticated users, return empty data
        monthly_stats = {"income": 0, "expenses": 0, "balance": 0, "savings": 0}
        category_stats = []
        history_stats = {"labels": [], "income": [], "expenses": []}
        recent_expenses = []
    
    return {
        "stats": monthly_stats,
        "categories": category_stats,
        "history": history_stats,
        "expenses": recent_expenses,
        "current_date": now,
        "is_authenticated": user is not None
    }

class ExpenseCreate(BaseModel):
    amount: float
    description: str
    category: str
    transaction_type: str
    date: str

@app.post("/api/expenses")
def api_add_expense(
    expense: ExpenseCreate,
    user = Depends(require_auth),
    db: DatabaseService = Depends(get_db_service)
):
    """Add expense - requires authentication"""
    user_id = str(user.id)
    
    try:
        # Parse date
        parsed_date = datetime.strptime(expense.date, "%Y-%m-%d")
        
        # Create schema
        expense_data = ExpenseSchema(
            amount=expense.amount,
            description=expense.description,
            category=expense.category,
            transaction_type=expense.transaction_type,
            date=parsed_date
        )
        
        db.create_expense(user_id, expense_data)
        
        return {"message": "Expense added successfully"}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


# ==================== PROFILE PICTURE ENDPOINTS ====================

import uuid
import shutil

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


@app.post("/api/profile-picture", response_model=UserResponse)
@limiter.limit("5/hour")
async def upload_profile_picture(
    request: Request,
    file: UploadFile = File(...),
    user = Depends(require_auth),
    db: DatabaseService = Depends(get_db_service)
):
    """Upload a profile picture for the current user"""
    
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Read file content in chunks and check size (prevents DoS)
    content = b""
    chunk_size = 1024 * 1024  # 1MB chunks
    while chunk := await file.read(chunk_size):
        content += chunk
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
            )
    
    # Delete old profile picture if exists
    if user.profile_picture_url:
        old_filename = os.path.basename(user.profile_picture_url)
        old_filepath = os.path.join(UPLOADS_DIR, old_filename)
        if os.path.exists(old_filepath):
            os.remove(old_filepath)
    
    # Generate unique filename
    unique_filename = f"{user.id}_{uuid.uuid4().hex}{file_ext}"
    filepath = os.path.join(UPLOADS_DIR, unique_filename)
    
    # Save file
    with open(filepath, "wb") as f:
        f.write(content)
    
    # Update user's profile picture URL
    profile_picture_url = f"/uploads/profile_pictures/{unique_filename}"
    updated_user = db.update_user(user_id=user.id, profile_picture_url=profile_picture_url)
    
    if not updated_user:
        # Clean up file if update failed
        os.remove(filepath)
        raise HTTPException(status_code=500, detail="Failed to update profile picture")
    
    return UserResponse(
        id=updated_user.id,
        username=updated_user.username,
        email=updated_user.email,
        telegram_id=updated_user.telegram_id,
        has_gemini_key=bool(updated_user.gemini_api_key),
        interaction_count=updated_user.interaction_count or 0,
        is_active=updated_user.is_active,
        email_verified=updated_user.email_verified,
        full_name=updated_user.full_name,
        profile_picture_url=updated_user.profile_picture_url,
        preferred_currency=updated_user.preferred_currency or "ARS",
        timezone=updated_user.timezone or "America/Bogota",
        language=updated_user.language or "es"
    )


@app.delete("/api/profile-picture", response_model=UserResponse)
def delete_profile_picture(
    user = Depends(require_auth),
    db: DatabaseService = Depends(get_db_service)
):
    """Delete the current user's profile picture"""
    
    if not user.profile_picture_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No profile picture to delete"
        )
    
    # Delete the file
    filename = os.path.basename(user.profile_picture_url)
    filepath = os.path.join(UPLOADS_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    
    # Update user to remove profile picture URL
    updated_user = db.update_user(user_id=user.id, profile_picture_url=None)
    
    # Handle None case - need to explicitly set to None
    from sqlalchemy import update
    session = db.get_session()
    try:
        from models.user import UserDB
        session.execute(
            update(UserDB).where(UserDB.id == user.id).values(profile_picture_url=None)
        )
        session.commit()
        updated_user = db.get_user_by_id(user.id)
    finally:
        session.close()
    
    if not updated_user:
        raise HTTPException(status_code=500, detail="Failed to delete profile picture")
    
    return UserResponse(
        id=updated_user.id,
        username=updated_user.username,
        email=updated_user.email,
        telegram_id=updated_user.telegram_id,
        has_gemini_key=bool(updated_user.gemini_api_key),
        interaction_count=updated_user.interaction_count or 0,
        is_active=updated_user.is_active,
        email_verified=updated_user.email_verified,
        full_name=updated_user.full_name,
        profile_picture_url=updated_user.profile_picture_url,
        preferred_currency=updated_user.preferred_currency or "ARS",
        timezone=updated_user.timezone or "America/Bogota",
        language=updated_user.language or "es"
    )


# ==================== TELEGRAM LINK CODE ENDPOINTS ====================

from models.telegram_link_code import TelegramLinkCodeResponse, TelegramLinkStatusResponse


@app.post("/api/telegram/generate-link-code", response_model=TelegramLinkCodeResponse)
@limiter.limit("5/hour")
def generate_telegram_link_code(
    request: Request,
    user = Depends(require_auth),
    db: DatabaseService = Depends(get_db_service)
):
    """
    Generate a unique code for linking Telegram account
    
    Returns a 6-character code that expires in 10 minutes
    """
    # Create link code
    link_code = db.create_link_code(user.id)
    
    if not link_code:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate link code"
        )
    
    return TelegramLinkCodeResponse(
        code=link_code.code,
        expires_at=link_code.expires_at
    )


@app.get("/api/telegram/link-status", response_model=TelegramLinkStatusResponse)
def check_telegram_link_status(
    user = Depends(require_auth),
    db: DatabaseService = Depends(get_db_service)
):
    """
    Check if user's Telegram account has been linked
    
    Used for polling to detect when link code has been used
    """
    # Refresh user data to get latest telegram_id
    updated_user = db.get_user_by_id(user.id)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return TelegramLinkStatusResponse(
        linked=bool(updated_user.telegram_id),
        telegram_id=updated_user.telegram_id
    )


"""
Authentication router for Gastiflow Web API.
Handles user registration, login, logout, token refresh, and settings.
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm

from ..dependencies import get_db_service, require_auth
from ..config import ENVIRONMENT
from services.database_service import DatabaseService
from services.auth_service import (
    verify_password, get_password_hash, create_access_token, create_refresh_token,
    decode_token, REFRESH_TOKEN_EXPIRE_DAYS, encode_verification_token
)
from services.email_service import EmailService
from services.security_service import (
    get_client_ip, get_user_agent, log_login_attempt, log_registration,
    log_token_refresh, log_logout, log_email_change
)
from models.user import UserCreate, UserUpdate, UserResponse, RefreshTokenRequest, RefreshTokenResponse

# Get limiter from app state (will be set by middleware)
from slowapi import Limiter
from slowapi.util import get_remote_address
limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/api", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
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
        telegram_id=user_data.telegram_id,
        full_name=user_data.full_name
    )
    
    # Log registration
    log_registration(user.username, user.email, client_ip, user_agent)
    
    # Send verification email if email provided
    if user.email:
        token = encode_verification_token(user.email)
        db.set_email_verification_token(user.id, token)
        success, error_msg = EmailService.send_verification_email(user.email, token, user.username)
        if not success:
            logger.warning(f"Failed to send verification email to {user.email}: {error_msg}")
            # No fallamos el registro si el email no se envía, solo logueamos
    
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


@router.post("/login", response_model=RefreshTokenResponse)
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


@router.get("/me", response_model=UserResponse)
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


@router.post("/refresh", response_model=RefreshTokenResponse)
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


@router.post("/logout")
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


@router.put("/settings", response_model=UserResponse)
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
            success, error_msg = EmailService.send_email_change_notification(user.email, user.username)
            if not success:
                logger.warning(f"Failed to send email change notification: {error_msg}")
                # Continuamos aunque falle la notificación
        
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

"""
Gastiflow Web API - Main Application Entry Point

This is the main FastAPI application that brings together all routers and middleware.
Architecture follows FastAPI best practices with modular routers.
"""
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Import configuration
from .config import ENVIRONMENT, UPLOADS_DIR

# Import middleware setup
from .middleware import setup_all_middleware

# Import all routers
from .routers import (
    health_router,
    auth_router,
    email_router,
    expenses_router,
    profile_router,
    telegram_router,
    dashboard_router,
    budgets_router,
)

# Initialize FastAPI app
app = FastAPI(
    title="Gastiflow Web",
    description="Personal finance management API",
    version="1.0.0"
)

# ==================== MIDDLEWARE SETUP ====================
# Setup all middleware (CORS, rate limiting, security headers)
limiter = setup_all_middleware(app)

# ==================== STATIC FILES ====================
# Mount static files
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# Mount uploads directory for profile pictures
app.mount("/uploads", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "uploads")), name="uploads")

# ==================== EXCEPTION HANDLERS ====================

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
                msg = error_dict.get('msg', '')
                if msg.startswith('Value error, '):
                    error_dict['msg'] = msg.replace('Value error, ', '')
                
                # Remove the 'ctx' which might contain the actual value
                if 'ctx' in error_dict:
                    del error_dict['ctx']
                # Remove 'input' which contains the submitted value
                if 'input' in error_dict:
                    error_dict['input'] = '***'
        
        sanitized_errors.append(error_dict)
    
    return JSONResponse(
        status_code=422,
        content={"detail": sanitized_errors}
    )

# ==================== INCLUDE ROUTERS ====================

# Health check routes (no prefix, accessible at /health and /api/health)
app.include_router(health_router)

# Authentication routes (/api/register, /api/login, etc.)
app.include_router(auth_router)

# Email verification routes (/api/verify-email, etc.)
app.include_router(email_router)

# Expense management routes (/api/dashboard, /api/expenses)
app.include_router(expenses_router)

# Profile routes (/api/profile-picture)
app.include_router(profile_router)

# Telegram linking routes (/api/telegram/*)
app.include_router(telegram_router)

# Budget management routes (/api/budgets/*)
app.include_router(budgets_router)

# Legacy HTML dashboard routes (/, /add)
app.include_router(dashboard_router)

# ==================== STARTUP EVENT ====================

@app.on_event("startup")
async def startup_event():
    """Application startup tasks."""
    from loguru import logger
    logger.info(f"Gastiflow Web API started in {ENVIRONMENT} mode")
    logger.info(f"Uploads directory: {UPLOADS_DIR}")

"""
Email verification router for Gastiflow Web API.
Handles email verification and resend verification.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request

from ..dependencies import get_db_service, require_auth
from services.database_service import DatabaseService
from services.auth_service import decode_verification_token, encode_verification_token
from services.email_service import EmailService

from slowapi import Limiter
from slowapi.util import get_remote_address
limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/api", tags=["Email Verification"])


@router.get("/verify-email")
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


@router.post("/resend-verification")
@limiter.limit("5/minute")  # Más permisivo: 5 por minuto
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
    success, error_msg = EmailService.send_verification_email(user.email, token, user.username)
    
    if not success:
        logger.error(f"Failed to resend verification email: {error_msg}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send verification email: {error_msg}"
        )
    
    return {"message": "Verification email sent"}


@router.get("/email-status")
def get_email_status(user = Depends(require_auth)):
    """
    Get email verification status for current user
    """
    return {
        "email": user.email,
        "email_verified": user.email_verified,
        "has_email": bool(user.email)
    }

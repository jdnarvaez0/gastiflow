"""
Telegram router for Gastiflow Web API.
Handles Telegram account linking functionality.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request

from ..dependencies import get_db_service, require_auth
from services.database_service import DatabaseService
from models.telegram_link_code import TelegramLinkCodeResponse, TelegramLinkStatusResponse

from slowapi import Limiter
from slowapi.util import get_remote_address
limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/api/telegram", tags=["Telegram"])


@router.post("/link-code", response_model=TelegramLinkCodeResponse)
@limiter.limit("5/minute")
def generate_telegram_link_code(
    request: Request,
    user = Depends(require_auth),
    db: DatabaseService = Depends(get_db_service)
):
    """
    Generate a unique code for linking Telegram account
    
    Returns a 6-character code that expires in 10 minutes
    """
    # Check if user already has Telegram linked
    if user.telegram_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Telegram account already linked"
        )
    
    # Generate link code
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


@router.get("/link-status", response_model=TelegramLinkStatusResponse)
def check_telegram_link_status(
    user = Depends(require_auth),
    db: DatabaseService = Depends(get_db_service)
):
    """
    Check if user's Telegram account has been linked
    
    Used for polling to detect when link code has been used
    """
    # Refresh user data
    current_user = db.get_user_by_id(user.id)
    
    return TelegramLinkStatusResponse(
        is_linked=bool(current_user.telegram_id if current_user else False),
        telegram_id=current_user.telegram_id if current_user else None
    )

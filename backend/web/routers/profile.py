"""
Profile router for Gastiflow Web API.
Handles profile picture upload and deletion.
"""
import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File

from ..dependencies import get_db_service, require_auth
from ..config import UPLOADS_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from services.database_service import DatabaseService
from models.user import UserResponse

from slowapi import Limiter
from slowapi.util import get_remote_address
limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/api", tags=["Profile"])


@router.post("/profile-picture", response_model=UserResponse)
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


@router.delete("/profile-picture", response_model=UserResponse)
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
    
    # Update user's profile picture URL to None
    updated_user = db.update_user(user_id=user.id, profile_picture_url=None)
    
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

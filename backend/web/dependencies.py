"""
FastAPI dependencies for Gastiflow Web application.
Contains database service dependency and authentication dependencies.
"""
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from services.database_service import DatabaseService
from services.auth_service import decode_token

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login", auto_error=False)


def get_db_service() -> DatabaseService:
    """Get database service instance."""
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


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: DatabaseService = Depends(get_db_service)
):
    """
    Get current user from token (optional).
    Returns None if not authenticated.
    """
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


async def require_auth(
    token: str = Depends(oauth2_scheme),
    db: DatabaseService = Depends(get_db_service)
):
    """
    Require authenticated user.
    Raises HTTPException if not authenticated.
    """
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

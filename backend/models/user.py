"""
User model for authentication and multi-tenancy
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
import re

from models.expense import Base


# SQLAlchemy Model for users table
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    telegram_id = Column(String(100), unique=True, index=True, nullable=True)
    gemini_api_key = Column(String(255), nullable=True)  # User's own Gemini API key
    interaction_count = Column(Integer, default=0)  # For free trial tracking
    is_active = Column(Boolean, default=True)
    
    # Email verification fields
    email_verified = Column(Boolean, default=False)
    email_verification_token = Column(String(255), nullable=True)
    email_verification_sent_at = Column(DateTime, nullable=True)
    
    # Profile fields
    full_name = Column(String(200), nullable=True)
    profile_picture_url = Column(String(500), nullable=True)
    
    # User preferences
    preferred_currency = Column(String(10), default="ARS")
    timezone = Column(String(50), default="America/Bogota")
    language = Column(String(5), default="es")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"


# Pydantic schemas for API
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    password: str = Field(..., min_length=8)
    telegram_id: Optional[str] = None
    full_name: Optional[str] = Field(None, max_length=200)
    
    @validator('password')
    def validate_password_strength(cls, v):
        """Validate password meets security requirements"""
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character (!@#$%^&*(),.?":{}|<>)')
        return v


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    gemini_api_key: Optional[str] = None
    telegram_id: Optional[str] = None
    full_name: Optional[str] = None
    preferred_currency: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    telegram_id: Optional[str] = None
    has_gemini_key: bool = False
    interaction_count: int = 0
    is_active: bool = True
    email_verified: bool = False
    full_name: Optional[str] = None
    profile_picture_url: Optional[str] = None
    preferred_currency: str = "ARS"
    timezone: str = "America/Bogota"
    language: str = "es"

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None


# Refresh Token Models
class RefreshTokenDB(Base):
    """SQLAlchemy model for refresh tokens"""
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    token_hash = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    revoked = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<RefreshToken(id={self.id}, user_id={self.user_id}, revoked={self.revoked})>"


class RefreshTokenRequest(BaseModel):
    """Request model for refresh token endpoint"""
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """Response model for refresh token endpoint"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

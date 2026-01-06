"""
Telegram Link Code model for automatic account linking
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional

from models.expense import Base


class TelegramLinkCodeDB(Base):
    """SQLAlchemy model for telegram link codes"""
    __tablename__ = "telegram_link_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    code = Column(String(6), unique=True, nullable=False, index=True)
    telegram_id = Column(String(100), nullable=True)  # Filled when code is used
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<TelegramLinkCode(id={self.id}, code={self.code}, used={self.used})>"
    
    def is_expired(self) -> bool:
        """Check if the code has expired"""
        return datetime.utcnow() > self.expires_at
    
    def is_valid(self) -> bool:
        """Check if the code is valid (not used and not expired)"""
        return not self.used and not self.is_expired()


# Pydantic schemas for API
class TelegramLinkCodeCreate(BaseModel):
    """Request model for creating a link code"""
    pass  # No input needed, user is from auth


class TelegramLinkCodeResponse(BaseModel):
    """Response model for link code"""
    code: str
    expires_at: datetime
    
    class Config:
        from_attributes = True


class TelegramLinkStatusResponse(BaseModel):
    """Response model for link status check"""
    linked: bool
    telegram_id: Optional[str] = None

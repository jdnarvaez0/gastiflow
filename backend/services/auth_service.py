"""
Authentication service for JWT token management and password hashing
"""
import os
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv()

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# Free trial configuration
FREE_TRIAL_INTERACTIONS = 5


def is_trial_exceeded(interaction_count: int) -> bool:
    """Check if user has exceeded free trial"""
    return interaction_count >= FREE_TRIAL_INTERACTIONS


def get_remaining_trial(interaction_count: int) -> int:
    """Get remaining free trial interactions"""
    remaining = FREE_TRIAL_INTERACTIONS - interaction_count
    return max(0, remaining)


# Email verification configuration
EMAIL_VERIFICATION_EXPIRE_HOURS = 24


def generate_verification_token() -> str:
    """Generate a secure random verification token"""
    import secrets
    return secrets.token_urlsafe(32)


def create_verification_token_data(email: str) -> dict:
    """
    Create token data for email verification
    
    Args:
        email: Email address to verify
        
    Returns:
        Dictionary with email and expiration time
    """
    expire = datetime.utcnow() + timedelta(hours=EMAIL_VERIFICATION_EXPIRE_HOURS)
    return {
        "email": email,
        "exp": expire
    }


def encode_verification_token(email: str) -> str:
    """
    Create a JWT token for email verification
    
    Args:
        email: Email address to verify
        
    Returns:
        Encoded JWT token
    """
    data = create_verification_token_data(email)
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def decode_verification_token(token: str) -> Optional[str]:
    """
    Decode and validate an email verification token
    
    Args:
        token: Verification token to decode
        
    Returns:
        Email address if token is valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        return email
    except JWTError:
        return None


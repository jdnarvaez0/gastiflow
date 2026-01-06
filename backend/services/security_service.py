"""
Security service for logging security events and monitoring suspicious activities
"""
import logging
from datetime import datetime
from typing import Optional
from fastapi import Request

# Configure security logger
security_logger = logging.getLogger("security")
security_logger.setLevel(logging.INFO)

# Create handler if not already configured
if not security_logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '[%(asctime)s] [SECURITY] %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    security_logger.addHandler(handler)


def get_client_ip(request: Request) -> str:
    """
    Extract client IP address from request, considering proxies
    """
    # Check for X-Forwarded-For header (proxy/load balancer)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # Take the first IP in the chain
        return forwarded_for.split(",")[0].strip()
    
    # Check for X-Real-IP header
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Fallback to direct client
    return request.client.host if request.client else "unknown"


def get_user_agent(request: Request) -> str:
    """
    Extract user agent from request
    """
    return request.headers.get("User-Agent", "unknown")


def log_login_attempt(username: str, success: bool, ip: str, user_agent: str = "unknown"):
    """
    Log login attempt (successful or failed)
    """
    if success:
        security_logger.info(
            f"Successful login | User: {username} | IP: {ip} | UserAgent: {user_agent}"
        )
    else:
        security_logger.warning(
            f"Failed login attempt | User: {username} | IP: {ip} | UserAgent: {user_agent}"
        )


def log_registration(username: str, email: Optional[str], ip: str, user_agent: str = "unknown"):
    """
    Log new user registration
    """
    security_logger.info(
        f"New registration | User: {username} | Email: {email or 'none'} | IP: {ip} | UserAgent: {user_agent}"
    )


def log_token_refresh(username: str, ip: str, user_agent: str = "unknown"):
    """
    Log token refresh event
    """
    security_logger.info(
        f"Token refresh | User: {username} | IP: {ip} | UserAgent: {user_agent}"
    )


def log_logout(username: str, ip: str, user_agent: str = "unknown"):
    """
    Log user logout
    """
    security_logger.info(
        f"User logout | User: {username} | IP: {ip} | UserAgent: {user_agent}"
    )


def log_password_change(username: str, ip: str, user_agent: str = "unknown"):
    """
    Log password change event
    """
    security_logger.warning(
        f"Password changed | User: {username} | IP: {ip} | UserAgent: {user_agent}"
    )


def log_email_change(username: str, old_email: Optional[str], new_email: str, ip: str, user_agent: str = "unknown"):
    """
    Log email change event
    """
    security_logger.warning(
        f"Email changed | User: {username} | Old: {old_email or 'none'} | New: {new_email} | IP: {ip} | UserAgent: {user_agent}"
    )


def log_unauthorized_access(path: str, ip: str, reason: str = "Invalid token"):
    """
    Log unauthorized access attempt
    """
    security_logger.warning(
        f"Unauthorized access | Path: {path} | IP: {ip} | Reason: {reason}"
    )


def log_rate_limit_exceeded(endpoint: str, ip: str):
    """
    Log rate limit exceeded event
    """
    security_logger.warning(
        f"Rate limit exceeded | Endpoint: {endpoint} | IP: {ip}"
    )


def log_suspicious_activity(activity: str, username: Optional[str], ip: str, details: str = ""):
    """
    Log suspicious activity
    """
    user_info = f"User: {username}" if username else "User: anonymous"
    security_logger.error(
        f"Suspicious activity | {activity} | {user_info} | IP: {ip} | Details: {details}"
    )

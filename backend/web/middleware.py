"""
Middleware configuration for Gastiflow Web application.
Contains CORS, security headers, and other middleware setup.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os

from .config import ENVIRONMENT, ALLOWED_ORIGINS


def setup_cors(app: FastAPI) -> None:
    """Configure CORS middleware."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "ngrok-skip-browser-warning"],
    )


def setup_rate_limiter(app: FastAPI) -> Limiter:
    """Configure rate limiter."""
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    return limiter


def setup_production_middleware(app: FastAPI) -> None:
    """Configure production-only middleware (HTTPS redirect, trusted hosts)."""
    if ENVIRONMENT == "production":
        app.add_middleware(HTTPSRedirectMiddleware)
        
        allowed_hosts_str = os.getenv("ALLOWED_HOSTS", "")
        if allowed_hosts_str:
            allowed_hosts = [host.strip() for host in allowed_hosts_str.split(",")]
            app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)


def setup_security_headers(app: FastAPI) -> None:
    """Add security headers middleware."""
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        if ENVIRONMENT == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


def setup_all_middleware(app: FastAPI) -> Limiter:
    """Setup all middleware in correct order."""
    # CORS must be first
    setup_cors(app)
    
    # Rate limiter
    limiter = setup_rate_limiter(app)
    
    # Production middleware (HTTPS, trusted hosts)
    setup_production_middleware(app)
    
    # Security headers
    setup_security_headers(app)
    
    return limiter

"""
Routers package for Gastiflow Web API.
"""
from .health import router as health_router
from .auth import router as auth_router
from .email import router as email_router
from .expenses import router as expenses_router
from .profile import router as profile_router
from .telegram import router as telegram_router
from .dashboard import router as dashboard_router

__all__ = [
    "health_router",
    "auth_router", 
    "email_router",
    "expenses_router",
    "profile_router",
    "telegram_router",
    "dashboard_router",
]

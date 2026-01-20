"""
Health check router for Gastiflow Web API.
Provides system health monitoring endpoints.
"""
from datetime import datetime
from fastapi import APIRouter, Depends
import psutil
from sqlalchemy import text

from ..dependencies import get_db_service
from ..config import ENVIRONMENT, APP_VERSION
from services.database_service import DatabaseService

router = APIRouter(tags=["Health"])


@router.get("/health")
@router.get("/api/health")
def health_check(db: DatabaseService = Depends(get_db_service)):
    """
    Health check endpoint for monitoring.
    Returns system status, database connectivity, and uptime.
    """
    # Check database connectivity
    db_status = "healthy"
    try:
        session = db.get_session()
        session.execute(text("SELECT 1"))
        session.close()
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    # Get system info
    disk = psutil.disk_usage('/')
    memory = psutil.virtual_memory()
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "checks": {
            "database": db_status,
            "disk_usage_percent": disk.percent,
            "disk_free_gb": round(disk.free / (1024**3), 2),
            "memory_usage_percent": memory.percent
        }
    }

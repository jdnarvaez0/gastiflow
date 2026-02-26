"""
Configuration module for Gastiflow Web application.
Centralizes environment variables and application settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
LANDING_URL = os.getenv("LANDING_URL", "http://localhost:3001")

# CORS configuration
ALLOWED_ORIGINS = [
    "http://localhost:3000",      # Dashboard (dev)
    "http://localhost:3001",      # Landing (dev)
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "https://gastiflow.vercel.app",
    "https://app.gastiflow.com",  # Dashboard (prod)
    "https://gastiflow.com",      # Landing (prod)
    "https://www.gastiflow.com",  # Landing www (prod)
]

# Add configured URLs if different
if FRONTEND_URL and FRONTEND_URL not in ALLOWED_ORIGINS:
    ALLOWED_ORIGINS.append(FRONTEND_URL)
if LANDING_URL and LANDING_URL not in ALLOWED_ORIGINS:
    ALLOWED_ORIGINS.append(LANDING_URL)

# Only add ngrok in development
if ENVIRONMENT == "development":
    NGROK_URL = os.getenv("NGROK_URL")
    if NGROK_URL and NGROK_URL not in ALLOWED_ORIGINS:
        ALLOWED_ORIGINS.append(NGROK_URL)

# File upload configuration
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "uploads", "profile_pictures")
os.makedirs(UPLOADS_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Application version
APP_VERSION = "1.0.0"

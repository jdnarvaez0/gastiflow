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

# CORS configuration
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://gastiflow.vercel.app",
]

# Add configured frontend URL if different
if FRONTEND_URL not in ALLOWED_ORIGINS:
    ALLOWED_ORIGINS.append(FRONTEND_URL)

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

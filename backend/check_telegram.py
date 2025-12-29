"""Check if telegram ID exists"""
from services.database_service import DatabaseService
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")
if not db_url:
    user = os.getenv("POSTGRES_USER", "fintrack_user")
    password = os.getenv("POSTGRES_PASSWORD", "hack0840")
    db = os.getenv("POSTGRES_DB", "fin")
    port = os.getenv("POSTGRES_PORT", "5432")
    host = os.getenv("POSTGRES_HOST", "localhost")
    db_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"

db = DatabaseService(db_url)

telegram_id = "765693782"

# Check if telegram ID exists
user = db.get_user_by_telegram_id(telegram_id)
print(f"Telegram ID '{telegram_id}' existe: {user is not None}")
if user:
    print(f"  - Username: {user.username}")
    print(f"  - Email: {user.email}")
    print(f"  - ID: {user.id}")
else:
    print("  - El Telegram ID está disponible para vincular")

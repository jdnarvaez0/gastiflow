"""Check if user exists"""
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

# Check username
user = db.get_user_by_username('gastiflow')
print(f"Usuario 'gastiflow' existe: {user is not None}")
if user:
    print(f"  - Email: {user.email}")
    print(f"  - Email verificado: {user.email_verified}")

# Check email
email_user = db.get_user_by_email('gastiflow22@gmail.com')
print(f"\nEmail 'gastiflow22@gmail.com' existe: {email_user is not None}")
if email_user:
    print(f"  - Username: {email_user.username}")

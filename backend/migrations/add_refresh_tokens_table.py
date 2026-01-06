"""
Database migration: Add refresh_tokens table
"""
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


class RefreshToken(Base):
    """Refresh token model for migration"""
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    token_hash = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    revoked = Column(Boolean, default=False)


def run_migration():
    """Create refresh_tokens table"""
    # Get database URL
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "postgres")
        db = os.getenv("POSTGRES_DB", "gastiflow")
        port = os.getenv("POSTGRES_PORT", "5432")
        host = os.getenv("POSTGRES_HOST", "localhost")
        db_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    
    # Create engine and table
    engine = create_engine(db_url)
    
    print("Creating refresh_tokens table...")
    Base.metadata.create_all(engine, tables=[RefreshToken.__table__])
    print("✅ Migration completed successfully!")


if __name__ == "__main__":
    run_migration()

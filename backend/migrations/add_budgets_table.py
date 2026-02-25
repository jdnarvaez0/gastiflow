"""
Database migration: Add budgets table
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


class Budget(Base):
    """Budget model for migration"""
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    alert_threshold = Column(Float, default=0.8)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def run_migration():
    """Create budgets table"""
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
    
    print("Creating budgets table...")
    Base.metadata.create_all(engine, tables=[Budget.__table__])
    print("Migration completed successfully!")


if __name__ == "__main__":
    run_migration()

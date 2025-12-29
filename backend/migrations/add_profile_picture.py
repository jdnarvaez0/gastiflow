"""
Migration script to add profile_picture_url column to users table
"""
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")
if not db_url:
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    db = os.getenv("POSTGRES_DB", "gastiflow")
    port = os.getenv("POSTGRES_PORT", "5432")
    host = os.getenv("POSTGRES_HOST", "localhost")
    db_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(db_url)

print("Agregando columna 'profile_picture_url' a la tabla 'users'...")

try:
    with engine.connect() as conn:
        # Check if column already exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'profile_picture_url'
        """))
        
        if result.fetchone():
            print("✅ La columna 'profile_picture_url' ya existe en la tabla 'users'")
        else:
            # Add the column
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN profile_picture_url VARCHAR(500)
            """))
            conn.commit()
            print("✅ Columna 'profile_picture_url' agregada exitosamente!")
            
except Exception as e:
    print(f"❌ Error: {e}")
    raise

print("\n✅ Migración completada!")

"""
Script to add email verification fields to existing users table
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# Get database URL
db_url = os.getenv("DATABASE_URL")
if not db_url:
    user = os.getenv("POSTGRES_USER", "fintrack_user")
    password = os.getenv("POSTGRES_PASSWORD", "hack0840")
    db = os.getenv("POSTGRES_DB", "fin")
    port = os.getenv("POSTGRES_PORT", "5432")
    host = os.getenv("POSTGRES_HOST", "localhost")
    db_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"

print(f"Conectando a: {db_url[:50]}...")

engine = create_engine(db_url)

# SQL to add new columns if they don't exist
alter_statements = [
    """
    ALTER TABLE users 
    ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE;
    """,
    """
    ALTER TABLE users 
    ADD COLUMN IF NOT EXISTS email_verification_token VARCHAR(255);
    """,
    """
    ALTER TABLE users 
    ADD COLUMN IF NOT EXISTS email_verification_sent_at TIMESTAMP;
    """
]

try:
    with engine.connect() as conn:
        for statement in alter_statements:
            print(f"Ejecutando: {statement.strip()[:60]}...")
            conn.execute(text(statement))
            conn.commit()
        
        print("\n✅ Base de datos actualizada exitosamente!")
        print("Los siguientes campos fueron agregados a la tabla 'users':")
        print("  - email_verified (BOOLEAN)")
        print("  - email_verification_token (VARCHAR)")
        print("  - email_verification_sent_at (TIMESTAMP)")
        
except Exception as e:
    print(f"\n❌ Error actualizando base de datos: {e}")
    raise

print("\n✨ Ahora puedes reiniciar la aplicación.")

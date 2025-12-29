"""
Delete temporary telegram user to allow linking
"""
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

from sqlalchemy import create_engine, text

engine = create_engine(db_url)

telegram_id = "765693782"

print(f"Buscando usuario temporal con Telegram ID: {telegram_id}...")

try:
    with engine.connect() as conn:
        # First, check if user exists
        result = conn.execute(
            text("SELECT id, username, email FROM users WHERE telegram_id = :tid"),
            {"tid": telegram_id}
        )
        user = result.fetchone()
        
        if user:
            print(f"\nUsuario encontrado:")
            print(f"  - ID: {user[0]}")
            print(f"  - Username: {user[1]}")
            print(f"  - Email: {user[2]}")
            
            # Check if it's a temporary user (starts with telegram_)
            if user[1].startswith("telegram_"):
                print(f"\n✅ Es un usuario temporal. Eliminando...")
                
                # Delete the user
                conn.execute(
                    text("DELETE FROM users WHERE id = :uid"),
                    {"uid": user[0]}
                )
                conn.commit()
                
                print(f"✅ Usuario temporal eliminado exitosamente!")
                print(f"\nAhora puedes vincular el Telegram ID {telegram_id} a tu cuenta.")
            else:
                print(f"\n⚠️ Este NO es un usuario temporal.")
                print(f"El Telegram ID está vinculado a una cuenta real: {user[1]}")
                print(f"No se puede eliminar automáticamente.")
        else:
            print(f"\n❌ No se encontró ningún usuario con Telegram ID: {telegram_id}")
            
except Exception as e:
    print(f"\n❌ Error: {e}")
    raise

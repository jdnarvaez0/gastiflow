"""
Script para ejecutar migraciones SQL
"""
import os
import sys
from dotenv import load_dotenv

# Agregar el directorio backend al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text

def run_migration():
    load_dotenv()
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ ERROR: DATABASE_URL no encontrado en .env")
        return False
    
    print(f"📍 Conectando a la base de datos...")
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Ejecutar las migraciones de preferencias
            print("🔄 Ejecutando migración de preferencias de usuario...")
            
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS preferred_currency VARCHAR(10) DEFAULT 'ARS'"))
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS timezone VARCHAR(50) DEFAULT 'America/Bogota'"))
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS language VARCHAR(5) DEFAULT 'es'"))
            
            conn.commit()
            
            print("✅ Migración completada exitosamente!")
            print("   - preferred_currency (default: ARS)")
            print("   - timezone (default: America/Bogota)")
            print("   - language (default: es)")
            return True
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    run_migration()

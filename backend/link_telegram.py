"""
Script para vincular tu Telegram ID con tu cuenta web
"""
import os
from dotenv import load_dotenv
from services.database_service import DatabaseService

load_dotenv()

# Get database URL
db_url = os.getenv("DATABASE_URL")
if not db_url:
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    db = os.getenv("POSTGRES_DB", "gastiflow")
    port = os.getenv("POSTGRES_PORT", "5432")
    host = os.getenv("POSTGRES_HOST", "localhost")
    db_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"

print(f"Conectando a: {db_url}\n")

db = DatabaseService(db_url)

# Get your web user
web_username = input("Ingresa tu nombre de usuario web (ej: testuser): ").strip()
telegram_id = input("Ingresa tu Telegram ID (ej: 765693782): ").strip()

# Update the web user with the telegram ID
user = db.get_user_by_username(web_username)

if not user:
    print(f"\n❌ Usuario '{web_username}' no encontrado.")
    exit(1)

print(f"\n✅ Usuario encontrado: {user.username} (ID: {user.id})")
print(f"   Email: {user.email}")
print(f"   Telegram ID actual: {user.telegram_id}")

# Update telegram_id
updated_user = db.update_user(user.id, telegram_id=telegram_id)

if updated_user:
    print(f"\n✅ Telegram ID actualizado exitosamente!")
    print(f"   Usuario: {updated_user.username}")
    print(f"   Telegram ID: {updated_user.telegram_id}")
    
    # Now update all expenses from telegram_id to user.id
    print(f"\n🔄 Actualizando gastos del bot...")
    
    session = db.get_session()
    try:
        from models.expense import ExpenseDB
        
        # Count expenses to update
        count = session.query(ExpenseDB).filter(ExpenseDB.user_id == telegram_id).count()
        
        if count > 0:
            # Update all expenses
            session.query(ExpenseDB).filter(ExpenseDB.user_id == telegram_id).update(
                {ExpenseDB.user_id: str(user.id)}
            )
            session.commit()
            print(f"✅ {count} gastos actualizados de user_id '{telegram_id}' a '{user.id}'")
        else:
            print(f"ℹ️  No hay gastos con user_id '{telegram_id}' para actualizar")
            
    except Exception as e:
        session.rollback()
        print(f"❌ Error actualizando gastos: {e}")
    finally:
        session.close()
    
    print("\n✅ ¡Proceso completado!")
    print("   Ahora los gastos del bot aparecerán en tu cuenta web.")
else:
    print(f"\n❌ Error actualizando usuario")

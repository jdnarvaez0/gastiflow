"""
Script para verificar los gastos en la base de datos
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

# Get all expenses
print("=" * 80)
print("ÚLTIMOS 10 GASTOS EN LA BASE DE DATOS:")
print("=" * 80)

expenses = db.get_all_expenses(limit=10)

if not expenses:
    print("No hay gastos en la base de datos.")
else:
    for exp in expenses:
        print(f"\nID: {exp.id}")
        print(f"User ID: {exp.user_id}")
        print(f"Descripción: {exp.description}")
        print(f"Monto: ${exp.amount} {exp.currency}")
        print(f"Categoría: {exp.category}")
        print(f"Tipo: {exp.transaction_type}")
        print(f"Fecha: {exp.date}")
        print(f"Creado: {exp.created_at}")
        print("-" * 80)

# Get users
print("\n" + "=" * 80)
print("USUARIOS EN LA BASE DE DATOS:")
print("=" * 80)

session = db.get_session()
try:
    from models.user import UserDB
    users = session.query(UserDB).all()
    
    if not users:
        print("No hay usuarios en la base de datos.")
    else:
        for user in users:
            print(f"\nID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Telegram ID: {user.telegram_id}")
            print(f"Has Gemini Key: {bool(user.gemini_api_key)}")
            print(f"Interaction Count: {user.interaction_count}")
            print("-" * 80)
finally:
    session.close()

"""
Script de prueba para verificar la conexión a PostgreSQL
"""

from services.database_service import DatabaseService
from models.expense import ExpenseSchema, Category, TransactionType
from dotenv import load_dotenv
from datetime import datetime
import os


def test_database():
    print("🔍 Probando conexión a la base de datos...")

    # Cargar variables de entorno
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("❌ ERROR: DATABASE_URL no encontrado en .env")
        return False

    print(f"📍 URL: {database_url[:20]}...")

    try:
        # Inicializar servicio de base de datos
        db = DatabaseService(database_url)
        print("✅ Conexión a base de datos exitosa!")

        # Crear un gasto de prueba
        print("\n🧪 Creando gasto de prueba...")
        test_expense = ExpenseSchema(
            description="Test - Compra de prueba",
            amount=100.0,
            currency="ARS",
            category=Category.SUPERMERCADO,
            transaction_type=TransactionType.EXPENSE,
            date=datetime.now(),
        )

        # Guardar en base de datos
        db_expense = db.create_expense("test_user_123", test_expense)
        print(f"✅ Gasto creado con ID: {db_expense.id}")

        # Obtener gastos del usuario de prueba
        print("\n📊 Obteniendo gastos del usuario de prueba...")
        expenses = db.get_user_expenses("test_user_123", limit=5)
        print(f"✅ Encontrados {len(expenses)} gasto(s)")

        for exp in expenses:
            print(f"   • {exp.description}: ${exp.amount} {exp.currency}")

        # Obtener estadísticas
        print("\n📈 Obteniendo estadísticas...")
        stats = db.get_user_stats("test_user_123")
        print(f"✅ Estadísticas obtenidas:")
        print(f"   • Total gastos: ${stats['total_expenses']:.2f}")
        print(f"   • Total ingresos: ${stats['total_income']:.2f}")
        print(f"   • Balance: ${stats['balance']:.2f}")
        print(f"   • Transacciones: {stats['transaction_count']}")

        print("\n✅ ¡Todas las pruebas de base de datos pasaron exitosamente!")
        return True

    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\n💡 Posibles soluciones:")
        print("   1. Verifica que PostgreSQL esté corriendo")
        print("   2. Verifica el DATABASE_URL en .env")
        print("   3. Asegúrate de que la base de datos existe")
        return False


if __name__ == "__main__":
    test_database()

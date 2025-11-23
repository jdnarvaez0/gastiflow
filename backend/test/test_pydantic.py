"""
Script de prueba para verificar que Pydantic v2 funcione correctamente
"""

from models.expense import ExpenseSchema, Category, TransactionType
from datetime import datetime


def test_pydantic_model():
    print("🔍 Probando modelo Pydantic v2...")

    try:
        # Test 1: Crear modelo con datos válidos
        print("\n✅ Test 1: Creando gasto válido...")
        expense = ExpenseSchema(
            description="Compra de prueba",
            amount=100.50,
            currency="ARS",
            category=Category.SUPERMERCADO,
            transaction_type=TransactionType.EXPENSE,
        )
        print(f"   Gasto creado: {expense.description} - ${expense.amount}")

        # Test 2: Validar desde diccionario
        print("\n✅ Test 2: Validando desde diccionario...")
        data = {
            "description": "Cena en restaurante",
            "amount": 3000,
            "currency": "ARS",
            "category": "Restaurante",
            "transaction_type": "expense",
        }
        expense2 = ExpenseSchema.model_validate(data)
        print(f"   Gasto validado: {expense2.description} - ${expense2.amount}")

        # Test 3: Formatear mensaje
        print("\n✅ Test 3: Formateando mensaje...")
        message = expense2.format_message()
        print(f"   Mensaje formateado:\n{message}")

        # Test 4: Convertir a diccionario
        print("\n✅ Test 4: Convertir a diccionario...")
        expense_dict = expense2.model_dump()
        print(f"   Diccionario: {expense_dict}")

        print("\n✅ ¡Todos los tests de Pydantic pasaron!")
        return True

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_pydantic_model()

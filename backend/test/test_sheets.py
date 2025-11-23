"""
Script de prueba para verificar la conexión a Google Sheets
"""

import sys
import os

# Agregar el directorio raíz al path para poder importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.sheets_service import SheetsService
from models.expense import ExpenseSchema, Category, TransactionType
from dotenv import load_dotenv
from datetime import datetime


def test_google_sheets():
    print("🔍 Probando conexión a Google Sheets...")

    # Cargar variables de entorno
    load_dotenv()
    credentials_file = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE")
    sheet_id = os.getenv("GOOGLE_SHEET_ID")

    if not credentials_file or not sheet_id:
        print(
            "❌ ERROR: GOOGLE_SHEETS_CREDENTIALS_FILE o GOOGLE_SHEET_ID no encontrado en .env"
        )
        return False

    # Verificar que el archivo de credenciales existe
    if not os.path.exists(credentials_file):
        print(f"❌ ERROR: Archivo de credenciales no encontrado: {credentials_file}")
        print("\n💡 Solución:")
        print("   1. Descarga el archivo credentials.json de Google Cloud Console")
        print("   2. Colócalo en la carpeta config/")
        return False

    print(f"📍 Archivo de credenciales: {credentials_file}")
    print(f"📍 Sheet ID: {sheet_id[:20]}...")

    try:
        # Inicializar servicio de Google Sheets
        print("\n🔐 Autenticando con Google...")
        sheets = SheetsService(credentials_file, sheet_id)
        print("✅ Conexión a Google Sheets exitosa!")

        # Crear un gasto de prueba
        print("\n🧪 Añadiendo gasto de prueba a Google Sheets...")
        test_expense = ExpenseSchema(
            description="Test - Compra de prueba en Sheets",
            amount=250.50,
            currency="ARS",
            category=Category.RESTAURANTE,
            transaction_type=TransactionType.EXPENSE,
            date=datetime.now(),
        )

        # Añadir a Google Sheets
        success = sheets.add_expense("test_user_456", test_expense, db_id=999)

        if success:
            print("✅ Gasto añadido correctamente a Google Sheets!")
            print("\n📋 Abre tu Google Sheet para verificar que aparezca la nueva fila")
            print(f"   URL: https://docs.google.com/spreadsheets/d/{sheet_id}")
        else:
            print("❌ Error al añadir gasto a Google Sheets")
            return False

        # Obtener resumen
        print("\n📊 Obteniendo resumen del usuario...")
        summary = sheets.get_user_summary("test_user_456")
        print(f"✅ Resumen obtenido:")
        print(f"   • Cantidad de gastos: {summary['count']}")
        print(f"   • Total: ${summary['total']:.2f}")

        # Test adicional: añadir otro gasto
        print("\n🧪 Añadiendo segundo gasto de prueba...")
        test_expense2 = ExpenseSchema(
            description="Test - Supermercado",
            amount=1500.00,
            currency="ARS",
            category=Category.SUPERMERCADO,
            transaction_type=TransactionType.EXPENSE,
            date=datetime.now(),
        )

        success2 = sheets.add_expense("test_user_789", test_expense2, db_id=1000)
        if success2:
            print("✅ Segundo gasto añadido correctamente!")

        print("\n✅ ¡Todas las pruebas de Google Sheets pasaron exitosamente!")
        print("\n📝 Nota: Revisa tu Google Sheet para ver los datos insertados")
        print(f"   URL: https://docs.google.com/spreadsheets/d/{sheet_id}")
        return True

    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\n💡 Posibles soluciones:")
        print("   1. Verifica que el archivo credentials.json esté en config/")
        print("   2. Abre el archivo credentials.json y busca 'client_email'")
        print(
            "   3. Copia ese email y compártelo en tu Google Sheet con permisos de Editor"
        )
        print(
            "   4. Verifica que Google Sheets API y Google Drive API estén habilitadas en Google Cloud"
        )
        print(
            "   5. Verifica que el GOOGLE_SHEET_ID sea correcto (está en la URL del Sheet)"
        )

        # Mostrar información adicional del error
        import traceback

        print("\n🔍 Detalle del error:")
        traceback.print_exc()

        return False


if __name__ == "__main__":
    success = test_google_sheets()
    sys.exit(0 if success else 1)

"""
Script principal para ejecutar el bot con verificaciones previas
"""

import os
import sys
from dotenv import load_dotenv
from loguru import logger
import langchain

# -------------------------------------------------------------------------
# FIX: Monkeypatch para evitar error "module 'langchain' has no attribute 'verbose'"
# Esto ocurre por incompatibilidad entre versiones de langchain y langchain-core
if not hasattr(langchain, 'verbose'):
    langchain.verbose = False

if not hasattr(langchain, 'debug'):
    langchain.debug = False
# -------------------------------------------------------------------------



def check_environment():
    """Verifica que todas las variables de entorno estén configuradas"""
    print("🔍 Verificando variables de entorno...")

    load_dotenv()

    required_vars = [
        "TELEGRAM_BOT_TOKEN",
        "GEMINI_API_KEY",
        "DATABASE_URL",
        "GOOGLE_SHEETS_CREDENTIALS_FILE",
        "GOOGLE_SHEET_ID",
    ]

    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
            print(f"   ❌ {var} - NO CONFIGURADO")
        else:
            # Mostrar solo los primeros caracteres por seguridad
            display_value = value[:20] + "..." if len(value) > 20 else value
            print(f"   ✅ {var} - {display_value}")

    if missing_vars:
        print(f"\n❌ ERROR: Faltan {len(missing_vars)} variable(s) de entorno:")
        for var in missing_vars:
            print(f"   • {var}")
        print("\n💡 Solución: Edita el archivo .env y agrega las variables faltantes")
        return False

    print("✅ Todas las variables de entorno están configuradas\n")
    return True


def check_files():
    """Verifica que todos los archivos necesarios existan"""
    print("🔍 Verificando archivos necesarios...")

    load_dotenv()
    credentials_file = os.getenv(
        "GOOGLE_SHEETS_CREDENTIALS_FILE", "config/credentials.json"
    )
    
    # Si hay credenciales por variable de entorno, no necesitamos el archivo
    credentials_b64 = os.getenv("GOOGLE_CREDENTIALS_B64")

    required_files = [
        "bot/main.py",
        "bot/handlers.py",
        "services/ai_processor.py",
        "services/database_service.py",
        "services/sheets_service.py",
        "models/expense.py",
    ]
    
    # Solo agregar archivo de credenciales si no hay variable de entorno
    if not credentials_b64:
        required_files.append(credentials_file)
    else:
        print("   ✅ Credenciales de Google (via GOOGLE_CREDENTIALS_B64)")

    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - NO ENCONTRADO")
            missing_files.append(file)

    if missing_files:
        print(f"\n❌ ERROR: Faltan {len(missing_files)} archivo(s):")
        for file in missing_files:
            print(f"   • {file}")
        return False

    print("✅ Todos los archivos necesarios están presentes\n")
    return True


def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    print("🔍 Verificando dependencias de Python...")

    required_packages = [
        "telegram",
        "google.generativeai",
        "sqlalchemy",
        "gspread",
        "langchain",
        "dotenv",
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NO INSTALADO")
            missing_packages.append(package)

    if missing_packages:
        print(f"\n❌ ERROR: Faltan {len(missing_packages)} paquete(s):")
        for package in missing_packages:
            print(f"   • {package}")
        print("\n💡 Solución: Ejecuta 'pip install -r requirements.txt'")
        return False

    print("✅ Todas las dependencias están instaladas\n")
    return True


def run_bot():
    """Ejecuta el bot después de las verificaciones"""
    print("=" * 60)
    print("🚀 INICIANDO BOT DE GASTOS")
    print("=" * 60 + "\n")

    # Verificaciones previas
    checks = [
        ("Variables de entorno", check_environment),
        ("Archivos del proyecto", check_files),
        ("Dependencias de Python", check_dependencies),
    ]

    for check_name, check_func in checks:
        if not check_func():
            print(f"\n❌ Error en: {check_name}")
            print("⚠️  Corrige los errores antes de continuar\n")
            return False

    print("=" * 60)
    print("✅ TODAS LAS VERIFICACIONES PASARON")
    print("=" * 60 + "\n")

    print("🤖 Iniciando bot de Telegram...")
    print("💡 Presiona Ctrl+C para detener el bot\n")

    try:
        # Importar y ejecutar el bot
        from bot.main import main

        main()
    except KeyboardInterrupt:
        print("\n\n👋 Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"Error fatal: {e}")
        print(f"\n❌ ERROR FATAL: {e}")
        print("\n💡 Revisa el archivo bot_logs.log para más detalles")
        return False

    return True


if __name__ == "__main__":
    success = run_bot()
    sys.exit(0 if success else 1)

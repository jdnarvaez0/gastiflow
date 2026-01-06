import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from loguru import logger
import sys

# Importar servicios
from services.ai_processor import AIProcessor
from services.database_service import DatabaseService
from services.sheets_service import SheetsService
from bot.handlers import BotHandlers

# Configurar logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO",
)
logger.add("bot_logs.log", rotation="1 week", retention="1 month", level="DEBUG")


def main():
    """
    Función principal para iniciar el bot
    """
    # Cargar variables de entorno
    load_dotenv()

    # Obtener configuración
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE")
    GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

    # Validar configuración
    if not all(
        [
            TELEGRAM_TOKEN,
            GEMINI_API_KEY,
            DATABASE_URL,
            GOOGLE_SHEETS_CREDENTIALS,
            GOOGLE_SHEET_ID,
        ]
    ):
        logger.error("Faltan variables de entorno. Revisa tu archivo .env")
        return

    logger.info("Iniciando bot de gastos...")

    try:
        # Inicializar servicios
        logger.info("Inicializando servicios...")

        ai_processor = AIProcessor(GEMINI_API_KEY)
        logger.info("✓ AI Processor inicializado")

        db_service = DatabaseService(DATABASE_URL)
        logger.info("✓ Database Service inicializado")

        sheets_service = SheetsService(GOOGLE_SHEETS_CREDENTIALS, GOOGLE_SHEET_ID)
        logger.info("✓ Sheets Service inicializado")

        # Crear handlers
        handlers = BotHandlers(ai_processor, db_service, sheets_service, GEMINI_API_KEY)

        # Crear aplicación del bot
        application = Application.builder().token(TELEGRAM_TOKEN).build()

        # Registrar comandos
        application.add_handler(CommandHandler("start", handlers.start_command))
        application.add_handler(CommandHandler("help", handlers.help_command))
        application.add_handler(CommandHandler("link", handlers.link_command))
        application.add_handler(CommandHandler("stats", handlers.stats_command))
        application.add_handler(CommandHandler("recent", handlers.recent_command))

        # Registrar handlers de mensajes
        application.add_handler(MessageHandler(filters.PHOTO, handlers.handle_photo))
        application.add_handler(MessageHandler(filters.VOICE, handlers.handle_voice))
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_text)
        )

        logger.info("✓ Handlers registrados")

        # Iniciar el bot
        logger.info("🤖 Bot iniciado. Presiona Ctrl+C para detener.")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    except KeyboardInterrupt:
        logger.info("Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"Error fatal: {e}")
        raise


if __name__ == "__main__":
    main()

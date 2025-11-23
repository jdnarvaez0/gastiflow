from telegram import Update
from telegram.ext import ContextTypes
from services.ai_processor import AIProcessor
from services.database_service import DatabaseService
from services.sheets_service import SheetsService
from loguru import logger
import os


class BotHandlers:
    def __init__(
        self,
        ai_processor: AIProcessor,
        db_service: DatabaseService,
        sheets_service: SheetsService,
    ):
        self.ai = ai_processor
        self.db = db_service
        self.sheets = sheets_service

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Comando /start - Mensaje de bienvenida
        """
        welcome_message = """👋 ¡Hola! Soy tu asistente de gastos personales.

📸 Puedes enviarme:
• Una foto de tu factura o recibo
• Un mensaje de voz describiendo tu gasto
• Un mensaje de texto con el gasto

🤖 Yo extraeré automáticamente:
• Descripción del gasto
• Monto
• Categoría
• Y lo guardaré en tu registro

📊 Comandos disponibles:
/start - Ver este mensaje
/stats - Ver tus estadísticas
/recent - Ver tus últimos gastos
/help - Ayuda

¡Empieza enviándome una foto o describiendo tu gasto!"""

        await update.message.reply_text(welcome_message)
        logger.info(f"Usuario {update.effective_user.id} inició el bot")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Comando /help - Ayuda
        """
        help_text = """❓ Ayuda - Cómo usar el bot

📸 **Enviar foto de factura:**
Simplemente envía una foto del recibo y yo extraeré la información.

🎤 **Enviar audio:**
Envía un mensaje de voz diciendo algo como:
"Gasté 500 pesos en el supermercado"

✍️ **Enviar texto:**
Escribe tu gasto:
"Cena en restaurante, 3000 pesos"

📊 **Ver estadísticas:**
/stats - Resumen de tus gastos

📋 **Ver historial:**
/recent - Últimos 10 gastos

¿Necesitas más ayuda? Escríbeme y te guiaré."""

        await update.message.reply_text(help_text)

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Comando /stats - Estadísticas del usuario
        """
        user_id = str(update.effective_user.id)

        try:
            stats = self.db.get_user_stats(user_id)

            if stats["transaction_count"] == 0:
                await update.message.reply_text(
                    "📊 Aún no tienes gastos registrados.\n"
                    "¡Envía tu primera factura o descríbeme un gasto!"
                )
                return

            stats_message = f"""📊 **Tus Estadísticas**

💸 Total Gastos: ${stats['total_expenses']:.2f}
💰 Total Ingresos: ${stats['total_income']:.2f}
📈 Balance: ${stats['balance']:.2f}
🔢 Transacciones: {stats['transaction_count']}"""

            await update.message.reply_text(stats_message, parse_mode="Markdown")

        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            await update.message.reply_text(
                "❌ Error al obtener estadísticas. Intenta de nuevo."
            )

    async def recent_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Comando /recent - Últimos gastos
        """
        user_id = str(update.effective_user.id)

        try:
            expenses = self.db.get_user_expenses(user_id, limit=10)

            if not expenses:
                await update.message.reply_text("📋 No tienes gastos registrados aún.")
                return

            message = "📋 **Tus últimos gastos:**\n\n"

            for expense in expenses:
                emoji = "💸" if expense.transaction_type == "expense" else "💰"
                message += f"{emoji} {expense.description}\n"
                message += (
                    f"   ${expense.amount} {expense.currency} - {expense.category}\n"
                )
                message += f"   {expense.date.strftime('%Y-%m-%d %H:%M')}\n\n"

            await update.message.reply_text(message, parse_mode="Markdown")

        except Exception as e:
            logger.error(f"Error obteniendo gastos recientes: {e}")
            await update.message.reply_text(
                "❌ Error al obtener gastos. Intenta de nuevo."
            )

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Maneja fotos de facturas
        """
        user_id = str(update.effective_user.id)

        await update.message.reply_text("📸 Analizando tu factura...")

        try:
            # Descargar la foto
            photo = await update.message.photo[-1].get_file()
            photo_path = f"temp_{user_id}.jpg"
            await photo.download_to_drive(photo_path)

            # Procesar con IA
            expense = self.ai.process_image(photo_path)

            # Limpiar archivo temporal
            if os.path.exists(photo_path):
                os.remove(photo_path)

            if not expense:
                await update.message.reply_text(
                    "❌ No pude extraer información de la imagen.\n"
                    "Posibles razones:\n"
                    "• Imagen muy borrosa\n"
                    "• Límite de API alcanzado (espera 1 minuto)\n\n"
                    "Intenta con otra foto más clara o descríbeme el gasto en texto."
                )
                return

            # Guardar en base de datos
            db_expense = self.db.create_expense(user_id, expense)

            # Guardar en Google Sheets
            self.sheets.add_expense(user_id, expense, db_expense.id)

            # Enviar confirmación
            await update.message.reply_text(expense.format_message())

            logger.info(f"Factura procesada para usuario {user_id}")

        except Exception as e:
            logger.error(f"Error procesando foto: {e}")
            await update.message.reply_text(
                "❌ Hubo un error procesando tu foto. Intenta de nuevo."
            )

    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Maneja mensajes de voz
        """
        user_id = str(update.effective_user.id)

        await update.message.reply_text("🎤 Escuchando tu audio...")

        try:
            # Descargar audio
            voice = await update.message.voice.get_file()
            audio_path = f"temp_{user_id}.ogg"
            await voice.download_to_drive(audio_path)

            # Transcribir audio
            text = self.ai.transcribe_audio(audio_path)

            # Limpiar archivo temporal
            if os.path.exists(audio_path):
                os.remove(audio_path)

            if not text:
                await update.message.reply_text(
                    "❌ No pude entender el audio. Intenta de nuevo."
                )
                return

            await update.message.reply_text(f'📝 Entendí: "{text}"\n\nProcesando...')

            # Procesar texto para extraer gasto
            expense = self.ai.process_audio_text(text)

            if not expense:
                await update.message.reply_text(
                    "❌ No pude extraer información del audio.\n"
                    "Intenta describir el gasto más claramente."
                )
                return

            # Guardar en base de datos
            db_expense = self.db.create_expense(user_id, expense)

            # Guardar en Google Sheets
            self.sheets.add_expense(user_id, expense, db_expense.id)

            # Enviar confirmación
            await update.message.reply_text(expense.format_message())

            logger.info(f"Audio procesado para usuario {user_id}")

        except Exception as e:
            logger.error(f"Error procesando audio: {e}")
            await update.message.reply_text(
                "❌ Hubo un error procesando tu audio. Intenta de nuevo."
            )

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Maneja mensajes de texto
        """
        user_id = str(update.effective_user.id)
        text = update.message.text

        await update.message.reply_text("💭 Procesando tu mensaje...")

        try:
            # Procesar texto
            expense = self.ai.process_audio_text(text)

            if not expense:
                await update.message.reply_text(
                    "❌ No pude entender tu mensaje.\n"
                    "Intenta describir el gasto así:\n"
                    '"Gasté 500 pesos en el supermercado"'
                )
                return

            # Guardar en base de datos
            db_expense = self.db.create_expense(user_id, expense)

            # Guardar en Google Sheets
            self.sheets.add_expense(user_id, expense, db_expense.id)

            # Enviar confirmación
            await update.message.reply_text(expense.format_message())

            logger.info(f"Texto procesado para usuario {user_id}")

        except Exception as e:
            logger.error(f"Error procesando texto: {e}")
            await update.message.reply_text(
                "❌ Hubo un error procesando tu mensaje. Intenta de nuevo."
            )

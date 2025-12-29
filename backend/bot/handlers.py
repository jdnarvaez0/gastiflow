from telegram import Update
from telegram.ext import ContextTypes
from services.ai_processor import AIProcessor
from services.database_service import DatabaseService
from services.sheets_service import SheetsService
from services.auth_service import FREE_TRIAL_INTERACTIONS, is_trial_exceeded, get_remaining_trial
from loguru import logger
import os


class BotHandlers:
    def __init__(
        self,
        ai_processor: AIProcessor,
        db_service: DatabaseService,
        sheets_service: SheetsService,
        default_gemini_key: str,
    ):
        self.default_ai = ai_processor
        self.db = db_service
        self.sheets = sheets_service
        self.default_gemini_key = default_gemini_key

    def _get_ai_processor(self, telegram_id: str) -> tuple[AIProcessor, bool]:
        """
        Get the appropriate AI processor for the user.
        Returns (ai_processor, is_registered)
        """
        user = self.db.get_user_by_telegram_id(telegram_id)
        
        if user and user.gemini_api_key:
            # User is registered and has their own API key
            return AIProcessor(user.gemini_api_key), True
        
        # Use default AI processor
        return self.default_ai, False

    def _get_user_id(self, telegram_id: str) -> str:
        """
        Get the correct user_id to use for saving expenses.
        If user is registered and has telegram_id linked, use their numeric user.id
        Otherwise, use the telegram_id as string for backward compatibility
        """
        user = self.db.get_user_by_telegram_id(telegram_id)
        
        if user and user.id:
            # User is registered and linked, use their numeric ID
            return str(user.id)
        
        # User not registered or not linked, use telegram_id
        return telegram_id

    async def _check_trial_limit(self, update: Update, telegram_id: str) -> bool:
        """
        Check if user has exceeded free trial.
        Returns True if user can continue, False if blocked.
        """
        user = self.db.get_user_by_telegram_id(telegram_id)
        
        # If user is registered with their own API key, no limits
        if user and user.gemini_api_key:
            return True
        
        # Get current interaction count
        interaction_count = self.db.get_interaction_count(telegram_id)
        
        if is_trial_exceeded(interaction_count):
            await update.message.reply_text(
                f"⚠️ Has alcanzado el límite de {FREE_TRIAL_INTERACTIONS} interacciones gratuitas.\n\n"
                "Para seguir usando el bot, necesitas:\n"
                "1️⃣ Registrarte en la web de Gastiflow\n"
                "2️⃣ Obtener tu propia API Key de Google Gemini (es gratis)\n"
                "3️⃣ Configurar tu API Key en la sección de ajustes\n"
                "4️⃣ Vincular tu Telegram ID en ajustes\n\n"
                f"Tu Telegram ID es: `{telegram_id}`\n\n"
                "💡 Consejo: Puedes obtener una API Key gratis en:\n"
                "https://aistudio.google.com/app/apikey"
            )
            return False
        
        return True

    async def _increment_and_notify_trial(self, update: Update, telegram_id: str):
        """Increment trial counter and notify user of remaining trials"""
        user = self.db.get_user_by_telegram_id(telegram_id)
        
        # Don't count if user has their own API key
        if user and user.gemini_api_key:
            return
        
        new_count = self.db.increment_interaction_count(telegram_id)
        remaining = get_remaining_trial(new_count)
        
        if remaining > 0 and remaining <= 2:
            await update.message.reply_text(
                f"⏳ Te quedan {remaining} interacciones gratuitas.\n"
                "Regístrate en Gastiflow para seguir usando el bot sin límites."
            )

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Comando /start - Mensaje de bienvenida
        """
        telegram_id = str(update.effective_user.id)
        user = self.db.get_user_by_telegram_id(telegram_id)
        interaction_count = self.db.get_interaction_count(telegram_id)
        remaining = get_remaining_trial(interaction_count)
        
        if user and user.gemini_api_key:
            status_msg = "✅ Tu cuenta está vinculada y configurada."
        else:
            status_msg = f"🎁 Tienes {remaining} interacciones gratuitas restantes."
        
        welcome_message = f"""👋 ¡Hola! Soy tu asistente de gastos personales.

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

{status_msg}

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

🔗 **Vincular cuenta:**
Regístrate en la web y configura tu Telegram ID para usar tu propia API Key.

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
        telegram_id = str(update.effective_user.id)

        # Check trial limit
        if not await self._check_trial_limit(update, telegram_id):
            return

        await update.message.reply_text("📸 Analizando tu factura...")

        try:
            # Get appropriate AI processor
            ai, is_registered = self._get_ai_processor(telegram_id)
            
            # Descargar la foto
            photo = await update.message.photo[-1].get_file()
            photo_path = f"temp_{telegram_id}.jpg"
            await photo.download_to_drive(photo_path)

            # Procesar con IA
            expense = ai.process_image(photo_path)

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

            # Get correct user_id (numeric ID if registered, telegram_id if not)
            user_id = self._get_user_id(telegram_id)
            
            # Guardar en base de datos
            db_expense = self.db.create_expense(user_id, expense)

            # Guardar en Google Sheets
            self.sheets.add_expense(user_id, expense, db_expense.id)

            # Enviar confirmación
            await update.message.reply_text(expense.format_message())
            
            # Increment and notify trial
            await self._increment_and_notify_trial(update, telegram_id)

            logger.info(f"Factura procesada para usuario {telegram_id}")

        except Exception as e:
            logger.error(f"Error procesando foto: {e}")
            await update.message.reply_text(
                "❌ Hubo un error procesando tu foto. Intenta de nuevo."
            )

    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Maneja mensajes de voz
        """
        telegram_id = str(update.effective_user.id)

        # Check trial limit
        if not await self._check_trial_limit(update, telegram_id):
            return

        await update.message.reply_text("🎤 Escuchando tu audio...")

        try:
            # Get appropriate AI processor
            ai, is_registered = self._get_ai_processor(telegram_id)
            
            # Descargar audio
            voice = await update.message.voice.get_file()
            audio_path = f"temp_{telegram_id}.ogg"
            await voice.download_to_drive(audio_path)

            # Transcribir audio
            text = ai.transcribe_audio(audio_path)

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
            expense = ai.process_audio_text(text)

            if not expense:
                await update.message.reply_text(
                    "❌ No pude extraer información del audio.\n"
                    "Intenta describir el gasto más claramente."
                )
                return

            # Get correct user_id (numeric ID if registered, telegram_id if not)
            user_id = self._get_user_id(telegram_id)
            
            # Guardar en base de datos
            db_expense = self.db.create_expense(user_id, expense)

            # Guardar en Google Sheets
            self.sheets.add_expense(user_id, expense, db_expense.id)

            # Enviar confirmación
            await update.message.reply_text(expense.format_message())
            
            # Increment and notify trial
            await self._increment_and_notify_trial(update, telegram_id)

            logger.info(f"Audio procesado para usuario {telegram_id}")

        except Exception as e:
            logger.error(f"Error procesando audio: {e}")
            await update.message.reply_text(
                "❌ Hubo un error procesando tu audio. Intenta de nuevo."
            )

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Maneja mensajes de texto
        """
        telegram_id = str(update.effective_user.id)
        text = update.message.text

        # Check trial limit
        if not await self._check_trial_limit(update, telegram_id):
            return

        await update.message.reply_text("💭 Procesando tu mensaje...")

        try:
            # Get appropriate AI processor
            ai, is_registered = self._get_ai_processor(telegram_id)
            
            # Procesar texto
            expense = ai.process_audio_text(text)

            if not expense:
                await update.message.reply_text(
                    "❌ No pude entender tu mensaje.\n"
                    "Intenta describir el gasto así:\n"
                    '"Gasté 500 pesos en el supermercado"'
                )
                return

            # Get correct user_id (numeric ID if registered, telegram_id if not)
            user_id = self._get_user_id(telegram_id)
            
            # Guardar en base de datos
            db_expense = self.db.create_expense(user_id, expense)

            # Guardar en Google Sheets
            self.sheets.add_expense(user_id, expense, db_expense.id)

            # Enviar confirmación
            await update.message.reply_text(expense.format_message())
            
            # Increment and notify trial
            await self._increment_and_notify_trial(update, telegram_id)

            logger.info(f"Texto procesado para usuario {telegram_id}")

        except Exception as e:
            logger.error(f"Error procesando texto: {e}")
            await update.message.reply_text(
                "❌ Hubo un error procesando tu mensaje. Intenta de nuevo."
            )


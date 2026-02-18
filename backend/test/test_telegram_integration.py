"""
Integration tests for Telegram Bot functionality.
Tests the complete flow: linking, message processing, rate limiting.
"""
import pytest
import os
import sys
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock, AsyncMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.handlers import BotHandlers
from services.database_service import DatabaseService
from services.ai_processor import AIProcessor
from services.sheets_service import SheetsService
from services.auth_service import FREE_TRIAL_INTERACTIONS
from models.expense import ExpenseSchema, Category, TransactionType


# ============== Fixtures ==============

@pytest.fixture
def mock_db_service():
    """Create a mocked database service"""
    db = Mock(spec=DatabaseService)
    
    # Mock user data
    db.get_user_by_telegram_id = Mock(return_value=None)
    db.get_interaction_count = Mock(return_value=0)
    db.increment_interaction_count = Mock(return_value=1)
    db.create_expense = Mock(return_value=Mock(id=1, description="Test", amount=100.0))
    
    # Mock link code operations
    db.get_link_code = Mock(return_value=None)
    db.use_link_code = Mock(return_value=True)
    
    # Mock stats
    db.get_user_stats = Mock(return_value={
        "total_expenses": 1000.0,
        "total_income": 2000.0,
        "balance": 1000.0,
        "transaction_count": 10
    })
    db.get_user_expenses = Mock(return_value=[])
    
    return db


@pytest.fixture
def mock_ai_processor():
    """Create a mocked AI processor"""
    ai = Mock(spec=AIProcessor)
    
    # Mock successful expense extraction
    expense = ExpenseSchema(
        description="Supermercado Carrefour",
        amount=5000.0,
        currency="ARS",
        category=Category.SUPERMERCADO,
        transaction_type=TransactionType.EXPENSE
    )
    
    ai.process_image = Mock(return_value=expense)
    ai.process_audio_text = Mock(return_value=expense)
    ai.transcribe_audio = Mock(return_value="Gasté 5000 pesos en el supermercado")
    
    return ai


@pytest.fixture
def mock_sheets_service():
    """Create a mocked sheets service"""
    sheets = Mock(spec=SheetsService)
    sheets.add_expense = Mock(return_value=True)
    return sheets


@pytest.fixture
def bot_handlers(mock_db_service, mock_ai_processor, mock_sheets_service):
    """Create bot handlers with mocked services"""
    handlers = BotHandlers(
        ai_processor=mock_ai_processor,
        db_service=mock_db_service,
        sheets_service=mock_sheets_service,
        default_gemini_key="test-api-key"
    )
    return handlers


@pytest.fixture
def mock_telegram_update():
    """Create a mocked Telegram update"""
    update = Mock()
    update.effective_user = Mock()
    update.effective_user.id = 123456789
    update.effective_user.username = "testuser"
    update.effective_user.first_name = "Test"
    
    update.message = Mock()
    update.message.reply_text = AsyncMock()
    update.message.photo = None
    update.message.voice = None
    update.message.text = None
    
    return update


@pytest.fixture
def mock_context():
    """Create a mocked Telegram context"""
    context = Mock()
    context.args = []
    return context


# ============== Test Cases ==============

@pytest.mark.asyncio
class TestTelegramLinking:
    """Test account linking flow"""
    
    async def test_start_command_unlinked_user(self, bot_handlers, mock_telegram_update, mock_context):
        """Test /start for new unlinked user"""
        mock_telegram_update.message.text = "/start"
        
        await bot_handlers.start_command(mock_telegram_update, mock_context)
        
        # Should send welcome message with trial info
        mock_telegram_update.message.reply_text.assert_called_once()
        call_args = mock_telegram_update.message.reply_text.call_args[0][0]
        
        assert "¡Hola!" in call_args
        assert "interacciones gratuitas" in call_args
        bot_handlers.db.get_user_by_telegram_id.assert_called_with("123456789")
    
    async def test_start_command_linked_user(self, bot_handlers, mock_telegram_update, mock_context):
        """Test /start for linked user with API key"""
        mock_telegram_update.message.text = "/start"
        
        # Mock linked user with API key
        linked_user = Mock()
        linked_user.gemini_api_key = "user-api-key"
        linked_user.username = "testuser"
        bot_handlers.db.get_user_by_telegram_id.return_value = linked_user
        
        await bot_handlers.start_command(mock_telegram_update, mock_context)
        
        call_args = mock_telegram_update.message.reply_text.call_args[0][0]
        assert "Tu cuenta está vinculada" in call_args
    
    async def test_link_command_no_code(self, bot_handlers, mock_telegram_update, mock_context):
        """Test /link without providing code"""
        mock_telegram_update.message.text = "/link"
        
        await bot_handlers.link_command(mock_telegram_update, mock_context)
        
        call_args = mock_telegram_update.message.reply_text.call_args[0][0]
        assert "Uso incorrecto" in call_args
        assert "`/link ABC123`" in call_args
    
    async def test_link_command_invalid_code(self, bot_handlers, mock_telegram_update, mock_context):
        """Test /link with invalid code format"""
        mock_telegram_update.message.text = "/link ABC"
        mock_context.args = ["ABC"]
        
        await bot_handlers.link_command(mock_telegram_update, mock_context)
        
        call_args = mock_telegram_update.message.reply_text.call_args[0][0]
        assert "Código inválido" in call_args
    
    async def test_link_command_success(self, bot_handlers, mock_telegram_update, mock_context):
        """Test successful account linking"""
        mock_context.args = ["ABC123"]
        
        # Mock successful linking
        linked_user = Mock()
        linked_user.username = "testuser"
        bot_handlers.db.use_link_code.return_value = True
        bot_handlers.db.get_user_by_telegram_id.return_value = linked_user
        
        await bot_handlers.link_command(mock_telegram_update, mock_context)
        
        bot_handlers.db.use_link_code.assert_called_with("ABC123", "123456789")
        call_args = mock_telegram_update.message.reply_text.call_args[0][0]
        assert "¡Cuenta vinculada exitosamente!" in call_args


@pytest.mark.asyncio
class TestTelegramMessageProcessing:
    """Test message processing flow"""
    
    async def test_handle_text_message(self, bot_handlers, mock_telegram_update, mock_context):
        """Test processing text expense message"""
        mock_telegram_update.message.text = "Gasté 5000 pesos en el supermercado"
        
        await bot_handlers.handle_text(mock_telegram_update, mock_context)
        
        # Should process and save expense
        bot_handlers.default_ai.process_audio_text.assert_called_once()
        bot_handlers.db.create_expense.assert_called_once()
        bot_handlers.sheets.add_expense.assert_called_once()
        
        # Should confirm to user
        mock_telegram_update.message.reply_text.assert_called()
        call_args = mock_telegram_update.message.reply_text.call_args_list[-1][0][0]
        assert "✅ Transacción Registrada" in call_args
    
    async def test_handle_text_no_expense_found(self, bot_handlers, mock_telegram_update, mock_context):
        """Test text that doesn't contain expense info"""
        mock_telegram_update.message.text = "Hola, ¿cómo estás?"
        bot_handlers.default_ai.process_audio_text.return_value = None
        
        await bot_handlers.handle_text(mock_telegram_update, mock_context)
        
        # Should inform user
        call_args = mock_telegram_update.message.reply_text.call_args_list[-1][0][0]
        assert "No pude entender" in call_args
    
    async def test_handle_photo(self, bot_handlers, mock_telegram_update, mock_context):
        """Test processing receipt photo"""
        # Mock photo
        mock_photo = Mock()
        mock_photo.get_file = AsyncMock(return_value=Mock(
            download_to_drive=AsyncMock()
        ))
        mock_telegram_update.message.photo = [mock_photo]
        
        with patch('os.path.exists', return_value=True), \
             patch('os.remove') as mock_remove:
            
            await bot_handlers.handle_photo(mock_telegram_update, mock_context)
            
            # Should analyze and save
            bot_handlers.default_ai.process_image.assert_called_once()
            bot_handlers.db.create_expense.assert_called_once()
            mock_remove.assert_called_once()
    
    async def test_handle_voice(self, bot_handlers, mock_telegram_update, mock_context):
        """Test processing voice message"""
        # Mock voice
        mock_voice = Mock()
        mock_voice.get_file = AsyncMock(return_value=Mock(
            download_to_drive=AsyncMock()
        ))
        mock_telegram_update.message.voice = mock_voice
        
        with patch('os.path.exists', return_value=True), \
             patch('os.remove') as mock_remove:
            
            await bot_handlers.handle_voice(mock_telegram_update, mock_context)
            
            # Should transcribe and process
            bot_handlers.default_ai.transcribe_audio.assert_called_once()
            bot_handlers.default_ai.process_audio_text.assert_called_once()
            bot_handlers.db.create_expense.assert_called_once()


@pytest.mark.asyncio
class TestTelegramRateLimiting:
    """Test trial and rate limiting"""
    
    async def test_trial_limit_exceeded(self, bot_handlers, mock_telegram_update, mock_context):
        """Test blocking when trial limit exceeded"""
        mock_telegram_update.message.text = "Gasté 100 pesos"
        
        # Mock trial exceeded
        bot_handlers.db.get_interaction_count.return_value = FREE_TRIAL_INTERACTIONS + 1
        
        await bot_handlers.handle_text(mock_telegram_update, mock_context)
        
        # Should not process expense
        bot_handlers.default_ai.process_audio_text.assert_not_called()
        
        # Should inform about limit
        call_args = mock_telegram_update.message.reply_text.call_args[0][0]
        assert "límite" in call_args.lower() or "Regístrate" in call_args
    
    async def test_trial_remaining_warning(self, bot_handlers, mock_telegram_update, mock_context):
        """Test warning when running low on trials"""
        mock_telegram_update.message.text = "Gasté 100 pesos"
        
        # Mock only 2 remaining
        bot_handlers.db.increment_interaction_count.return_value = FREE_TRIAL_INTERACTIONS - 1
        
        await bot_handlers.handle_text(mock_telegram_update, mock_context)
        
        # Should send warning about remaining trials
        call_args = mock_telegram_update.message.reply_text.call_args_list[-1][0][0]
        assert "quedan" in call_args.lower() or "quedan" in call_args
    
    async def test_no_limit_for_registered_users(self, bot_handlers, mock_telegram_update, mock_context):
        """Test registered users bypass trial limit"""
        mock_telegram_update.message.text = "Gasté 100 pesos"
        
        # Mock registered user with API key
        registered_user = Mock()
        registered_user.gemini_api_key = "user-api-key"
        bot_handlers.db.get_user_by_telegram_id.return_value = registered_user
        
        # Mock high interaction count
        bot_handlers.db.get_interaction_count.return_value = 9999
        
        await bot_handlers.handle_text(mock_telegram_update, mock_context)
        
        # Should still process
        bot_handlers.default_ai.process_audio_text.assert_called_once()


@pytest.mark.asyncio
class TestTelegramCommands:
    """Test other bot commands"""
    
    async def test_stats_command_no_expenses(self, bot_handlers, mock_telegram_update, mock_context):
        """Test /stats with no expenses"""
        mock_telegram_update.message.text = "/stats"
        bot_handlers.db.get_user_stats.return_value = {
            "transaction_count": 0
        }
        
        await bot_handlers.stats_command(mock_telegram_update, mock_context)
        
        call_args = mock_telegram_update.message.reply_text.call_args[0][0]
        assert "Aún no tienes gastos" in call_args
    
    async def test_stats_command_with_data(self, bot_handlers, mock_telegram_update, mock_context):
        """Test /stats with expenses"""
        mock_telegram_update.message.text = "/stats"
        
        await bot_handlers.stats_command(mock_telegram_update, mock_context)
        
        call_args = mock_telegram_update.message.reply_text.call_args[0][0]
        assert "Tus Estadísticas" in call_args
        assert "$1000.0" in call_args  # balance
    
    async def test_recent_command(self, bot_handlers, mock_telegram_update, mock_context):
        """Test /recent command"""
        mock_telegram_update.message.text = "/recent"
        
        # Mock expenses
        expense = Mock()
        expense.description = "Supermercado"
        expense.amount = 5000.0
        expense.currency = "ARS"
        expense.category = "Supermercado"
        expense.transaction_type = "expense"
        expense.date = datetime.now()
        
        bot_handlers.db.get_user_expenses.return_value = [expense]
        
        await bot_handlers.recent_command(mock_telegram_update, mock_context)
        
        call_args = mock_telegram_update.message.reply_text.call_args[0][0]
        assert "Tus últimos gastos" in call_args
        assert "Supermercado" in call_args
    
    async def test_help_command(self, bot_handlers, mock_telegram_update, mock_context):
        """Test /help command"""
        mock_telegram_update.message.text = "/help"
        
        await bot_handlers.help_command(mock_telegram_update, mock_context)
        
        call_args = mock_telegram_update.message.reply_text.call_args[0][0]
        assert "Ayuda" in call_args
        assert "/stats" in call_args
        assert "/recent" in call_args


@pytest.mark.asyncio
class TestEndToEndFlow:
    """End-to-end integration tests"""
    
    async def test_complete_user_journey(self, bot_handlers, mock_telegram_update, mock_context):
        """Test complete flow: start -> link -> add expense -> stats"""
        user_id = "123456789"
        
        # 1. User starts bot
        mock_telegram_update.message.text = "/start"
        await bot_handlers.start_command(mock_telegram_update, mock_context)
        
        # 2. User links account
        mock_context.args = ["LINK12"]
        linked_user = Mock()
        linked_user.username = "testuser"
        linked_user.gemini_api_key = "user-key"
        bot_handlers.db.use_link_code.return_value = True
        bot_handlers.db.get_user_by_telegram_id.return_value = linked_user
        
        await bot_handlers.link_command(mock_telegram_update, mock_context)
        
        # 3. User sends expense
        mock_telegram_update.message.text = "Cena 3000 pesos"
        await bot_handlers.handle_text(mock_telegram_update, mock_context)
        
        # 4. User checks stats
        mock_telegram_update.message.text = "/stats"
        await bot_handlers.stats_command(mock_telegram_update, mock_context)
        
        # Verify all interactions
        assert bot_handlers.db.create_expense.call_count >= 1
        assert mock_telegram_update.message.reply_text.call_count >= 4


# ============== Run Tests ==============

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

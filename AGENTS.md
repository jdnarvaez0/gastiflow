# Gastiflow - AI-Powered Expense Tracker

> **Project Language**: English for code and documentation, Spanish for UI content (target audience is Spanish/English bilingual users)

## Project Overview

Gastiflow is a full-stack expense tracking application with AI-powered receipt parsing via Telegram Bot integration. Users can:
- Track expenses through Telegram (photos, voice, text)
- View analytics and manage expenses via web dashboard
- Link Telegram account for seamless expense entry
- Sync data to Google Sheets

## Architecture

### Technology Stack

| Layer | Technologies |
|-------|-------------|
| **Backend** | Python 3.10+, FastAPI, SQLAlchemy, python-telegram-bot |
| **Frontend** | Nuxt 3 (Vue 3), TailwindCSS, @nuxt/ui v4, Chart.js |
| **AI** | Google Gemini 2.0 Flash (vision + text) via LangChain |
| **Database** | PostgreSQL |
| **Deployment** | Docker, AWS EC2, Vercel, ngrok (dev) |

### Project Structure

```
gastiflow/
├── backend/                    # FastAPI backend + Telegram bot
│   ├── bot/                    # Telegram bot handlers
│   │   ├── main.py            # Bot entry point
│   │   ├── handlers.py        # Command/message handlers
│   │   └── __init__.py
│   ├── models/                 # SQLAlchemy + Pydantic models
│   │   ├── expense.py         # Expense schema & DB model
│   │   ├── user.py            # User model, auth schemas
│   │   └── telegram_link.py   # Telegram linking codes
│   ├── services/               # Business logic
│   │   ├── ai_processor.py    # Gemini AI processing
│   │   ├── auth_service.py    # JWT, password hashing
│   │   ├── database_service.py # DB operations
│   │   ├── email_service.py   # SMTP email verification
│   │   ├── security_service.py # Audit logging
│   │   └── sheets_service.py  # Google Sheets sync
│   ├── web/                    # FastAPI web application
│   │   ├── main.py            # App factory, router registration
│   │   ├── config.py          # Environment config
│   │   ├── middleware.py      # CORS, rate limiting, security headers
│   │   ├── dependencies.py    # Auth & DB dependencies
│   │   └── routers/           # API route handlers
│   │       ├── __init__.py
│   │       ├── auth.py        # Registration, login, tokens
│   │       ├── dashboard.py   # Stats, analytics
│   │       ├── email.py       # Verification endpoints
│   │       ├── expenses.py    # CRUD operations
│   │       ├── health.py      # Health checks
│   │       ├── profile.py     # User profile, uploads
│   │       └── telegram.py    # Bot linking
│   ├── migrations/             # Alembic DB migrations
│   ├── test/                   # Test suite
│   ├── run_bot.py             # Script to run Telegram bot
│   ├── start.py               # Development startup script
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile
├── frontend/                   # Nuxt 3 frontend
│   ├── components/            # Vue components
│   ├── composables/           # Reusable logic (useAuth, useApi)
│   ├── layouts/               # Nuxt layouts (default, public)
│   ├── locales/               # i18n translations (es.json, en.json)
│   ├── middleware/            # Route middleware (auth.ts)
│   ├── pages/                 # File-based routing
│   │   ├── index.vue          # Landing
│   │   ├── login.vue
│   │   ├── register.vue
│   │   ├── dashboard.vue      # Main dashboard
│   │   ├── settings.vue       # User settings
│   │   ├── verify-email.vue
│   │   └── ...
│   ├── assets/css/            # Global styles
│   ├── app.vue
│   ├── nuxt.config.ts         # Nuxt configuration
│   ├── tailwind.config.js
│   └── Dockerfile
├── docker-compose.yml         # Production Docker setup
├── docker-compose.dev.yml     # Development Docker setup
├── start-app.ps1              # Windows PowerShell startup script
├── .env.example               # Environment template
└── init.sql                   # Database initialization (optional)
```

## Development Commands

### Local Development (without Docker)

```powershell
# Start all services (Windows)
.\start-app.ps1

# Or manually - Terminal 1: API
cd backend
.\.venv\Scripts\activate
uvicorn web.main:app --reload --port 8000

# Terminal 2: Telegram Bot
cd backend
.\.venv\Scripts\activate
python run_bot.py

# Terminal 3: Frontend
cd frontend
npm run dev
```

### Docker Development

```bash
# Start all services with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Frontend Commands

```bash
cd frontend
npm install      # Install dependencies
npm run dev      # Development server (port 3000)
npm run build    # Production build
npm run preview  # Preview production build
```

### Backend Commands

```bash
cd backend
pip install -r requirements.txt
uvicorn web.main:app --reload --port 8000  # API only
python run_bot.py                            # Bot only
python start.py                              # Both (legacy)
```

## Environment Configuration

Copy `.env.example` to `.env` and configure:

```env
# REQUIRED - Core settings
JWT_SECRET_KEY=your-secret-key
ENVIRONMENT=development  # or production
DATABASE_URL=postgresql://user:pass@host:5432/db

# REQUIRED - Integrations
TELEGRAM_BOT_TOKEN=from_botfather
GEMINI_API_KEY=from_google_ai_studio

# REQUIRED - CORS
FRONTEND_URL=http://localhost:3000

# OPTIONAL - Email verification
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASSWORD=app-password

# OPTIONAL - Google Sheets
GOOGLE_SHEETS_CREDENTIALS_FILE=config/credentials.json
GOOGLE_SHEET_ID=your-sheet-id

# OPTIONAL - Ngrok (development only)
NGROK_URL=https://your-subdomain.ngrok-free.app
```

## Code Style Guidelines

### Python (Backend)

- **Style**: Follow PEP 8, use type hints everywhere
- **Imports**: Standard lib → Third party → Local modules
- **Docstrings**: Google-style docstrings for all public functions
- **Logging**: Use `loguru` for structured logging
- **Error Handling**: 
  - Use FastAPI's HTTPException for API errors
  - Log errors with context before raising
  - Handle rate limits (429) with exponential backoff in AI processor

Example:
```python
from services.database_service import DatabaseService  # Local last
from fastapi import HTTPException
from loguru import logger

def process_expense(db: DatabaseService, data: dict) -> ExpenseSchema:
    """Process and save an expense.
    
    Args:
        db: Database service instance
        data: Raw expense data
        
    Returns:
        Validated expense schema
        
    Raises:
        HTTPException: If validation fails
    """
    try:
        expense = ExpenseSchema(**data)
        db.save_expense(expense)
        logger.info(f"Expense saved: {expense.description}")
        return expense
    except ValidationError as e:
        logger.error(f"Validation failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))
```

### TypeScript/Vue (Frontend)

- **Style**: ESLint + Prettier with Nuxt conventions
- **Composables**: Use `useState` for shared state, prefix with `use`
- **Components**: PascalCase, multi-word names
- **Types**: Define interfaces in composables or dedicated types files
- **API Calls**: Use `$fetch` with proper error handling

Example:
```typescript
// composables/useFeature.ts
export interface FeatureData {
    id: number
    name: string
}

export const useFeature = () => {
    const config = useRuntimeConfig()
    const data = useState<FeatureData[]>('feature_data', () => [])
    
    const fetchData = async () => {
        data.value = await $fetch<FeatureData[]>('/api/feature', {
            baseURL: config.public.apiUrl,
            headers: { 'ngrok-skip-browser-warning': 'true' }
        })
    }
    
    return { data, fetchData }
}
```

## Testing

### Backend Tests

```bash
cd backend
python -m pytest test/           # Run all tests
python test/test_db.py          # Run specific test
```

Test files:
- `test/test_db.py` - Database operations
- `test/test_gemini.py` - AI processing
- `test/test_sheets.py` - Google Sheets integration

### Frontend Testing

No automated tests currently configured. Test manually via browser.

## Security Considerations

### Authentication
- JWT tokens with refresh token rotation
- Password requirements: 8+ chars, upper, lower, digit, special char
- Rate limiting on auth endpoints (3/hour for register)
- Email verification before full account activation

### API Security
- CORS configured to specific origins (not `*` in production)
- Rate limiting via slowapi
- Security headers (X-Content-Type-Options, X-Frame-Options, HSTS)
- Input validation with Pydantic models
- Sensitive field sanitization in error messages

### File Uploads
- Profile pictures: max 5MB, allowed extensions: .jpg, .jpeg, .png, .gif, .webp
- Files stored in `web/uploads/profile_pictures/`
- Original filenames sanitized

### Environment Variables
- Never commit `.env` files
- Use strong JWT_SECRET_KEY (64+ chars recommended)
- Use Gmail App Passwords, not account passwords
- Rotate API keys regularly

## Database Schema

### Key Tables

**users**: id, username, email, hashed_password, telegram_id, email_verified, profile_picture_url, preferences (currency, timezone, language)

**expenses**: id, user_id, description, amount, currency, category, transaction_type, date, created_at

**refresh_tokens**: id, user_id, token_hash, expires_at, revoked

**telegram_link_codes**: id, user_id, code, expires_at, used

## Deployment

See `DEPLOY.md` for detailed instructions.

**Production Architecture:**
- Frontend: Vercel (from `frontend/` directory)
- Backend API: Render or AWS EC2 (from `backend/` directory)
- Telegram Bot: AWS EC2 or Render (runs continuously)
- Database: Neon PostgreSQL or Supabase

**Environment for Production:**
- Set `ENVIRONMENT=production`
- Set `ALLOWED_HOSTS=yourdomain.com`
- Remove ngrok from allowed origins
- Configure Sentry DSN for error tracking

## Common Tasks

### Adding a New API Endpoint

1. Create/update router in `backend/web/routers/`
2. Add to `backend/web/routers/__init__.py`
3. Import and include in `backend/web/main.py`
4. Add proxy rule in `frontend/nuxt.config.ts` if needed
5. Create corresponding composable in `frontend/composables/`

### Adding a New Database Model

1. Define SQLAlchemy model in `backend/models/`
2. Create Pydantic schema for API validation
3. Add database operations to `services/database_service.py`
4. Create Alembic migration: `alembic revision -m "description"`

### Adding i18n Translations

1. Add key to `frontend/locales/es.json` and `frontend/locales/en.json`
2. Use in component: `{{ $t('key.subkey') }}`

## Troubleshooting

**Bot not responding**: Check TELEGRAM_BOT_TOKEN, ensure webhook is not set (uses polling in dev)

**CORS errors**: Verify FRONTEND_URL matches actual origin, check ngrok URL in dev

**Database connection errors**: Check DATABASE_URL format, ensure PostgreSQL is running

**AI processing fails**: Check GEMINI_API_KEY, verify rate limits not exceeded

**Profile pictures not loading**: Check uploads directory permissions, verify UPLOADS_DIR path

## External Dependencies

- **Telegram**: Create bot via @BotFather
- **Google AI**: Get API key at https://aistudio.google.com/app/apikey
- **Google Sheets**: Setup OAuth2 credentials, share sheet with service account
- **Email**: Gmail with App Password (not regular password)

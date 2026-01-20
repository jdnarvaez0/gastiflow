# 💰 Gastiflow

> AI-powered expense tracker with Telegram bot integration and web dashboard

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Nuxt](https://img.shields.io/badge/Nuxt-3-00DC82.svg)](https://nuxt.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Features

- 🤖 **Telegram Bot** - Track expenses via photos, voice, or text
- 🧠 **AI-Powered** - Google Gemini for OCR and natural language processing
- 🔐 **Authentication** - JWT-based user system with email verification
- 📊 **Web Dashboard** - Expense visualization and stats
- 📧 **Email Verification** - Secure account confirmation
- 📑 **Google Sheets** - Auto-sync expenses
- 💾 **PostgreSQL** - Robust database storage
- 🏗️ **Modular Architecture** - Clean FastAPI routers pattern

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Backend** | Python 3.10+, FastAPI, SQLAlchemy, python-telegram-bot |
| **Frontend** | Nuxt 3, Vue 3, TailwindCSS, Chart.js |
| **AI** | Google Gemini 2.0 Flash |
| **Database** | PostgreSQL |
| **Deployment** | AWS EC2, Vercel, ngrok |

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ and Node.js 18+
- PostgreSQL database
- [Gemini API Key](https://aistudio.google.com/app/apikey)
- [Telegram Bot Token](https://t.me/botfather)

### Setup

1. **Clone and configure**
```bash
git clone https://github.com/jdnarvaez0/gastiflow.git
cd gastiflow
cp backend/.env.example backend/.env
# Edit backend/.env with your credentials
```

2. **Install dependencies**
```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

3. **Run services**
```bash
# Option A: Automated (Windows)
.\start-app.ps1

# Option B: Manual
# Terminal 1 - API
cd backend && uvicorn web.main:app --reload --port 8000

# Terminal 2 - Telegram Bot
cd backend && python run_bot.py

# Terminal 3 - Frontend
cd frontend && npm run dev
```

**Access:**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health

## 📁 Project Structure

```
gastiflow/
├── backend/
│   ├── web/
│   │   ├── main.py           # FastAPI app (115 lines)
│   │   ├── config.py         # Environment config
│   │   ├── dependencies.py   # Auth & DB dependencies
│   │   ├── middleware.py     # CORS, security, rate limiting
│   │   └── routers/          # Modular API endpoints
│   │       ├── auth.py       # Authentication
│   │       ├── expenses.py   # Expense management
│   │       ├── profile.py    # Profile & settings
│   │       ├── telegram.py   # Telegram linking
│   │       └── health.py     # System monitoring
│   ├── bot/                  # Telegram bot handlers
│   ├── services/             # Business logic (Auth, AI, DB, Email)
│   ├── models/               # SQLAlchemy models
│   └── migrations/           # Database migrations
├── frontend/
│   ├── pages/                # Routes (login, dashboard, settings)
│   ├── components/           # Vue components
│   └── composables/          # Reusable logic (auth, API)
└── .env.example              # Environment template
```

## 🐳 Docker

```bash
docker-compose up -d
```

## 🌍 Deployment

**Production Setup:**
- Frontend: [Vercel](https://gastiflow.vercel.app)
- Backend: AWS EC2 + ngrok tunnel
- Database: PostgreSQL (Supabase/Neon compatible)

See [DEPLOY.md](DEPLOY.md) for detailed instructions.

## 🔧 Environment Variables

Key variables (see `backend/.env.example` for full list):

```env
# Required
TELEGRAM_BOT_TOKEN=your_bot_token
GEMINI_API_KEY=your_api_key
DATABASE_URL=postgresql://user:pass@host:5432/db
JWT_SECRET_KEY=your_secret_key

# Optional
SMTP_USER=your@gmail.com        # For email verification
SMTP_PASSWORD=app_password       # Gmail app password
FRONTEND_URL=http://localhost:3000
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | System health check |
| `/api/register` | POST | User registration |
| `/api/login` | POST | Login (returns JWT) |
| `/api/me` | GET | Get current user |
| `/api/dashboard` | GET | Expense stats |
| `/api/expenses` | POST | Add expense |
| `/api/profile-picture` | POST | Upload avatar |
| `/api/telegram/link-code` | POST | Get Telegram link code |

Full API docs: http://localhost:8000/docs

## 🤝 Contributing

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

MIT License - See [LICENSE](LICENSE)

---

⭐ Star this repo if you find it useful!

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
| **Frontend** | Nuxt 3, Vue 3, TailwindCSS, @nuxt/ui v4, Chart.js |
| **AI** | Google Gemini 2.0 Flash |
| **Database** | PostgreSQL |
| **Deployment** | AWS EC2, Vercel, ngrok |

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ and Node.js 18+
- PostgreSQL database (or Docker)
- [Gemini API Key](https://aistudio.google.com/app/apikey)
- [Telegram Bot Token](https://t.me/botfather)

### Option 1: Automated Setup (Recommended)

```bash
# Clone repository
git clone https://github.com/jdnarvaez0/gastiflow.git
cd gastiflow

# Run setup script (Windows)
.\setup.ps1

# Or using Task (cross-platform)
# Install Task: https://taskfile.dev/installation/
task setup
```

### Option 2: Manual Setup

```bash
# Clone and configure
git clone https://github.com/jdnarvaez0/gastiflow.git
cd gastiflow
cp .env.example .env
# Edit .env with your credentials

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Dashboard (App)
cd ../apps/dashboard
npm install

# Landing Page (Marketing)
cd ../apps/landing
npm install
```

### Running the Application

```bash
# Using PowerShell script (Windows - Recommended)
.\start-app.ps1       # Start all services (API + Bot + Dashboard + Landing)

# Using Task (cross-platform)
task dev              # Start all services
task dev:api          # API only
task dev:bot          # Telegram bot only
task dev:dashboard    # Dashboard only
task dev:landing      # Landing only

# Using Docker
docker-compose -f docker-compose.yml -f docker-compose.override.yml up

# Manual (separate terminals)
cd backend && uvicorn web.main:app --reload --port 8000
cd backend && python run_bot.py
cd apps/dashboard && npm run dev
cd apps/landing && npm run dev -- --port 3001
```

**Access Points:**
- 🌐 Landing Page: http://localhost:3001 (Marketing site)
- 🎨 Dashboard: http://localhost:3000 (App - requires login)
- 📚 API Docs: http://localhost:8000/docs
- 🏥 Health: http://localhost:8000/api/health

**Verify everything is running:**
```bash
.\health-check.ps1    # Windows
# or
task health           # Using Task
```

## 📁 Project Structure

```
gastiflow/
├── backend/
│   ├── web/
│   │   ├── main.py           # FastAPI app
│   │   ├── config.py         # Environment config
│   │   ├── dependencies.py   # Auth & DB dependencies
│   │   ├── middleware.py     # CORS, security, rate limiting
│   │   └── routers/          # Modular API endpoints
│   │       ├── auth.py       # Authentication
│   │       ├── expenses.py   # Expense management (paginated)
│   │       ├── budgets.py    # Budget management (new!)
│   │       ├── profile.py    # Profile & settings
│   │       ├── telegram.py   # Telegram linking
│   │       └── health.py     # System monitoring
│   ├── bot/                  # Telegram bot handlers
│   ├── services/             # Business logic
│   ├── models/               # SQLAlchemy models
│   └── migrations/           # Database migrations
├── apps/
│   ├── dashboard/            # Main app (SSR - requires auth)
│   │   ├── pages/            # Routes (dashboard, settings, etc.)
│   │   ├── components/       # Vue components
│   │   ├── composables/      # Reusable logic (useAuth, useApi)
│   │   └── layouts/          # App layouts
│   └── landing/              # Marketing site (SSG - public)
│       ├── pages/            # Landing page
│       └── components/       # Marketing components
├── .github/workflows/        # CI/CD
├── docker-compose.override.yml  # Dev services
├── Taskfile.yml             # Task commands
└── setup.ps1                # Windows setup script
```

## 🛠️ Development Commands

### Using Task (Recommended)

```bash
# Development
task dev              # Start all services (API + Bot + Dashboard + Landing)
task dev:api          # API server only
task dev:bot          # Telegram bot only
task dev:dashboard    # Dashboard only (port 3000)
task dev:landing      # Landing page only (port 3001)

# Using PowerShell (Windows)
.\start-app.ps1       # Start all services with single command

# Testing
task test             # Run all tests
task test:backend     # Backend tests
task test:integration # Telegram integration tests

# Docker
task docker:up        # Start services
task docker:down      # Stop services
task docker:logs      # View logs

# Utilities
task env:check        # Verify configuration
task db:clean         # Clean expired tokens
task clean            # Clean cache files
task --list-all       # Show all commands
```

### Using Make

```bash
make setup         # Setup environment
make dev           # Start all services
make test          # Run tests
make docker-up     # Start with Docker
make help          # Show all commands
```

## 🐳 Docker

```bash
# Development with all services
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d

# View logs
task docker:logs
```

## 🔄 CI/CD Pipeline

**Continuous Integration (Automated):**

| Trigger | Tests | Build | Docker |
|---------|-------|-------|--------|
| PR to `dev` | ✅ | ✅ | ✅ |
| PR to `main` | ✅ | ✅ | ✅ |
| Push to `main` | ✅ | ✅ | ✅ |

**Deployment (Manual):**

| Environment | Trigger | Command |
|-------------|---------|---------|
| Staging | Manual | GitHub Actions → "Deploy to Staging" |
| Production | Manual | GitHub Actions → "Deploy to Production" |

**Required Secrets:**

Configure these in GitHub → Settings → Secrets and variables → Actions:

```bash
# For Staging Deployment
STAGING_SSH_HOST          # Your staging server IP/hostname
STAGING_SSH_USER          # SSH username
STAGING_SSH_KEY           # Private SSH key
STAGING_DEPLOY_DIR        # Deploy directory (default: /opt/gastiflow-staging)

# For Production Deployment  
SSH_HOST                  # Production server IP/hostname
SSH_USER                  # SSH username
SSH_PRIVATE_KEY           # Private SSH key
DEPLOY_DIR                # Deploy directory (default: /opt/gastiflow)
```

**Deploy to Staging:**
1. Go to GitHub → Actions → "Deploy to Staging"
2. Click "Run workflow"
3. Select branch (`dev` or `main`)
4. Click "Run workflow"

**Deploy to Production:**
1. Go to GitHub → Actions → "Deploy to Production"
2. Click "Run workflow"
3. Type "deploy" to confirm
4. Click "Run workflow"

⚠️ **Production deploy requires typing "deploy" to prevent accidental deployments.**

## 🌍 Deployment

**Architecture:**
- **Landing Page** (SSG): Vercel/Netlify (marketing site)
- **Dashboard** (SSR): Render/Railway/VPS (app with auth)
- **Backend API**: Render/Railway/VPS
- **Telegram Bot**: Background worker (always-on)
- **Database**: PostgreSQL (Supabase/Neon/Railway)

See [DEPLOY_NEW.md](DEPLOY_NEW.md) for detailed instructions on the new architecture.

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

# 💰 Gastiflow - AI-Powered Expense Tracker

> Sistema inteligente de gestión de gastos con bot de Telegram y panel web

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Nuxt](https://img.shields.io/badge/Nuxt-3-00DC82.svg)](https://nuxt.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Características

- 🤖 **Bot de Telegram** - Registra gastos con fotos, voz o texto
- 🧠 **IA Integrada** - Google Gemini para OCR y procesamiento de lenguaje natural
-  **Autenticación** - Sistema completo de usuarios con JWT
- � **Dashboard Web** - Visualización de gastos y estadísticas
- 📧 **Verificación de Email** - Confirmación de cuentas
- � **Google Sheets** - Sincronización automática
- 💾 **PostgreSQL** - Base de datos robusta

## 🛠️ Stack Tecnológico

**Backend:** Python 3.10+, FastAPI, SQLAlchemy, python-telegram-bot  
**Frontend:** Nuxt 3, Vue 3, Chart.js  
**IA:** Google Gemini (gemini-2.5-flash)  
**Database:** PostgreSQL  
**Deployment:** AWS EC2, Vercel, ngrok

## 📋 Prerrequisitos

- Python 3.10+
- Node.js 18+
- PostgreSQL
- [API Key de Google Gemini](https://aistudio.google.com/app/apikey)
- [Token de Bot de Telegram](https://t.me/botfather)
- Cuenta de Gmail (para emails)

## 🚀 Instalación

### 1. Clonar repositorio

```bash
git clone https://github.com/jdnarvaez0/gastiflow.git
cd gastiflow
```

### 2. Configurar variables de entorno

Crea un archivo `.env` basado en `.env.example`:

```env
# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token

# IA
GEMINI_API_KEY=your_gemini_api_key

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/gastiflow

# Auth
JWT_SECRET_KEY=your_secret_key

# Email (Gmail)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password

# Frontend
FRONTEND_URL=http://localhost:3000
```

### 3. Instalar dependencias

**Backend:**
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 4. Iniciar aplicación

**Opción A - Script automático (Windows):**
```powershell
.\start-app.ps1
```

**Opción B - Manual:**
```bash
# Terminal 1 - API
cd backend
uvicorn web.main:app --reload --port 8000

# Terminal 2 - Bot
cd backend
python run_bot.py

# Terminal 3 - Frontend
cd frontend
npm run dev
```

**Acceder:**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

## 🐳 Docker

```bash
docker-compose up -d
```

## 🌍 Deployment

### Producción Actual
- **Frontend:** Vercel (https://gastiflow.vercel.app)
- **Backend:** AWS EC2 + ngrok
- **Database:** PostgreSQL (Supabase/Neon)

### Configurar ngrok (HTTPS para EC2)

1. **Instalar y configurar:**
```bash
sudo snap install ngrok
ngrok config add-authtoken YOUR_TOKEN
```

2. **Crear servicio systemd:**
```bash
sudo nano /etc/systemd/system/ngrok.service
```

```ini
[Unit]
Description=ngrok secure tunnel
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu
ExecStart=/snap/bin/ngrok http 8000 --log=stdout --request-header-add='ngrok-skip-browser-warning:true'
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. **Activar:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable ngrok
sudo systemctl start ngrok
```

4. **Obtener URL y configurar en Vercel:**
```bash
curl http://localhost:4040/api/tunnels | grep public_url
```

Agrega `NUXT_API_URL` en Vercel con la URL de ngrok y redeploy.

Ver `DEPLOY.md` para más detalles.

## 📁 Estructura

```
gastiflow/
├── backend/           # Python FastAPI + Bot
│   ├── bot/          # Telegram bot handlers
│   ├── web/          # REST API
│   ├── services/     # Auth, AI, Database, Email
│   ├── models/       # SQLAlchemy models
│   └── migrations/   # Database migrations
├── frontend/          # Nuxt 3 application
│   ├── pages/        # Routes (login, dashboard, etc)
│   ├── components/   # Vue components
│   └── composables/  # Auth logic
├── .env.example      # Environment template
├── docker-compose.yml
└── start-app.ps1     # Windows startup script
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

MIT License - Ver [LICENSE](LICENSE)

---

⭐ Si te fue útil, dale una estrella!

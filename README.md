# 💰 Gastiflow - AI-Powered Expense Tracker

> **Version 0.1.0** - MVP (Minimum Viable Product)

Un bot de Telegram inteligente para rastrear gastos automáticamente usando IA, con un moderno panel web para visualización y gestión.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Nuxt](https://img.shields.io/badge/Nuxt-3-00DC82.svg)](https://nuxt.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://core.telegram.org/bots)

## ✨ Características

- 🤖 **Bot de Telegram** - Registra gastos desde cualquier lugar
- 📸 **OCR con IA** - Extrae datos de fotos de facturas usando Google Gemini Vision
- 🎤 **Transcripción de voz** - Convierte mensajes de voz a gastos
- 💬 **Procesamiento de lenguaje natural** - Entiende descripciones en texto plano
- 📊 **Panel Web Moderno** - Dashboard interactivo construido con Nuxt 3 y TailwindCSS
- 📈 **Google Sheets** - Sincronización automática con hojas de cálculo
- 💾 **Base de datos PostgreSQL** - Almacenamiento persistente y confiable
- 🔄 **Múltiples formatos** - Acepta fotos, voz y texto

## 🏗️ Arquitectura

```
┌─────────────────┐
│  Telegram Bot   │ ← Usuario envía gasto (foto/voz/texto)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AI Processor   │ ← Google Gemini (Vision + NLP)
│ (Gemini Flash)  │
└────────┬────────┘
         │
         ├─────────────┐
         │             │
         ▼             ▼
┌──────────────┐  ┌────────────────┐
│  PostgreSQL  │  │ Google Sheets  │
│   Database   │  │  (Backup/Sync) │
└──────┬───────┘  └────────────────┘
       │
       │
       ▼
┌──────────────────┐
│   FastAPI API    │ ← Backend Service
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Nuxt 3 Frontend │ ← Panel de visualización (Browser)
└──────────────────┘
```

## 🛠️ Stack Tecnológico

### Backend
- **Lenguaje**: Python 3.10+
- **Framework Web**: FastAPI
- **AI/LLM**: Google Gemini (gemini-2.5-flash), LangChain
- **Bot**: python-telegram-bot
- **Base de Datos**: PostgreSQL, SQLAlchemy
- **Validación**: Pydantic

### Frontend
- **Framework**: Nuxt 3 (Vue 3)
- **UI Library**: Nuxt UI
- **Estilos**: TailwindCSS
- **Iconos**: Heroicons

### Infraestructura
- **Contenedores**: Docker + Docker Compose
- **Scripting**: PowerShell (para automatización local)

## 📋 Prerrequisitos

- Python 3.10 o superior
- Node.js 18+ (para el frontend)
- PostgreSQL (local o Docker)
- API Key de Google Gemini
- Token de Bot de Telegram
- Credenciales de Google Cloud (para Sheets)

## 🚀 Instalación y Uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/jdnarvaez0/gastiflow
cd gastiflow
```

### 2. Configuración Rápida (Windows)

El proyecto incluye un script de PowerShell para automatizar el inicio de todos los servicios.

1.  Asegúrate de tener configurado tu archivo `.env` (ver sección de Configuración).
2.  Ejecuta el script de inicio:

```powershell
.\start-app.ps1
```

Este script verificará e instalará las dependencias necesarias, y levantará:
- Backend (FastAPI) en `http://localhost:8000`
- Bot de Telegram
- Frontend (Nuxt) en `http://localhost:3000`

### 3. Instalación Manual

Si prefieres configurar cada parte manualmente:

#### Backend

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
```

#### Frontend

```bash
cd frontend
npm install
```

### 4. Configuración (.env)

Crea un archivo `.env` en la carpeta raíz (o en `backend/` si ejecutas manualmente) basado en `.env.example`.

**Variables principales:**

```env
TELEGRAM_BOT_TOKEN=tu_token
GEMINI_API_KEY=tu_api_key
DATABASE_URL=postgresql://user:pass@localhost:5432/gastiflow
```

## 🐳 Docker

Para ejecutar todo el stack usando Docker:

```bash
docker-compose up -d
```

Esto levantará la base de datos, el backend y el frontend en contenedores.

## 📁 Estructura del Proyecto

```
gastiflow/
├── backend/                # Código del servidor y bot
│   ├── bot/               # Lógica del bot de Telegram
│   ├── web/               # API FastAPI
│   ├── services/          # Lógica de negocio (AI, DB, Sheets)
│   ├── models/            # Modelos SQLAlchemy
│   └── requirements.txt   # Dependencias Python
├── frontend/               # Aplicación web Nuxt 3
│   ├── components/        # Componentes Vue
│   ├── pages/             # Rutas de la aplicación
│   └── nuxt.config.ts     # Configuración de Nuxt
├── docker-compose.yml      # Orquestación de contenedores
├── start-app.ps1          # Script de inicio rápido (Windows)
└── README.md              # Documentación
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

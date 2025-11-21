# 💰 Gastiflow - AI-Powered Expense Tracker

> **Version 0.1.0** - MVP (Minimum Viable Product)

Un bot de Telegram inteligente para rastrear gastos automáticamente usando IA, con interfaz web para visualización.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://core.telegram.org/bots)

## ✨ Características

- 🤖 **Bot de Telegram** - Registra gastos desde cualquier lugar
- 📸 **OCR con IA** - Extrae datos de fotos de facturas usando Google Gemini Vision
- 🎤 **Transcripción de voz** - Convierte mensajes de voz a gastos
- 💬 **Procesamiento de lenguaje natural** - Entiende descripciones en texto plano
- 📊 **Panel web** - Visualiza tus gastos y estadísticas en tiempo real
- 📈 **Google Sheets** - Sincronización automática con hojas de cálculo
- 💾 **Base de datos PostgreSQL** - Almacenamiento persistente y confiable
- 🔄 **Múltiples formatos** - Acepta fotos, voz y texto

## 🎯 Casos de Uso

1. **Foto de factura** → El bot extrae automáticamente: descripción, monto, categoría
2. **Mensaje de voz** → "Gasté 500 pesos en el supermercado" → Registro automático
3. **Mensaje de texto** → "Cena 3000" → Procesado con IA y categorizado

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
│   FastAPI Web    │ ← Panel de visualización
│    Dashboard     │
└──────────────────┘
```

## 🛠️ Stack Tecnológico

- **Backend**: Python 3.10+
- **LLM Framework**: LangChain - Framework para construcción de aplicaciones con LLMs
- **Bot Framework**: python-telegram-bot
- **AI/ML**: Google Gemini (gemini-2.5-flash)
- **Web Framework**: FastAPI + Jinja2
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Data Validation**: Pydantic
- **Cloud Storage**: Google Sheets API
- **Containerization**: Docker + Docker Compose

## 📋 Prerequisitos

Antes de comenzar, asegúrate de tener:

- Python 3.10 o superior
- PostgreSQL (local o cloud como Supabase/Neon)
- Una API Key de Google Gemini ([Google AI Studio](https://aistudio.google.com/))
- Un bot de Telegram (creado con [@BotFather](https://t.me/botfather))
- Credenciales de Google Cloud (para Sheets API)

## 🚀 Instalación Rápida

### 1. Clonar el repositorio

```bash
git clone https://github.com/jdnarvaez0/gastiflow
cd gastiflow
```

### 2. Crear entorno virtual

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
```

**Variables requeridas en `.env`:**

```env
# Bot de Telegram
TELEGRAM_BOT_TOKEN=tu_token_de_botfather

# Google Gemini API
GEMINI_API_KEY=tu_api_key_de_gemini

# Base de datos
DATABASE_URL=postgresql://user:password@localhost:5432/gastiflow

# Google Sheets
GOOGLE_SHEETS_CREDENTIALS_FILE=config/credentials.json
GOOGLE_SHEET_ID=tu_id_de_google_sheet
```

### 5. Configurar Google Sheets (Opcional)

1. Crea un proyecto en [Google Cloud Console](https://console.cloud.google.com/)
2. Habilita Google Sheets API y Google Drive API
3. Crea una Service Account y descarga el JSON de credenciales
4. Guarda el archivo como `config/credentials.json`
5. Comparte tu Google Sheet con el email de la service account

### 6. Ejecutar el bot

```bash
python run_bot.py
```

### 7. Ejecutar el panel web (opcional)

```bash
uvicorn web.main:app --reload
```

Abre tu navegador en `http://localhost:8000`

## 🐳 Docker

Para ejecutar con Docker:

```bash
# Iniciar servicios (PostgreSQL + Web)
docker-compose up -d

# Para ejecutar solo el bot
python run_bot.py
```

## 📖 Uso

### Comandos del Bot

- `/start` - Mensaje de bienvenida
- `/help` - Ayuda y guía de uso
- `/stats` - Ver estadísticas de gastos
- `/recent` - Ver últimos 10 gastos

### Registrar un Gasto

**Opción 1: Foto de factura**
- Envía una foto del recibo al bot
- El bot extrae automáticamente toda la información

**Opción 2: Mensaje de voz**
- Graba un audio: "Gasté 1500 pesos en transporte"
- El bot transcribe y procesa el gasto

**Opción 3: Mensaje de texto**
- Escribe: "Almuerzo 2500 pesos"
- El bot lo procesa con IA

## 📁 Estructura del Proyecto

```
gastiflow/
├── bot/                    # Bot de Telegram
│   ├── main.py            # Entry point del bot
│   └── handlers.py        # Handlers de mensajes
├── web/                    # Interfaz web
│   ├── main.py            # FastAPI app
│   ├── templates/         # Plantillas HTML
│   └── static/            # CSS, JS, assets
├── services/               # Servicios core
│   ├── ai_processor.py    # Procesamiento con Gemini
│   ├── database_service.py # ORM y queries
│   └── sheets_service.py  # Integración con Sheets
├── models/                 # Modelos de datos
│   └── expense.py         # Schema de gastos
├── config/                 # Configuración
│   └── credentials.json   # Credenciales de Google (gitignored)
├── test/                   # Tests
├── requirements.txt        # Dependencias
├── .env.example           # Template de variables
├── docker-compose.yml     # Configuración Docker
└── README.md              # Este archivo
```

## 🔐 Seguridad

⚠️ **IMPORTANTE**: Nunca subas estos archivos a Git:
- `.env` - Variables de entorno
- `config/credentials.json` - Credenciales de Google
- `bot_logs.log` - Logs del bot

El archivo `.gitignore` ya está configurado para ignorar estos archivos.

## 🧪 Testing

```bash
# Ejecutar todos los tests
python -m pytest test/

# Test específico
python test/test_db.py
```

## 🗺️ Roadmap

### v0.2.0 (Próxima versión)
- [ ] Autenticación de usuarios en web
- [ ] Editar/eliminar gastos desde el bot
- [ ] Exportar reportes en PDF
- [ ] Gráficos estadísticos

### v0.3.0 (Futuro)
- [ ] Presupuestos mensuales
- [ ] Alertas y notificaciones
- [ ] Categorías personalizadas
- [ ] Multi-moneda con conversión automática

## 🤝 Contribuir

Las contribuciones son bienvenidas! Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

⭐ Si te gusta este proyecto, dale una estrella en GitHub!

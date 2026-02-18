# Gastiflow Makefile
# For Windows users, use `task` command instead (see Taskfile.yml)

.PHONY: help setup dev test clean docker-up docker-down

# Default target
help:
	@echo "Gastiflow Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup         - Setup development environment"
	@echo ""
	@echo "Development:"
	@echo "  make dev           - Start all services"
	@echo "  make dev-api       - Start FastAPI server"
	@echo "  make dev-bot       - Start Telegram bot"
	@echo "  make dev-frontend  - Start Nuxt dev server"
	@echo ""
	@echo "Testing:"
	@echo "  make test          - Run all tests"
	@echo "  make test-backend  - Run backend tests"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up     - Start with Docker Compose"
	@echo "  make docker-down   - Stop Docker services"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean         - Clean cache files"
	@echo "  make env-check     - Verify environment config"

# Setup
setup:
	@echo "Setting up Gastiflow..."
	cd backend && python -m venv .venv || true
	cd backend && .venv/bin/pip install -r requirements.txt
	cd frontend && npm install
	@echo "✅ Setup complete!"

# Development

dev:
	@echo "Starting all services..."
	make dev-api & make dev-bot & make dev-frontend

dev-api:
	cd backend && .venv/bin/uvicorn web.main:app --reload --port 8000

dev-bot:
	cd backend && .venv/bin/python run_bot.py

dev-frontend:
	cd frontend && npm run dev

# Testing
test:
	make test-backend

test-backend:
	cd backend && .venv/bin/pytest test/ -v --tb=short

test-integration:
	cd backend && .venv/bin/pytest test/test_telegram_integration.py -v

# Docker
docker-up:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d

docker-down:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml down

docker-logs:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml logs -f

docker-build:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml build

# Utilities
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf backend/.pytest_cache frontend/.nuxt frontend/dist 2>/dev/null || true
	@echo "✅ Clean complete"

env-check:
	@echo "Checking environment..."
	@test -f .env || (echo "❌ .env file not found" && exit 1)
	@grep -q "JWT_SECRET_KEY=" .env || (echo "❌ JWT_SECRET_KEY not set" && exit 1)
	@grep -q "DATABASE_URL=" .env || (echo "❌ DATABASE_URL not set" && exit 1)
	@grep -q "GEMINI_API_KEY=" .env || (echo "❌ GEMINI_API_KEY not set" && exit 1)
	@echo "✅ Environment OK"

# Database
db-migrate:
	cd backend && .venv/bin/python migrations/run_migration.py

db-clean:
	cd backend && .venv/bin/python -c "
from services.database_service import DatabaseService
from web.config import DATABASE_URL
db = DatabaseService(DATABASE_URL)
tokens = db.cleanup_expired_tokens()
codes = db.cleanup_expired_link_codes()
print(f'Cleaned {tokens} expired tokens')
print(f'Cleaned {codes} expired link codes')
"

# Production (use with caution)
deploy:
	@echo "Deploying to production..."
	bash ./deploy.sh

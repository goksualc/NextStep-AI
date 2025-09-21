# InternAI Development Makefile

.PHONY: help setup dev-web dev-api dev lint format test clean install-deps install-web-deps install-api-deps

# Default target
help:
	@echo "InternAI Development Commands:"
	@echo ""
	@echo "  setup          - Initial project setup"
	@echo "  dev-web        - Start Next.js development server"
	@echo "  dev-api        - Start FastAPI development server"
	@echo "  dev            - Start both web and API servers"
	@echo "  lint           - Run linting for all projects"
	@echo "  format         - Format code for all projects"
	@echo "  test           - Run tests for all projects"
	@echo "  clean          - Clean build artifacts and dependencies"
	@echo "  install-deps   - Install all dependencies"
	@echo "  install-web-deps - Install web app dependencies"
	@echo "  install-api-deps - Install API dependencies"
	@echo ""

# Initial setup
setup: install-deps
	@echo "Setting up InternAI project..."
	@cp env.example .env || echo "Please copy env.example to .env and configure your settings"
	@echo "Setup complete! Don't forget to configure your .env file."

# Install all dependencies
install-deps: install-web-deps install-api-deps
	@echo "All dependencies installed!"

# Install web app dependencies
install-web-deps:
	@echo "Installing web app dependencies..."
	cd apps/web && npm install

# Install API dependencies
install-api-deps:
	@echo "Installing API dependencies..."
	cd apps/api && pip install -r requirements.txt
	cd packages/embeddings && pip install -e .

# Development servers
dev-web:
	@echo "Starting Next.js development server..."
	cd apps/web && npm run dev

dev-api:
	@echo "Starting FastAPI development server..."
	cd apps/api && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

dev: 
	@echo "Starting both development servers..."
	@echo "Web app will be available at http://localhost:3000"
	@echo "API will be available at http://localhost:8000"
	@echo "API docs will be available at http://localhost:8000/docs"
	@echo ""
	@echo "Starting servers in background..."
	@make dev-web &
	@make dev-api

# Linting
lint:
	@echo "Running linting for web app..."
	cd apps/web && npm run lint
	@echo "Running linting for API..."
	cd apps/api && python -m black --check .
	cd apps/api && python -m ruff check .
	cd packages/embeddings && python -m black --check .
	cd packages/embeddings && python -m ruff check .

# Formatting
format:
	@echo "Formatting web app code..."
	cd apps/web && npm run format
	@echo "Formatting API code..."
	cd apps/api && python -m black .
	cd apps/api && python -m ruff --fix .
	cd packages/embeddings && python -m black .
	cd packages/embeddings && python -m ruff --fix .

# Testing
test:
	@echo "Running web app tests..."
	cd apps/web && npm run test || echo "No tests configured for web app yet"
	@echo "Running API tests..."
	cd apps/api && python -m pytest tests/ || echo "No tests configured for API yet"

# Type checking
type-check:
	@echo "Running TypeScript type checking..."
	cd apps/web && npm run type-check
	@echo "Running Python type checking..."
	cd apps/api && python -m mypy . || echo "MyPy not configured yet"
	cd packages/embeddings && python -m mypy . || echo "MyPy not configured yet"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	cd apps/web && rm -rf .next out build
	cd apps/api && find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	cd apps/api && find . -type f -name "*.pyc" -delete 2>/dev/null || true
	cd packages/embeddings && find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	cd packages/embeddings && find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Production build
build: clean
	@echo "Building web app for production..."
	cd apps/web && npm run build

# Docker commands (for future use)
docker-build:
	@echo "Building Docker images..."
	docker build -f apps/web/Dockerfile -t internai-web apps/web/
	docker build -f apps/api/Dockerfile -t internai-api apps/api/

docker-run:
	@echo "Running with Docker Compose..."
	docker-compose up --build

# Database commands (for future use)
db-migrate:
	@echo "Running database migrations..."
	@echo "Database migrations not implemented yet"

db-seed:
	@echo "Seeding database..."
	@echo "Database seeding not implemented yet"

# Agent-specific commands
test-agents:
	@echo "Testing AI agents..."
	cd agents/cv_analyzer && python -m pytest . || echo "CV Analyzer tests not implemented yet"
	cd agents/job_scout && python -m pytest . || echo "Job Scout tests not implemented yet"
	cd agents/matcher && python -m pytest . || echo "Matcher tests not implemented yet"
	cd agents/app_writer && python -m pytest . || echo "App Writer tests not implemented yet"
	cd agents/coach && python -m pytest . || echo "Coach tests not implemented yet"

# Documentation
docs:
	@echo "Generating API documentation..."
	cd apps/api && python -c "import main; print('API documentation available at http://localhost:8000/docs')"

# Health check
health:
	@echo "Checking service health..."
	@curl -s http://localhost:8000/health | jq . || echo "API not running"
	@curl -s http://localhost:3000 > /dev/null && echo "Web app is running" || echo "Web app not running"

# Variables
PYTHON = poetry run python
PYTEST = poetry run pytest
ALEMBIC = poetry run alembic
UVICORN = poetry run uvicorn
BLACK = poetry run black
ISORT = poetry run isort
PYRIGHT = poetry run pyright
RUFF = poetry run ruff
APP_PATH = src/app
TEST_PATH = tests
MIGRATIONS_PATH = migrations

.PHONY: help
help: ## Show this help message
	@echo 'Usage:'
	@echo '  make <target>'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: install
install: ## Install dependencies
	poetry install

.PHONY: format
format: ## Format code using black and isort
	$(BLACK) $(APP_PATH) $(TEST_PATH)
	$(ISORT) $(APP_PATH) $(TEST_PATH)

.PHONY: lint
lint: ## Run linting (ruff, black, isort, PYRIGHT)
	$(RUFF) check $(APP_PATH) $(TEST_PATH) --fix
	$(BLACK) $(APP_PATH) $(TEST_PATH)
	$(ISORT) $(APP_PATH) $(TEST_PATH)
	$(PYRIGHT) $(APP_PATH)

.PHONY: test
test: ## Run tests
	$(PYTEST) $(TEST_PATH) -v --cov=$(APP_PATH) --cov-report=term-missing

.PHONY: test-watch
test-watch: ## Run tests in watch mode
	$(PYTEST) $(TEST_PATH) -v -f

.PHONY: db-up
db-up: ## Start the database container
	docker-compose up -d db

.PHONY: db-down
db-down: ## Stop the database container
	docker-compose down

.PHONY: db-shell
db-shell: ## Connect to the database using psql
	docker-compose exec db psql -U postgres -d db

.PHONY: migration-create
migration-create: ## Create a new migration (use make migration-create message="migration message")
	$(ALEMBIC) revision --autogenerate -m "$(message)"

.PHONY: migration-up
migration-up: ## Run all migrations
	$(ALEMBIC) upgrade head

.PHONY: migration-down
migration-down: ## Rollback last migration
	$(ALEMBIC) downgrade -1

.PHONY: migration-reset
migration-reset: ## Rollback all migrations
	$(ALEMBIC) downgrade base

.PHONY: migration-history
migration-history: ## Show migration history
	$(ALEMBIC) history --verbose

.PHONY: run
run: ## Run the development server
	$(UVICORN) src.app.main:app --reload --host 0.0.0.0 --port 8000

.PHONY: clean
clean: ## Clean python cache files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".PYRIGHT_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

.PHONY: setup-dev
setup-dev: install db-up migration-up ## Setup development environment

.PHONY: update
update: ## Update dependencies
	poetry update

.PHONY: check-migrations
check-migrations: ## Check if there are pending migrations
	$(ALEMBIC) check

.PHONY: all
all: lint test ## Run all checks (linting and tests)
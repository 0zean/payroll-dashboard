# Makefile

# Install dependencies
install:
	@echo "🚀 Creating virtual environment using uv"
	uv sync --frozen

# Format code with Black and isort
format:
	uv run ruff format --check ./payroll_dashboard ./main.py ./rxconfig.py
	uv run ruff check --select I ./payroll_dashboard ./main.py ./rxconfig.py

# Linting and formatting with ruff
lint:
	uv run ruff check ./payroll_dashboard ./main.py ./rxconfig.py

# Run tests
test:
	uv run pytest ./payroll_dashboard/tests/

# Run all checks
check: format lint test

.PHONY: install format lint test check
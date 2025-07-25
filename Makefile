# Makefile

# Install dependencies
install:
	uv sync --freeze

# Format code with Black and isort
format:
	uv run ruff format ./payroll_dashboard ./main.py ./rxconfig.py

# Linting and formatting with ruff
lint:
	uv run ruff check ./payroll_dashboard ./main.py ./rxconfig.py
	uv run ruff check --select I ./payroll_dashboard ./main.py ./rxconfig.py

# Run all checks
check: format lint

.PHONY: install format lint check
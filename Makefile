# This tells make that these are commands, not files
.PHONY: install run test lint format typecheck check clean

install:
	uv sync --locked

run:
	uv run uvicorn app.main:app --reload

lint:
	uv run ruff check . --fix

format:
	uv run ruff format . --check

typecheck:
	uv run mypy app

unit:
	uv run pytest tests/unit

integration:
	uv run pytest tests/integration

coverage:
	uv run pytest --cov=app --cov-report=html

check: lint typecheck test

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

pre-commit:
	uv run pre-commit run --all-files
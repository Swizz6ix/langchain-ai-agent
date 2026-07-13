.PHONY: install run test lint format typecheck check clean \
        bandit pip-audit sbom licenses security

install:
	uv sync --locked --all-groups

run:
	uv run uvicorn app.main:app --reload

lint:
	uv run ruff check . --fix

format:
	uv run ruff format .

typecheck:
	uv run mypy app

unit:
	uv run pytest tests/unit

integration:
	uv run pytest tests/integration

coverage:
	uv run pytest --cov=app --cov-report=html



# Security

bandit:
	uv run bandit \
		-r app \
		-f json \
		-o bandit-report.json

pip-audit:
	uv run pip-audit \
		-f json \
		-o pip-audit-report.json

sbom:
	uv run cyclonedx-py environment \
		-o sbom.json

licenses:
	uv run pip-licenses \
		--format=markdown \
		--output-file licenses.md


security: bandit pip-audit sbom licenses


check:
	$(MAKE) lint
	$(MAKE) typecheck
	$(MAKE) unit
	$(MAKE) security


clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +


pre-commit:
	uv run pre-commit run --all-files
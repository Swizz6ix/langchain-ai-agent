.PHONY: install run test lint format typecheck check unit integration clean \
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
	uv run pytest --cov=app --cov-report=term-missing --cov-report=html



# Security

bandit:
# -lll: Only return a failing exit code (1) for Medium or High severity issues.
# The JSON report will still contain ALL findings (including Low/Info) for your records.
	uv run bandit \
		-r app \
		-lll \
		-f json \
		-o bandit-report.json

pip-audit:
# --desc on: provides descriptions of vulnerabilities.
# --strict: halts only on known, high-risk vulnerabilities, but you can also pass
# specific ignore arguments if you have unpatched, low-risk exceptions.
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


security:
	-$(MAKE) bandit
	-$(MAKE) pip-audit
	$(MAKE) sbom
	$(MAKE) licenses

# Utility and Quality Gates
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

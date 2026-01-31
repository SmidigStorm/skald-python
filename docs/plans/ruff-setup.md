# Configure Ruff

**Completed: 2026-01-31**

## Summary

Set up Ruff for linting and formatting Python code. Replaces need for flake8, isort, and Black with a single fast tool.

## Requirements

- [x] RUFF-001: Linting configured - `ruff check .` works
- [x] RUFF-002: Formatting configured - `ruff format .` works
- [x] RUFF-003: Django-compatible rules enabled
- [x] RUFF-004: Works in Docker

## Implementation Steps

### Step 1: Add ruff to requirements-dev.txt

### Step 2: Configure ruff in pyproject.toml

- Line length: 88 (Black default)
- Target: Python 3.12
- Enable: pyflakes (F), pycodestyle (E, W), isort (I), Django (DJ)
- Exclude: migrations, .venv, __pycache__

### Step 3: Run ruff format

Auto-format existing code.

### Step 4: Run ruff check

Verify no linting errors.

### Step 5: Rebuild Docker

Include ruff in container.

## Acceptance Criteria

- [x] `ruff check .` passes with no errors
- [x] `ruff format --check .` passes (code is formatted)
- [x] Django-specific rules work
- [x] Works in Docker container

# Initialize Django Project

**Completed: 2026-01-31**

## Summary

Set up a minimal Django 5.x project with PostgreSQL configuration, ready for development. Following YAGNI - no domain apps until needed.

## Requirements

- [x] SETUP-001: Django 5.x project created - `python manage.py runserver` works
- [x] SETUP-002: Project structure follows conventions - `skald_project/` config directory
- [x] SETUP-003: PostgreSQL configured - Settings support env-based PostgreSQL connection
- [x] SETUP-004: Settings organized - Single settings.py with environment variables
- [x] SETUP-005: Type hints enforced - pyproject.toml configured
- [x] SETUP-006: Basic dependencies installed - requirements.txt with core packages

## Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Project name | `skald_project` | Django convention with _project suffix |
| Dependencies | pip + requirements.txt | Simple, familiar, no extra tooling |
| Settings | Single file + env vars | Simpler than split settings, 12-factor app compliant |
| Python version | Mise (.mise.toml) | User already uses Mise for other projects |
| App scaffolding | Skip for now | YAGNI - create apps when needed |

## Implementation Steps

### Step 1: Create `.mise.toml`

Pin Python version for the project.

```toml
[tools]
python = "3.12"
```

### Step 2: Create `requirements.txt`

Core dependencies only.

```
Django>=5.0,<6.0
djangorestframework>=3.14,<4.0
psycopg[binary]>=3.1,<4.0
python-dotenv>=1.0,<2.0
```

### Step 3: Create `pyproject.toml`

Python project configuration with type hint settings.

```toml
[project]
name = "skald"
version = "0.1.0"
requires-python = ">=3.12"

[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "standard"
```

### Step 4: Run Django startproject

```bash
mise install
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
django-admin startproject skald_project .
```

This creates:
- `manage.py`
- `skald_project/settings.py`
- `skald_project/urls.py`
- `skald_project/wsgi.py`
- `skald_project/asgi.py`

### Step 5: Update `settings.py`

Modify for PostgreSQL and environment variables:

1. Add at top: `from dotenv import load_dotenv` and `load_dotenv()`
2. Update `SECRET_KEY` to read from env
3. Update `DEBUG` to read from env
4. Update `ALLOWED_HOSTS` to read from env
5. Replace SQLite with PostgreSQL:
   ```python
   DATABASES = {
       "default": {
           "ENGINE": "django.db.backends.postgresql",
           "NAME": os.getenv("DB_NAME", "skald"),
           "USER": os.getenv("DB_USER", "postgres"),
           "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
           "HOST": os.getenv("DB_HOST", "localhost"),
           "PORT": os.getenv("DB_PORT", "5432"),
       }
   }
   ```
6. Add `rest_framework` to `INSTALLED_APPS`

### Step 6: Create `.env.example`

Template for required environment variables.

```
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=skald
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### Step 7: Create `.gitignore`

Standard Python/Django ignores.

```
# Python
__pycache__/
*.py[cod]
.venv/
venv/
.env

# Django
*.log
local_settings.py
db.sqlite3

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
```

### Step 8: Verify

```bash
python manage.py check
```

Should output: `System check identified no issues.`

## Acceptance Criteria

- [x] `python manage.py check` passes
- [x] `python manage.py runserver` starts (may fail on DB connection - that's OK)
- [x] `.mise.toml` pins Python 3.12
- [x] `requirements.txt` contains Django, DRF, psycopg, python-dotenv
- [x] `settings.py` reads config from environment variables
- [x] `.env.example` documents required variables
- [x] `.gitignore` excludes venv, .env, __pycache__

## Files Created/Modified

| File | Action |
|------|--------|
| `.mise.toml` | Create |
| `requirements.txt` | Create |
| `pyproject.toml` | Create |
| `manage.py` | Create (via django-admin) |
| `skald_project/__init__.py` | Create (via django-admin) |
| `skald_project/settings.py` | Create then modify |
| `skald_project/urls.py` | Create (via django-admin) |
| `skald_project/wsgi.py` | Create (via django-admin) |
| `skald_project/asgi.py` | Create (via django-admin) |
| `.env.example` | Create |
| `.gitignore` | Create |

# Skald

AI-native product development platform.

## Development Setup

### Prerequisites

- Python 3.12+
- Docker (for PostgreSQL)

### 1. Start PostgreSQL

```bash
docker-compose up -d
```

### 2. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or: .venv\Scripts\activate  # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements-dev.txt
```

### 4. Configure environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create superuser

```bash
python manage.py createsuperuser
```

### 7. Run development server

```bash
python manage.py runserver
```

Visit http://localhost:8000/admin/

## Running Tests

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

Run specific test file:

```bash
pytest tests/user_access/test_user_login.py -v
```

## Project Structure

```
skald-python/
├── docs/                    # Documentation
│   ├── domains/             # Domain documentation & requirements
│   ├── plans/               # Implementation plans
│   └── strategy/            # Vision, architecture, tech stack
├── skald_project/           # Django project settings
├── users/                   # User Access domain app
├── tests/                   # Test files
│   └── user_access/         # User Access domain tests
└── requirements.txt         # Production dependencies
```

## Tech Stack

- Django 6.0
- PostgreSQL 18
- pytest-bdd for BDD testing

# Set up Docker + Compose

**Completed: 2026-01-31**

## Summary

Configure Docker and Docker Compose for local development with Python 3.12 and PostgreSQL containers. Enables `docker compose up` workflow.

## Requirements

- [x] DOCKER-001: Dockerfile for Django - Builds Python 3.12-slim image with dependencies
- [x] DOCKER-002: docker-compose.yml - Defines web + db services
- [x] DOCKER-003: PostgreSQL container - Database accessible to Django
- [x] DOCKER-004: Volume persistence - Database data survives container restart
- [x] DOCKER-005: Dev workflow works - `docker compose up` starts everything

## Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Base image | `python:3.12-slim` | Balance of size (~150MB) and compatibility |
| Auto-migrations | Yes | Simpler dev workflow |
| Port | 8000 | Standard Django dev port |
| Hot reload | Volume mount | Edit code locally, see changes immediately |

## Implementation Steps

### Step 1: Create `Dockerfile`

**Implements**: DOCKER-001

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Run entrypoint script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
```

### Step 2: Create `entrypoint.sh`

**Implements**: DOCKER-005

Script that:
1. Waits for PostgreSQL to be ready
2. Runs migrations
3. Starts the dev server

```bash
#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

echo "Running migrations..."
python manage.py migrate

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000
```

### Step 3: Create `docker-compose.yml`

**Implements**: DOCKER-002, DOCKER-003, DOCKER-004

```yaml
services:
  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: skald
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres

  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      DEBUG: "True"
      SECRET_KEY: "docker-dev-secret-key-change-in-prod"
      ALLOWED_HOSTS: "localhost,127.0.0.1"
      DB_NAME: skald
      DB_USER: postgres
      DB_PASSWORD: postgres
      DB_HOST: db
      DB_PORT: 5432
    depends_on:
      - db

volumes:
  postgres_data:
```

### Step 4: Create `.dockerignore`

Exclude unnecessary files from Docker context.

```
.venv/
venv/
__pycache__/
*.py[cod]
.git/
.gitignore
.env
*.md
docs/
```

### Step 5: Update `Dockerfile` for netcat

Add netcat to the image for the wait-for-db script.

```dockerfile
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*
```

### Step 6: Verify

```bash
docker compose up --build
```

Should see:
- PostgreSQL starting
- Django migrations running
- Server at http://localhost:8000

## Acceptance Criteria

- [x] `docker compose up` starts both containers
- [x] PostgreSQL is accessible from Django container
- [x] Migrations run automatically on startup
- [x] Django dev server accessible at http://localhost:8000
- [x] Code changes reflect immediately (volume mount)
- [x] Database data persists after `docker compose down`

## Files Created

| File | Purpose |
|------|---------|
| `Dockerfile` | Django container image |
| `docker-compose.yml` | Service orchestration |
| `entrypoint.sh` | Startup script |
| `.dockerignore` | Exclude files from build |

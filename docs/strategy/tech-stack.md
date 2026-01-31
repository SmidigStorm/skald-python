# Tech Stack

## Core

| Layer | Choice | Notes |
|-------|--------|-------|
| **Language** | Python 3.12+ | Type hints everywhere |
| **Framework** | Django 5.x | Batteries included, good for AI-assisted development |
| **API** | Django REST Framework | REST APIs alongside templates |
| **Database** | PostgreSQL | Robust, handles complex domain models |
| **Containerization** | Docker | Kubernetes deployment target |

## Django Built-ins We'll Use

- **Admin** - Free CRUD UI for all domain entities
- **Auth** - Users, permissions (User Access domain)
- **ORM** - Models with migrations
- **Templates** - Server-rendered HTML for basic UI

## Additional Libraries

| Library | Purpose |
|---------|---------|
| **django-rest-framework** | REST API endpoints |
| **python-gitlab** | GitLab API integration (trigger tests, fetch results) |
| **markdown** | Render wiki content in Domain Knowledge |
| **pytest + pytest-django** | Testing |
| **pytest-bdd** | BDD test runner |

## Future Additions (when needed)

| Need | Likely Choice |
|------|---------------|
| Rich interactivity | HTMX (no JS framework needed) |
| Data visualization | Plotly or Chart.js |
| Diagrams | Mermaid.js |
| AI integration | Anthropic SDK |
| Background jobs | Django-Q2 or Celery |

## Dev Setup

```bash
# With Docker
docker compose up

# Or locally
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Deployment

- **Target**: Kubernetes
- **Container**: Docker
- **Database**: PostgreSQL (managed service recommended)

## Why Django?

1. **Admin panel** - Instant UI for iterating on domain models
2. **Built-in auth** - User Access domain gets a head start
3. **Opinionated** - Fits our "opinionated over flexible" principle
4. **AI-friendly** - Clear conventions, well-documented, easy to vibe-code
5. **Mature ecosystem** - Libraries for everything we need

# Skald

Skald is an AI-native product development platform. It guides teams through a best-practice workflow from strategy to tested code.

## Tech Stack

- **Django 6.x** + Django REST Framework
- **PostgreSQL 18** database
- **Docker** (Postgres only for dev, Kubernetes for prod)
- **pytest-bdd** for BDD testing

See `docs/strategy/tech-stack.md` for details.

## Local Development

### Docker Strategy

Docker is used **only for PostgreSQL** in development. Django runs locally in a venv.

```bash
docker-compose up -d    # Start Postgres
source .venv/bin/activate
python manage.py runserver
```

### Naming Conventions

| Resource | Name | Notes |
|----------|------|-------|
| Docker Compose service | `db` | Postgres service |
| Container name | `skald-python-db-1` | Auto-generated |
| Database name | `skald` | Dev database |
| Database user | `postgres` | Default user |
| Database password | `postgres` | Dev only |
| Port | `5432` | Default Postgres port |

### Environment Variables

Configured in `.env` (copy from `.env.example`):

```
DB_NAME=skald
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

## Project Structure

```
docs/
├── strategy/
│   ├── vision.md              # Product vision
│   ├── tech-stack.md          # Technology choices
│   └── architecture/          # ADRs (001-*.md)
└── domains/
    ├── _overview.md           # Domain relationships
    ├── domain-knowledge/      # Entities, glossary, ubiquitous language
    ├── requirements/          # BDD: Requirements, Rules, Examples
    ├── user-access/           # Users, Products, Roles (multi-tenancy)
    ├── insights/              # Atomic UX: Experiments, Facts, Insights
    ├── strategy/              # OKRs: Objectives, Key Results
    ├── planning/              # Backlog, Sprints, Releases, Teams
    ├── architecture/          # ADRs, Technologies
    └── testing/               # Tests, TestRuns, TestResults
```

## Core Concepts

### Multi-tenancy
**Product** is the tenant boundary. All data is scoped to a product.

### Domain Hierarchy
```
Product → Domain → SubDomain → Capability → Requirement → Example
```

### Core Flow
```
Strategy → Domain Knowledge → Requirements → Planning → Code → Testing
```

### Key Entities by Domain

| Domain | Key Entities |
|--------|--------------|
| User Access | User, Product, ProductMembership, Role |
| Domain Knowledge | Domain, SubDomain, Capability, Entity, GlossaryTerm |
| Requirements | Requirement, Rule, Example, OpenQuestion, Answer |
| Insights | Experiment, Fact, Insight, Recommendation |
| Strategy | StrategicPillar, TimeHorizon, Objective, KeyResult |
| Planning | BacklogItem, Sprint, Release, Team |
| Architecture | ADR, Technology |
| Testing | Test, TestSuite, TestRun, TestResult |

## Methodology

| Area | Approach |
|------|----------|
| Requirements | BDD, Example Mapping, Gherkin scenarios |
| Domain modeling | Domain-Driven Design |
| User research | Atomic UX Research |
| Architecture | ADRs (Architecture Decision Records) |
| Testing | Acceptance tests tied to Examples |

## Documentation

- **Vision**: `docs/strategy/vision.md`
- **Domain models**: `docs/domains/*/entities/_overview.md`
- **ADRs**: `docs/strategy/architecture/`
- **Tech stack**: `docs/strategy/tech-stack.md`

## Product Principles

1. **Opinionated over flexible** - Guide users through best practices
2. **Executable specs, not documentation** - Requirements run as tests
3. **Domain language everywhere** - Ubiquitous language in UI, specs, and code

## Development Practices

### Code Style
- **Type hints everywhere** - Helps catch errors and clarifies intent
- **Ruff** for linting and formatting
- **Explicit over clever** - Clear code beats smart code

### Django Architecture

```
View → Model → Database
```

- **Fat models** - Business logic lives in models
- **Thin views** - HTTP handling only, call model methods
- **Templates** - Display only, no logic
- **One Django app per domain** - Clear boundaries

```
apps/
├── users/           # User Access domain
├── knowledge/       # Domain Knowledge domain
├── requirements/    # Requirements domain
├── insights/        # Insights domain
├── strategy/        # Strategy domain
├── planning/        # Planning domain
├── architecture/    # Architecture domain
├── testing/         # Testing domain
└── core/            # Shared utilities
```

### Key Principles

| Principle | Practice |
|-----------|----------|
| **DRY** | Don't repeat, but don't abstract too early (rule of 3) |
| **Explicit** | Pass dependencies, avoid magic |
| **Fail fast** | Validate early, clear error messages |
| **Single responsibility** | One reason to change per class |

### Testing

- **Unit tests** for model methods
- **API tests** for endpoints
- **pytest-bdd** for acceptance tests (tied to Examples)

### Avoid

- Logic in views or templates
- Magic strings (use constants/enums)
- N+1 queries (use `select_related`, `prefetch_related`)

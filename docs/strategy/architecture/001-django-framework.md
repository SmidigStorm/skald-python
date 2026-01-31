# 1. Use Django as the Web Framework

**Status**: accepted

## Context

Skald is an AI-native product development platform that needs:
- REST APIs for external integrations (MCP, GitLab)
- Basic web UI for managing domain entities
- User authentication and authorization
- Wiki-like features for Domain Knowledge
- Quick iteration on domain models

We considered FastAPI (lightweight, async, great API docs) vs Django (batteries included, admin panel, built-in auth).

## Decision

Use Django 5.x with Django REST Framework.

## Consequences

**Positive:**
- Admin panel provides free CRUD UI while iterating on domain models
- Built-in auth system accelerates User Access domain
- Opinionated conventions align with our "opinionated over flexible" principle
- Well-documented framework is AI-friendly for assisted development
- Mature ecosystem with libraries for all our needs (GitLab, Markdown, etc.)
- Templates + HTMX gives basic UI without frontend build tooling

**Negative:**
- Heavier than FastAPI
- Async support is partial (improving in Django 5.x)
- More conventions to learn
- API documentation not as automatic as FastAPI (need drf-spectacular)

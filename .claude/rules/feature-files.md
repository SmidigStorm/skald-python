---
paths:
  - "**/*.feature"
---

# Feature File Conventions

## Location

Feature files live inside each domain's requirements folder with a **flat structure**:

```
docs/domains/<domain>/requirements/<feature-name>.feature
```

Examples:
- `docs/domains/user-access/requirements/user-login.feature`
- `docs/domains/user-access/requirements/user-management.feature`
- `docs/domains/planning/requirements/backlog-prioritization.feature`

## Feature ID Format

**Skip feature IDs for now.** We may add them later using format `@DOM-NNN`.

## Tags

**Skip tags for now.** We may add priority/status tags later:
- Priority: `@must` / `@should` / `@could` / `@wont`
- Status: `@implemented` / `@in-progress` / `@planned`

## Actors

- system administrator
- product manager
- product contributor
- product viewer
- unauthenticated user

## Open Questions

Document uncertainties as comments after the feature description:

```gherkin
Feature: UAC-001 User Login
  As an unauthenticated user
  I want to log in
  So that I can access the system.

  # OPEN QUESTIONS:
  # - Should we add rate limiting?

  Rule: ...
```

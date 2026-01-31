# Skald Domain Overview

Skald is an AI-native product development platform. This document provides an overview of all domains and their relationships.

## Domains

| Domain | Purpose | Status |
|--------|---------|--------|
| [Domain Knowledge](domain-knowledge/entities/_overview.md) | Entities, relationships, ubiquitous language, documentation | ✓ Documented |
| [Requirements](requirements/entities/_overview.md) | BDD features, scenarios, executable specs | ✓ Documented |
| [User Access](user-access/entities/_overview.md) | Multi-tenancy, users, products, roles | ✓ Documented |
| [Insights](insights/entities/_overview.md) | User research, Atomic UX observations | Pending |
| [Planning](planning/entities/_overview.md) | Releases, Backlog Items, Plans | Pending |
| [Architecture](architecture/entities/_overview.md) | ADRs, tech stack, system design decisions | Pending |
| [Testing](testing/entities/_overview.md) | E2E tests tied to specifications | Pending |

## Cross-Domain Relationships

```mermaid
erDiagram
    Product ||--o{ Domain : "has"
    Domain ||--o{ SubDomain : "has"
    SubDomain ||--o{ Capability : "has"
    Capability ||--o{ Requirement : "has"
    Requirement }o--|| BacklogItem : "solved by"
    Example ||--o{ TestCase : "automated as"
    Product ||--o{ User : "has members"
```

## Core Flow

```
Domain Knowledge → Requirements → Planning → Code → Testing
```

1. **Domain Knowledge** - Define the domain model (entities, capabilities, glossary)
2. **Requirements** - Specify what capabilities need (rules, examples)
3. **Planning** - Prioritize and plan work (backlog items, releases)
4. **Code** - Implement (external to Skald)
5. **Testing** - Verify examples pass (E2E tests)

## Shared Entities

Some entities are shared across domains:

| Entity | Primary Domain | Also Used In |
|--------|---------------|--------------|
| Product | User Access | Domain Knowledge (tenant boundary) |
| Capability | Domain Knowledge | Requirements (contains requirements) |
| Example | Requirements | Testing (executed as tests) |
| Backlog Item | Planning | Requirements (solves requirements) |

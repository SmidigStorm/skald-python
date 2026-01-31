# Technology

A technology used in the product's tech stack.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | Technology name (e.g., "FastAPI") |
| category | enum | yes | Type of technology |
| version | string | no | Version in use |

## Category Values

| Category | Examples |
|----------|----------|
| frontend | React, Vue, Angular |
| backend | FastAPI, Django, Express |
| database | PostgreSQL, MongoDB, Redis |
| infrastructure | Docker, Kubernetes, AWS |
| testing | Playwright, pytest, Jest |
| other | Miscellaneous |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Product | N:1 | The product using this technology |
| decided by | ADR | N:0..1 | The ADR that chose this technology |

## Notes

- Category list is not exhaustive - "other" catches edge cases
- Version is optional but useful for tracking upgrades
- Link to ADR explains "why" this technology was chosen

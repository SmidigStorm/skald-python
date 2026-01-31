# TimeHorizon

A user-defined time period for scoping objectives. Examples: "Q1 2026", "Annual 2026", "H1 2026".

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | Period name (e.g., "Q1 2026") |
| start_date | date | yes | When the period begins |
| end_date | date | yes | When the period ends |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Product | N:1 | The product this horizon is for |
| contains | Objective | 1:N | Objectives within this time period |

## Notes

- User-defined - not restricted to quarters or years
- Provides time-boxing for OKRs
- Multiple horizons can exist per product (e.g., quarterly + annual)

# Sprint

A time-boxed iteration for planning and executing work. Sprints are shared across all teams within a product.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | Sprint name (e.g., "Sprint 1", "Week 12") |
| start_date | date | yes | When the sprint begins |
| end_date | date | yes | When the sprint ends |
| goal | string | no | What the sprint aims to achieve |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Product | N:1 | The product this sprint is for |
| contains | BacklogItem | 1:N | Items planned for this sprint |

## Notes

- Sprints are shared across teams - all teams work within the same sprint cadence
- Each team pulls their owned items into the sprint
- Sprint and Release are independent - items in a sprint can go to different releases

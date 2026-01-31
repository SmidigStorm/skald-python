# BacklogItem

Something we've decided to do. BacklogItems live in the ordered product backlog and are assigned to teams for execution.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| title | string | yes | Short description of the work |
| description | string | no | Detailed description |
| position | integer | yes | Order in the product backlog (lower = higher priority) |
| status | enum | yes | Todo, In Progress, Done |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Product | N:1 | The product this item is in |
| owned by | Team | N:1 | The team responsible for this work |
| planned into | Sprint | N:0..1 | The sprint this is planned for |
| connected to | Release | N:0..1 | The release this ships in |
| implements | Requirement | N:N | Requirements this item fulfills |
| contributes to | [Objective](../../strategy/entities/objective.md) | N:0..1 | Optional link to strategic objective |

## Status Values

| Status | Description |
|--------|-------------|
| Todo | Not started |
| In Progress | Work has begun |
| Done | Completed |

## Notes

- Position determines priority within the product backlog
- A "team view" filters the backlog by team ownership
- An item can exist without being in a sprint (backlog) or release (not yet planned for shipping)

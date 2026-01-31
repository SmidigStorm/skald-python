# Release

A version or milestone that ships to users. Releases are independent of sprints.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | Release name (e.g., "v1.0", "MVP", "Q1 2024") |
| description | string | no | What this release includes |
| target_date | date | no | When we aim to ship |
| status | enum | yes | Planned, In Progress, Released |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Product | N:1 | The product this release is for |
| contains | BacklogItem | 1:N | Items shipping in this release |

## Status Values

| Status | Description |
|--------|-------------|
| Planned | Release is defined but work hasn't started |
| In Progress | Work is ongoing |
| Released | Shipped to users |

## Notes

- A release can contain items from multiple sprints
- A sprint can have items going to different releases
- target_date is optional - useful for roadmap planning

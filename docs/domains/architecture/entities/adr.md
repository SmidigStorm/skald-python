# ADR (Architecture Decision Record)

A record of a significant technical decision. Follows the standard ADR format.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| title | string | yes | Short description of the decision |
| status | enum | yes | Current status |
| context | string | yes | Why this decision is needed |
| decision | string | yes | What was decided |
| consequences | string | yes | Impact of the decision (positive and negative) |

## Status Values

| Status | Description |
|--------|-------------|
| Proposed | Under discussion |
| Accepted | Decision made and active |
| Deprecated | No longer recommended |
| Superseded | Replaced by another ADR |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Product | N:1 | The product this decision is for |
| superseded by | ADR | N:0..1 | The ADR that replaces this one |
| decides | Technology | 1:N | Technologies chosen by this decision |

## Notes

- ADRs are immutable once accepted - create a new ADR to change a decision
- Use "Superseded" status when a new ADR replaces an old one
- Context should explain the forces at play, not just the problem

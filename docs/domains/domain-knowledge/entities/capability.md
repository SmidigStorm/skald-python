# Capability

What the system can do. Capabilities are verb-like and describe actions or behaviors at the sub-domain level.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | Capability name (verb-like, e.g., "Process Payment") |
| description | string | no | What this capability does |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | SubDomain | N:1 | A capability belongs to one sub-domain |

## Examples

- "Process Payment"
- "Generate Invoice"
- "Validate Order"
- "Send Notification"

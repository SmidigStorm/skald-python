# Domain

A top-level area of concern within a product. Domains group related sub-domains together.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | Domain name |
| description | string | no | Domain description |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Product | N:1 | A domain belongs to one product |
| contains | SubDomain | 1:N | A domain contains multiple sub-domains |

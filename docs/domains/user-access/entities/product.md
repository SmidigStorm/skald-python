# Product

The tenant boundary in Skald. Each product has its own isolated data - domain model, requirements, backlog, etc.

> **Note:** Product is shared with the [Domain Knowledge](../../domain-knowledge/entities/product.md) domain where it owns the domain model hierarchy.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | Product name |
| description | string | no | Product description |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| has | ProductMembership | 1:N | Users who have access to this product |
| contains | [Domain](../../domain-knowledge/entities/domain.md) | 1:N | Domain model hierarchy |

## Multi-tenancy

- All data is scoped to a product
- Users only see data for products they are members of
- Products share the same database but data is isolated

# Product

The tenant boundary in Skald. Each product has its own isolated domain model.

> **Note:** Product is shared with the [User Access](../../user-access/entities/product.md) domain where it serves as the multi-tenancy boundary.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | Product name |
| description | string | no | Product description |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| contains | Domain | 1:N | A product contains multiple domains |

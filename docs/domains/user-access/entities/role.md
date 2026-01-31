# Role

A permission level that determines what a user can do. Roles can be global or per-product.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | Role name |
| scope | enum | yes | global, per-product |

## Defined Roles

| Role | Scope | Permissions |
|------|-------|-------------|
| System Administrator | global | Manage all products and users |
| Product Manager | per-product | Full control of one product |
| Product Contributor | per-product | Edit access, not admin |
| Product Viewer | per-product | Read-only access |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| assigned to | User | 1:N | Global role assignment |
| assigned via | ProductMembership | 1:N | Per-product role assignments |

## Notes

- Only System Administrator is a global role
- Per-product roles are assigned via ProductMembership
- Detailed permissions to be defined during architecture discussions

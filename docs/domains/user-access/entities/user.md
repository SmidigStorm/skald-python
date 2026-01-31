# User

A person who uses Skald. Users authenticate with email/password and are assigned roles per-product.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | User's display name |
| email | string | yes | Email address (unique, used for login) |
| password | string | yes | Hashed password |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| has | ProductMembership | 1:N | User's product memberships |
| has | Role | 0:1 | Global role (System Administrator) |

## Notes

- Authentication is built-in (email/password)
- A user can be a member of multiple products with different roles
- System Administrator is a global role, not tied to any product

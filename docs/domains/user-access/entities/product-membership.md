# ProductMembership

Links a user to a product with a specific role. This is how per-product authorization is managed.

## Attributes

None beyond the relationships.

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | User | N:1 | The user |
| belongs to | Product | N:1 | The product |
| assigned | Role | N:1 | The role for this user on this product |

## Notes

- A user can have different roles on different products
- Example: Alice is Product Manager on "App A" but Viewer on "App B"

# TeamMembership

Links a user to a team. Flat membership with no roles within the team.

## Attributes

None beyond the relationships.

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Team | N:1 | The team |
| belongs to | User | N:1 | The user |

## Notes

- A user can be a member of multiple teams
- No hierarchy or roles within team - just membership

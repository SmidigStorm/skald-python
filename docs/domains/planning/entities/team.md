# Team

A group of users who work together on backlog items. Teams are per-product.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | Team name |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Product | N:1 | The product this team works on |
| has | TeamMembership | 1:N | Team members |
| owns | BacklogItem | 1:N | Items this team is responsible for |

## Notes

- Team is a Planning concept - it organizes who does what work
- Membership is flat (no roles within the team)
- A user can be on multiple teams (within same or different products)

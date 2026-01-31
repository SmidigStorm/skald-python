# Insight

A pattern identified across multiple facts. The "aha" moment from research.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| description | string | yes | The pattern (e.g., "Users expect immediate feedback after submitting forms") |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Product | N:1 | The product this insight is about |
| supported by | Fact | N:N | Facts that support this insight |
| leads to | Recommendation | 1:N | Actions based on this insight |

## Notes

- Insights emerge from patterns across facts
- An insight should be supported by multiple facts
- Insights inform recommendations

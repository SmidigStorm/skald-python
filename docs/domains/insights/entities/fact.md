# Fact

An observation from an experiment. A specific thing that was seen or heard.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| description | string | yes | The observation (e.g., "User clicked X expecting Y to happen") |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Experiment | N:1 | The experiment this came from |
| contributes to | Insight | N:N | Insights this fact supports |

## Notes

- Facts are atomic - one observation per fact
- Multiple facts can contribute to the same insight
- A fact can contribute to multiple insights

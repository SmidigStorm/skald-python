# Recommendation

An action proposed based on insights. The bridge from research to product work.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| description | string | yes | The proposed action |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Product | N:1 | The product this is for |
| based on | Insight | N:N | Insights that led to this recommendation |
| becomes | BacklogItem | 1:0..1 | Optional: work item created from this |
| becomes | Requirement | 1:0..1 | Optional: requirement created from this |

## Notes

- Recommendations are actionable
- Can become a BacklogItem (tactical work) or Requirement (capability spec)
- Not all recommendations become work items immediately

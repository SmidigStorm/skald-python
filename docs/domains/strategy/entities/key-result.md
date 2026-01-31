# KeyResult

A measurable outcome for an objective. The "KR" in OKR. Key Results define how you measure success.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| description | string | yes | What is being measured (e.g., "Increase signup conversion rate") |
| target_value | number | yes | The goal to reach |
| current_value | number | yes | Current progress |
| unit | string | yes | Unit of measurement (e.g., "%", "users", "seconds") |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Objective | N:1 | The objective this measures |

## Examples

| Description | Current | Target | Unit |
|-------------|---------|--------|------|
| Increase signup conversion rate | 12 | 25 | % |
| Reduce page load time | 3.2 | 1.5 | seconds |
| Grow monthly active users | 1000 | 5000 | users |

## Notes

- Key Results are specific and measurable
- Progress is tracked via current_value vs target_value
- Each Objective should have 2-5 Key Results

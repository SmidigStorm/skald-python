# Objective

A qualitative goal within a time horizon. The "O" in OKR. Objectives describe what you want to achieve.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| title | string | yes | The objective (e.g., "Improve user onboarding experience") |
| description | string | no | Context and details |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | TimeHorizon | N:1 | The time period this objective is for |
| has | KeyResult | 1:N | Measurable outcomes for this objective |
| contributed to by | BacklogItem | N:N | Work items that help achieve this |

## Notes

- Objectives are qualitative - they describe direction, not metrics
- Key Results provide the measurable outcomes
- BacklogItems can optionally link to Objectives to show contribution

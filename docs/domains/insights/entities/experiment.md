# Experiment

A research study or session. The container for facts/observations.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | Experiment name |
| description | string | no | What was studied and why |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Product | N:1 | The product being researched |
| produces | Fact | 1:N | Observations from this experiment |

## Notes

- Source type (interview, usability test, etc.) not modeled for now
- An experiment can produce many facts

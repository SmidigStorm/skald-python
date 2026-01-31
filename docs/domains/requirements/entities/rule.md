# Rule

A business rule that governs a requirement. Rules express the logic and constraints that the system must follow. Inspired by Gherkin 6 `Rule:` keyword.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | Rule name |
| description | string | no | Detailed explanation of the business rule |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Requirement | N:1 | A rule belongs to one requirement |
| has | Example | 1:N | Scenarios that illustrate this rule |

## Example

For requirement "User Login":

```gherkin
Rule: Users must provide valid credentials

Rule: Account locks after 3 failed attempts

Rule: Session expires after 30 minutes of inactivity
```

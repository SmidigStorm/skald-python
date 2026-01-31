# OpenQuestion

An unresolved ambiguity or uncertainty about a requirement. Open questions are captured during Example Mapping sessions and must be answered before implementation.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| text | string | yes | The question |
| status | enum | yes | open, answered |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Requirement | N:1 | A question belongs to one requirement |
| has | Answer | 1:N | Answers to this question |

## Example

For requirement "User Login":

```markdown
**Question:** What happens if the user's account is locked?
**Status:** open

**Question:** Should we support "remember me" functionality?
**Status:** answered
```

# Answer

A resolution to an open question. When a question is answered, the answer may lead to new rules or examples being added to the requirement.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| text | string | yes | The answer |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | OpenQuestion | N:1 | An answer belongs to one question |

## Example

```markdown
**Question:** Should we support "remember me" functionality?
**Answer:** Yes, but only for 7 days maximum. Add a new rule for this.
```

When an answer is provided:
1. Mark the question status as `answered`
2. Consider adding new Rules or Examples based on the answer

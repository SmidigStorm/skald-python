# TestSuite

A group of related tests. Scope and grouping criteria to be determined.

> **TBD:** This entity needs refinement after discovery session.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | Suite name |
| description | string | no | What this suite covers |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Product | N:1 | The product this suite is for |
| contains | Test | 1:N | Tests in this suite |

## Open Questions

- What defines a suite? Per Capability? Per Requirement? User-defined?
- Can a Test belong to multiple suites?
- Are suites hierarchical?

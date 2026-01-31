# TestRun

One execution of tests. Can be triggered manually or by CI.

> **TBD:** Attributes to be refined after discovery session.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| timestamp | datetime | yes | When the run started |
| trigger | enum | yes | manual, ci |
| status | enum | yes | running, completed, failed |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Product | N:1 | The product being tested |
| produces | TestResult | 1:N | Results for each test |

## Open Questions

- Environment info? (browser, OS, staging vs prod)
- Duration tracking?
- Link to CI job/pipeline?
- Which tests were included? (all, suite, selection)

# TestResult

The outcome of a single test within a test run.

> **TBD:** Details to be refined after discovery session.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| status | enum | yes | passed, failed, skipped |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | TestRun | N:1 | The run this result is from |
| for | Test | N:1 | The test that was executed |

## Open Questions

- Error message / stack trace?
- Duration?
- Screenshots / video?
- Logs?
- Retry attempts?

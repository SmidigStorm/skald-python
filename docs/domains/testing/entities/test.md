# Test

An executable acceptance test linked 1:1 to an Example. Typically a Playwright test file or similar.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| file_path | string | yes | Path to the test file |
| status | enum | yes | Current status |

## Status Values

| Status | Description |
|--------|-------------|
| Pending | Test not yet implemented |
| Passing | Last run passed |
| Failing | Last run failed |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| automates | Example | 1:1 | The Example this test verifies |
| belongs to | TestSuite | N:0..1 | Optional suite grouping |
| has | TestResult | 1:N | Results from test runs |

## Notes

- 1:1 with Example - each Example has exactly one Test
- file_path points to the actual test implementation (e.g., `tests/e2e/login.spec.ts`)
- Status reflects the most recent TestResult

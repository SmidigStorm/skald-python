# Example

A Gherkin scenario that illustrates a rule. Examples are executable specifications - they define expected behavior and can be automated as tests.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | Scenario name |
| gherkin | string | yes | Given/When/Then steps |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Rule | N:1 | An example belongs to one rule |

## Test Status

Examples have execution status managed by the **Testing** domain:
- `pending` - not yet automated
- `automated` - test exists
- `passing` - test passes
- `failing` - test fails

## Example

```gherkin
Rule: Users must provide valid credentials

  Scenario: Successful login with valid credentials
    Given a user "alice" with password "secret123"
    When they submit the login form with "alice" and "secret123"
    Then they should be redirected to the dashboard
    And a session should be created

  Scenario: Failed login with wrong password
    Given a user "alice" with password "secret123"
    When they submit the login form with "alice" and "wrongpass"
    Then they should see "Invalid credentials"
    And no session should be created
```

# Set up pytest + pytest-bdd

**Completed: 2026-01-31**

## Summary

Configure testing infrastructure with pytest for unit/integration tests and pytest-bdd for executable Gherkin specifications. Feature files live alongside domain documentation, enabling "executable specs, not documentation."

## Requirements

- [x] TEST-001: pytest configured - `pytest` runs and discovers tests
- [x] TEST-002: pytest-django integrated - Can test Django models, views, API
- [x] TEST-003: pytest-bdd configured - Gherkin .feature files execute as tests
- [x] TEST-004: Feature files in docs/domains/ - BDD tests live alongside requirements
- [x] TEST-005: Works in Docker - `docker-compose exec web pytest` runs tests

## Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Feature file location | `docs/domains/*/features/` | Specs live with domain documentation |
| Step definitions | `tests/steps/` | Centralized, reusable across domains |
| Test dependencies | `requirements-dev.txt` | Separate from production deps |

## Implementation Steps

### Step 1: Create `requirements-dev.txt`

Test dependencies only.

```
-r requirements.txt
pytest>=8.0,<9.0
pytest-django>=4.5,<5.0
pytest-bdd>=7.0,<8.0
```

### Step 2: Configure pytest in `pyproject.toml`

Add pytest configuration.

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "skald_project.settings"
python_files = ["test_*.py", "*_test.py"]
testpaths = ["tests"]
bdd_features_base_dir = "docs/domains/"
```

### Step 3: Create `tests/` directory structure

```
tests/
├── __init__.py
├── conftest.py           # Shared fixtures
└── steps/
    └── __init__.py
```

**conftest.py** contents:
```python
import pytest

pytest_plugins = ["pytest_bdd"]

@pytest.fixture
def api_client():
    """DRF API client for testing endpoints."""
    from rest_framework.test import APIClient
    return APIClient()
```

### Step 4: Create example feature + step definitions

**docs/domains/testing/features/health_check.feature**:
```gherkin
Feature: Health Check
  As a developer
  I want to verify the application is running
  So that I can confirm the test setup works

  Scenario: Application responds to health check
    Given the application is running
    When I request the admin login page
    Then I receive a successful response
```

**tests/steps/test_health_check.py**:
```python
import pytest
from pytest_bdd import scenario, given, when, then

@scenario("../../docs/domains/testing/features/health_check.feature", "Application responds to health check")
def test_health_check():
    pass

@given("the application is running")
def app_running():
    pass

@when("I request the admin login page")
def request_admin(client):
    return client.get("/admin/login/")

@then("I receive a successful response")
def check_response(request_admin):
    assert request_admin.status_code == 200
```

### Step 5: Update Dockerfile for test support

Modify Dockerfile to optionally install dev dependencies.

Create a build arg or just install dev deps in the dev image (docker-compose handles this).

Update `docker-compose.yml` to use dev requirements:
```yaml
web:
  build:
    context: .
    dockerfile: Dockerfile
  # ... existing config
```

Update `Dockerfile`:
```dockerfile
# After COPY requirements.txt
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt
```

### Step 6: Verify

```bash
# Local (with venv)
pytest

# Docker
docker-compose exec web pytest
```

Expected output:
```
tests/steps/test_health_check.py .                                    [100%]
1 passed
```

## Acceptance Criteria

- [x] `pytest` discovers and runs tests
- [x] `pytest --collect-only` shows BDD scenarios
- [x] Feature files in `docs/domains/*/features/` are found
- [x] Step definitions in `tests/steps/` work
- [x] `docker-compose exec web pytest` passes
- [x] Example health check test passes

## Directory Structure After Implementation

```
skald-python/
├── requirements.txt          # Production deps
├── requirements-dev.txt      # Test deps (includes prod)
├── pyproject.toml            # pytest config added
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── steps/
│       ├── __init__.py
│       └── test_health_check.py
└── docs/
    └── domains/
        └── testing/
            └── features/
                └── health_check.feature
```

## Files Created/Modified

| File | Action |
|------|--------|
| `requirements-dev.txt` | Create |
| `pyproject.toml` | Modify (add pytest config) |
| `tests/__init__.py` | Create |
| `tests/conftest.py` | Create |
| `tests/steps/__init__.py` | Create |
| `tests/steps/test_health_check.py` | Create |
| `docs/domains/testing/features/health_check.feature` | Create |
| `Dockerfile` | Modify (install dev deps) |

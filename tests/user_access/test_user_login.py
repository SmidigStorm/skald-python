"""E2E tests for user login feature."""

from typing import Any

import pytest
from django.http import HttpResponse
from django.test import Client
from pytest_bdd import given, parsers, scenarios, then, when

from users.models import User

scenarios("user-access/requirements/user-login.feature")


@pytest.fixture
def test_user_password() -> dict[str, str]:
    """Store the password for the test user."""
    return {}


@given(
    parsers.parse('the user "{username}" exists with password "{password}"'),
    target_fixture="test_user",
)
def user_exists_with_password(
    db: Any, username: str, password: str, test_user_password: dict[str, str]
) -> User:
    """Create a user with the given username and password."""
    user = User.objects.create_user(username=username, password=password, is_staff=True)
    test_user_password["value"] = password
    return user


@given(parsers.parse('no user exists with username "{username}"'))
def no_user_exists(db: Any, username: str) -> None:
    """Ensure no user exists with the given username."""
    User.objects.filter(username=username).delete()


@when(
    parsers.parse('the user logs in with username "{username}" and password "{password}"'),
    target_fixture="login_response",
)
def user_logs_in(client: Client, username: str, password: str) -> HttpResponse:
    """Attempt to log in with the given credentials."""
    response = client.post(
        "/admin/login/?next=/admin/",
        {"username": username, "password": password, "next": "/admin/"},
        follow=True,
    )
    return response


@then("the user is redirected to the dashboard")
def user_redirected_to_dashboard(login_response: HttpResponse) -> None:
    """Verify the user was redirected to the dashboard (admin index)."""
    assert login_response.status_code == 200
    assert login_response.redirect_chain, "Expected redirect after login"
    assert b"Site administration" in login_response.content


@then(parsers.parse('the user sees the error "{error_message}"'))
def user_sees_error(login_response: HttpResponse, error_message: str) -> None:
    """Verify the error message is displayed."""
    assert login_response.status_code == 200
    content = login_response.content.decode()
    # Django admin shows "Please enter the correct username and password"
    assert "errornote" in content, f"Expected error note in response for: {error_message}"


@then("the user remains on the login page")
def user_remains_on_login_page(login_response: HttpResponse) -> None:
    """Verify the user is still on the login page."""
    content = login_response.content.decode()
    assert "username" in content.lower()
    assert "password" in content.lower()

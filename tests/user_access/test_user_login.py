"""E2E tests for user login feature."""

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from users.models import User

scenarios("user-access/requirements/user-login.feature")


@pytest.fixture
def test_user_password():
    """Store the password for the test user."""
    return {}


@given(
    parsers.parse('the user "{username}" exists with password "{password}"'),
    target_fixture="test_user",
)
def user_exists_with_password(db, username, password, test_user_password):
    """Create a user with the given username and password."""
    user = User.objects.create_user(username=username, password=password, is_staff=True)
    test_user_password["value"] = password
    return user


@given(parsers.parse('no user exists with username "{username}"'))
def no_user_exists(db, username):
    """Ensure no user exists with the given username."""
    User.objects.filter(username=username).delete()


@when(
    parsers.parse('the user logs in with username "{username}" and password "{password}"'),
    target_fixture="login_response",
)
def user_logs_in(client, username, password):
    """Attempt to log in with the given credentials."""
    response = client.post(
        "/admin/login/?next=/admin/",
        {"username": username, "password": password, "next": "/admin/"},
        follow=True,
    )
    return response


@then("the user is redirected to the dashboard")
def user_redirected_to_dashboard(login_response):
    """Verify the user was redirected to the dashboard (admin index)."""
    assert login_response.status_code == 200
    # After successful login to admin, user lands on admin index
    assert b"Site administration" in login_response.content or login_response.redirect_chain


@then(parsers.parse('the user sees the error "{error_message}"'))
def user_sees_error(login_response, error_message):
    """Verify the error message is displayed."""
    # Django admin shows login errors in the page content
    assert login_response.status_code == 200
    # Check for error indication (Django admin uses specific error classes)
    content = login_response.content.decode()
    assert "errornote" in content or "error" in content.lower()


@then("the user remains on the login page")
def user_remains_on_login_page(login_response):
    """Verify the user is still on the login page."""
    content = login_response.content.decode()
    # Login page has a login form
    assert "username" in content.lower()
    assert "password" in content.lower()

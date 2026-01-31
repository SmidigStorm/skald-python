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
    user = User.objects.create_user(username=username, password=password)
    test_user_password["value"] = password
    return user


@given(parsers.parse('no user exists with username "{username}"'))
def no_user_exists(db: Any, username: str) -> None:
    """Ensure no user exists with the given username."""
    User.objects.filter(username=username).delete()


@given("I am not logged in")
def not_logged_in(client: Client, db: Any) -> None:
    """Ensure user is logged out."""
    client.logout()


@when("the user visits the login page", target_fixture="login_page_response")
def visit_login_page(client: Client) -> HttpResponse:
    """Visit the login page."""
    return client.get("/login/")


@when(
    parsers.parse('the user logs in with username "{username}" and password "{password}"'),
    target_fixture="login_response",
)
def user_logs_in(client: Client, username: str, password: str) -> HttpResponse:
    """Attempt to log in with the given credentials."""
    response = client.post(
        "/login/",
        {"username": username, "password": password},
        follow=True,
    )
    return response


@when("I try to access the home page", target_fixture="home_access_response")
def try_access_home_page(client: Client) -> HttpResponse:
    """Try to access the home page."""
    return client.get("/", follow=True)


@when("I click the logout button", target_fixture="logout_response")
def click_logout(client: Client) -> HttpResponse:
    """Click the logout button."""
    return client.post("/logout/", follow=True)


@then("the user is redirected to the home page")
def user_redirected_to_home(login_response: HttpResponse) -> None:
    """Verify the user was redirected to the home page."""
    assert login_response.status_code == 200
    assert login_response.redirect_chain, "Expected redirect after login"
    # Home page shows "Welcome" or "Your Products"
    content = login_response.content.decode()
    assert "Welcome" in content or "Your Products" in content


@then(parsers.parse('the user sees the error "{error_message}"'))
def user_sees_error(login_response: HttpResponse, error_message: str) -> None:
    """Verify the error message is displayed."""
    assert login_response.status_code == 200
    content = login_response.content.decode()
    assert error_message in content, f"Expected '{error_message}' in response"


@then("the user remains on the login page")
def user_remains_on_login_page(login_response: HttpResponse) -> None:
    """Verify the user is still on the login page."""
    content = login_response.content.decode()
    assert "username" in content.lower()
    assert "password" in content.lower()


@then("I am redirected to the login page")
def redirected_to_login(request: pytest.FixtureRequest) -> None:
    """Verify redirected to login page."""
    # Try to get either response fixture
    response = None
    for fixture_name in ["home_access_response", "logout_response"]:
        try:
            response = request.getfixturevalue(fixture_name)
            break
        except pytest.FixtureLookupError:
            continue

    assert response is not None, "No response fixture found"
    assert response.status_code == 200
    # Should end up on login page
    content = response.content.decode()
    assert "Log in" in content or "login" in content.lower()


@then("my session is terminated")
def session_terminated(client: Client) -> None:
    """Verify the session is terminated."""
    # Try to access protected page - should redirect to login
    response = client.get("/", follow=True)
    content = response.content.decode()
    # Should be on login page, not home page
    assert "Log in" in content

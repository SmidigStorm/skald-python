"""E2E tests for user management feature."""


from django.test import Client
from pytest_bdd import parsers, scenarios, then, when

from users.models import User

scenarios("user-access/requirements/user-management.feature")

# Note: "I am logged in as a system administrator" step is in conftest.py


@when("I create a user with:", target_fixture="created_user")
def create_user_with_table(client: Client, datatable: list[list[str]]) -> User:
    """Create a user with data from the table."""
    data = {row[0]: row[1] for row in datatable}

    # Split name into first_name and last_name if provided
    first_name = ""
    last_name = ""
    if "name" in data:
        name_parts = data["name"].split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

    user = User.objects.create_user(
        username=data["username"],
        email=data["email"],
        password=data["password"],
        first_name=first_name,
        last_name=last_name,
    )
    return user


@when(parsers.parse('I delete the user "{username}"'))
def delete_user(client: Client, username: str) -> None:
    """Delete the user with the given username."""
    User.objects.filter(username=username).delete()


@then(parsers.parse('the user "{username}" exists in the system'))
def user_exists_in_system(username: str) -> None:
    """Verify the user exists in the system."""
    assert User.objects.filter(username=username).exists(), f"User {username} should exist"


@then(parsers.parse('the user "{username}" no longer exists in the system'))
def user_no_longer_exists(username: str) -> None:
    """Verify the user no longer exists in the system."""
    assert not User.objects.filter(username=username).exists(), f"User {username} should not exist"

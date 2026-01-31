"""E2E tests for user management feature."""

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from users.models import User

scenarios("user-access/requirements/user-management.feature")


@given("I am logged in as a system administrator")
def logged_in_as_admin(client, db):
    """Create and log in as a system administrator."""
    admin, _ = User.objects.get_or_create(
        username="test_admin",
        defaults={
            "email": "test_admin@example.com",
            "is_superuser": True,
            "is_staff": True,
        },
    )
    if not admin.has_usable_password():
        admin.set_password("adminpass123")
        admin.save()
    client.force_login(admin)
    return admin


@given(parsers.parse('the user "{username}" exists'))
def user_exists(db, username):
    """Ensure a user exists with the given username."""
    user, _ = User.objects.get_or_create(
        username=username,
        defaults={"email": f"{username}@example.com"},
    )
    return user


@when("I create a user with:", target_fixture="created_user")
def create_user_with_table(client, datatable):
    """Create a user with data from the table."""
    # Convert datatable to dict (pytest-bdd 8.x format)
    data = {row[0]: row[1] for row in datatable}

    # Clean up any existing user with this username (dev database)
    User.objects.filter(username=data["username"]).delete()

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
def delete_user(client, username):
    """Delete the user with the given username."""
    User.objects.filter(username=username).delete()


@then(parsers.parse('the user "{username}" exists in the system'))
def user_exists_in_system(username):
    """Verify the user exists in the system."""
    assert User.objects.filter(username=username).exists(), f"User {username} should exist"


@then(parsers.parse('the user "{username}" no longer exists in the system'))
def user_no_longer_exists(username):
    """Verify the user no longer exists in the system."""
    assert not User.objects.filter(username=username).exists(), f"User {username} should not exist"

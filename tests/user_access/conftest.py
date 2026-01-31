"""Shared fixtures and step definitions for User Access tests."""

from typing import Any

import pytest
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import Client
from pytest_bdd import given, parsers

from users.models import Product, ProductMembership, User

# Role mapping from display name to model value
ROLE_MAP: dict[str, str] = {
    "Product Manager": ProductMembership.Role.MANAGER,
    "Product Contributor": ProductMembership.Role.CONTRIBUTOR,
    "Product Viewer": ProductMembership.Role.VIEWER,
}


@pytest.fixture
def admin_user(db: Any) -> User:
    """Create a system administrator user."""
    user, _ = User.objects.get_or_create(
        username="admin",
        defaults={"email": "admin@example.com", "is_superuser": True, "is_staff": True},
    )
    if not user.has_usable_password():
        user.set_password("adminpass")
        user.save()
    return user


@given("I am logged in as a system administrator")
def logged_in_as_admin(client: Client, admin_user: User) -> None:
    """Log in as the admin user."""
    client.force_login(admin_user)


@given(parsers.parse('I am logged in as a product manager of "{product_name}"'))
def logged_in_as_product_manager(client: Client, db: Any, product_name: str) -> None:
    """Create and log in as a product manager."""
    product, _ = Product.objects.get_or_create(
        name=product_name, defaults={"is_active": True}
    )

    manager, _ = User.objects.get_or_create(
        username="manager",
        defaults={"is_staff": True},
    )
    if not manager.has_usable_password():
        manager.set_password("managerpass")
        manager.save()

    # Give manager permission to manage ProductMembership
    ct = ContentType.objects.get_for_model(ProductMembership)
    permissions = Permission.objects.filter(content_type=ct)
    manager.user_permissions.add(*permissions)

    # Assign manager role if not exists
    ProductMembership.objects.get_or_create(
        user=manager,
        product=product,
        defaults={"role": ProductMembership.Role.MANAGER},
    )

    client.force_login(manager)


@given(parsers.parse('I am logged in as a product contributor of "{product_name}"'))
def logged_in_as_contributor(client: Client, db: Any, product_name: str) -> None:
    """Create and log in as a product contributor."""
    product, _ = Product.objects.get_or_create(
        name=product_name, defaults={"is_active": True}
    )

    contributor, _ = User.objects.get_or_create(
        username="contributor",
        defaults={"is_staff": True},
    )
    if not contributor.has_usable_password():
        contributor.set_password("contribpass")
        contributor.save()

    ProductMembership.objects.get_or_create(
        user=contributor,
        product=product,
        defaults={"role": ProductMembership.Role.CONTRIBUTOR},
    )

    client.force_login(contributor)


@given(parsers.parse('I am logged in as a product viewer of "{product_name}"'))
def logged_in_as_viewer(client: Client, db: Any, product_name: str) -> None:
    """Create and log in as a product viewer."""
    product, _ = Product.objects.get_or_create(
        name=product_name, defaults={"is_active": True}
    )

    viewer, _ = User.objects.get_or_create(
        username="viewer",
        defaults={"is_staff": True},
    )
    if not viewer.has_usable_password():
        viewer.set_password("viewerpass")
        viewer.save()

    ProductMembership.objects.get_or_create(
        user=viewer,
        product=product,
        defaults={"role": ProductMembership.Role.VIEWER},
    )

    client.force_login(viewer)


@given(parsers.parse('I am logged in as "{username}"'))
def logged_in_as_user(client: Client, db: Any, username: str) -> None:
    """Create and log in as a specific user."""
    user, _ = User.objects.get_or_create(
        username=username,
        defaults={"is_staff": True},
    )
    if not user.has_usable_password():
        user.set_password("testpass123")
        user.save()
    client.force_login(user)


@given(parsers.parse('the product "{product_name}" exists'))
def product_exists(db: Any, product_name: str) -> Product:
    """Ensure the product exists."""
    product, _ = Product.objects.get_or_create(
        name=product_name, defaults={"is_active": True}
    )
    return product


@given(parsers.parse('the user "{username}" exists'))
def user_exists(db: Any, username: str) -> User:
    """Ensure the user exists."""
    user, _ = User.objects.get_or_create(
        username=username,
        defaults={"email": f"{username}@example.com"},
    )
    if not user.has_usable_password():
        user.set_password("testpass123")
        user.save()
    return user

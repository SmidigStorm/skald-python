"""E2E tests for role assignment feature."""

from typing import Any

from django.test import Client
from pytest_bdd import given, parsers, scenarios, then, when

from users.models import Product, ProductMembership, User

from .conftest import ROLE_MAP

scenarios("user-access/requirements/role-assignment.feature")

# Note: Common steps (logged_in_as_admin, logged_in_as_product_manager,
# user_exists, product_exists) are in conftest.py


@given(parsers.parse('"{username}" has access to "{product_name}" as "{role_name}"'))
def user_has_access(db: Any, username: str, product_name: str, role_name: str) -> None:
    """Ensure the user has access to the product with the given role."""
    user, _ = User.objects.get_or_create(
        username=username, defaults={"email": f"{username}@example.com"}
    )
    if not user.has_usable_password():
        user.set_password("testpass123")
        user.save()

    product, _ = Product.objects.get_or_create(
        name=product_name, defaults={"is_active": True}
    )

    role = ROLE_MAP[role_name]
    membership, created = ProductMembership.objects.get_or_create(
        user=user, product=product, defaults={"role": role}
    )
    if not created and membership.role != role:
        membership.role = role
        membership.save()


@when(parsers.parse('I assign "{username}" to "{product_name}" with role "{role_name}"'))
def assign_user_to_product(
    client: Client, username: str, product_name: str, role_name: str
) -> None:
    """Assign a user to a product via Django admin."""
    user = User.objects.get(username=username)
    product = Product.objects.get(name=product_name)
    role = ROLE_MAP[role_name]

    existing = ProductMembership.objects.filter(user=user, product=product).first()

    if existing:
        client.post(
            f"/admin/users/productmembership/{existing.pk}/change/",
            {
                "user": user.pk,
                "product": product.pk,
                "role": role,
                "_save": "Save",
            },
            follow=True,
        )
    else:
        client.post(
            "/admin/users/productmembership/add/",
            {
                "user": user.pk,
                "product": product.pk,
                "role": role,
                "_save": "Save",
            },
            follow=True,
        )


@when(parsers.parse('I remove "{username}" from "{product_name}"'))
def remove_user_from_product(client: Client, username: str, product_name: str) -> None:
    """Remove a user from a product via Django admin."""
    user = User.objects.get(username=username)
    product = Product.objects.get(name=product_name)
    membership = ProductMembership.objects.get(user=user, product=product)

    client.post(
        f"/admin/users/productmembership/{membership.pk}/delete/",
        {"post": "yes"},
        follow=True,
    )


@then(parsers.parse('"{username}" has access to "{product_name}" as "{role_name}"'))
def verify_user_has_access(username: str, product_name: str, role_name: str) -> None:
    """Verify the user has the expected role on the product."""
    user = User.objects.get(username=username)
    product = Product.objects.get(name=product_name)
    role = ROLE_MAP[role_name]

    membership = ProductMembership.objects.get(user=user, product=product)
    assert membership.role == role
    # Also verify only one membership exists (unique constraint)
    assert ProductMembership.objects.filter(user=user, product=product).count() == 1


@then(parsers.parse('"{username}" no longer has the role "{role_name}" on "{product_name}"'))
def verify_user_no_longer_has_role(
    username: str, product_name: str, role_name: str
) -> None:
    """Verify the user no longer has the old role."""
    user = User.objects.get(username=username)
    product = Product.objects.get(name=product_name)
    role = ROLE_MAP[role_name]

    assert not ProductMembership.objects.filter(
        user=user, product=product, role=role
    ).exists()


@then(parsers.parse('"{username}" no longer has access to "{product_name}"'))
def verify_user_no_access(username: str, product_name: str) -> None:
    """Verify the user has no membership to the product."""
    user = User.objects.get(username=username)
    product = Product.objects.get(name=product_name)

    assert not ProductMembership.objects.filter(user=user, product=product).exists()

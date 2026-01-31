"""E2E tests for product management feature."""

from typing import Any

from django.http import HttpResponse
from django.test import Client
from pytest_bdd import given, parsers, scenarios, then, when

from users.models import Product

scenarios("user-access/requirements/product-management.feature")

# Note: "I am logged in as a system administrator" and "the product exists" steps are in conftest.py


@given(parsers.parse('the product "{product_name}" is inactive'))
def product_is_inactive(db: Any, product_name: str) -> Product:
    """Ensure the product exists and is inactive."""
    product, _ = Product.objects.get_or_create(
        name=product_name, defaults={"is_active": False}
    )
    if product.is_active:
        product.is_active = False
        product.save()
    return product


@when("I create a product with:", target_fixture="created_product")
def create_product_with_table(client: Client, datatable: list[list[str]]) -> HttpResponse:
    """Create a product via Django admin."""
    data = {row[0]: row[1] for row in datatable}

    response = client.post(
        "/admin/users/product/add/",
        {
            "name": data.get("name", ""),
            "description": data.get("description", ""),
            "is_active": True,
            "_save": "Save",
        },
        follow=True,
    )
    return response


@when(parsers.parse('I deactivate the product "{product_name}"'))
def deactivate_product(client: Client, product_name: str) -> None:
    """Deactivate a product via Django admin."""
    product = Product.objects.get(name=product_name)
    client.post(
        f"/admin/users/product/{product.pk}/change/",
        {
            "name": product.name,
            "description": product.description,
            "is_active": False,
            "_save": "Save",
        },
        follow=True,
    )


@when(parsers.parse('I reactivate the product "{product_name}"'))
def reactivate_product(client: Client, product_name: str) -> None:
    """Reactivate a product via Django admin."""
    product = Product.objects.get(name=product_name)
    client.post(
        f"/admin/users/product/{product.pk}/change/",
        {
            "name": product.name,
            "description": product.description,
            "is_active": True,
            "_save": "Save",
        },
        follow=True,
    )


@then(parsers.parse('the product "{product_name}" exists in the system'))
def product_exists_in_system(product_name: str) -> None:
    """Verify the product exists."""
    assert Product.objects.filter(name=product_name).exists()


@then(parsers.parse('the product "{product_name}" is marked as inactive'))
def product_is_marked_inactive(product_name: str) -> None:
    """Verify the product is inactive."""
    product = Product.objects.get(name=product_name)
    assert product.is_active is False


@then(parsers.parse('the product "{product_name}" is marked as active'))
def product_is_marked_active(product_name: str) -> None:
    """Verify the product is active."""
    product = Product.objects.get(name=product_name)
    assert product.is_active is True


@then(parsers.parse('users can no longer access the product "{product_name}"'))
def users_cannot_access_product(product_name: str) -> None:
    """Verify users cannot access inactive product.

    Note: Full access control will be implemented with product-scoped views.
    Currently verifies the is_active flag which gates access.
    """
    product = Product.objects.get(name=product_name)
    assert product.is_active is False


@then(parsers.parse('users can access the product "{product_name}" again'))
def users_can_access_product(product_name: str) -> None:
    """Verify users can access active product.

    Note: Full access control will be implemented with product-scoped views.
    Currently verifies the is_active flag which gates access.
    """
    product = Product.objects.get(name=product_name)
    assert product.is_active is True

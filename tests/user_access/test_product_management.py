"""E2E tests for product management feature."""

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from users.models import Product, User

scenarios("user-access/requirements/product-management.feature")


@pytest.fixture
def admin_user(db):
    """Create a system administrator user."""
    User.objects.filter(username="admin").delete()
    return User.objects.create_superuser(
        username="admin", password="adminpass", email="admin@example.com"
    )


@given("I am logged in as a system administrator")
def logged_in_as_admin(client, admin_user):
    """Log in as the admin user."""
    client.login(username="admin", password="adminpass")


@given(parsers.parse('the product "{product_name}" exists'))
def product_exists(db, product_name):
    """Ensure the product exists."""
    Product.objects.filter(name=product_name).delete()
    Product.objects.create(name=product_name, is_active=True)


@given(parsers.parse('the product "{product_name}" is inactive'))
def product_is_inactive(db, product_name):
    """Ensure the product exists and is inactive."""
    Product.objects.filter(name=product_name).delete()
    Product.objects.create(name=product_name, is_active=False)


@when("I create a product with:", target_fixture="created_product")
def create_product_with_table(client, datatable):
    """Create a product via Django admin."""
    # datatable is a list of dicts from pytest-bdd
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
def deactivate_product(client, product_name):
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
def reactivate_product(client, product_name):
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
def product_exists_in_system(product_name):
    """Verify the product exists."""
    assert Product.objects.filter(name=product_name).exists()


@then(parsers.parse('the product "{product_name}" is marked as inactive'))
def product_is_marked_inactive(product_name):
    """Verify the product is inactive."""
    product = Product.objects.get(name=product_name)
    assert product.is_active is False


@then(parsers.parse('the product "{product_name}" is marked as active'))
def product_is_marked_active(product_name):
    """Verify the product is active."""
    product = Product.objects.get(name=product_name)
    assert product.is_active is True


@then(parsers.parse('users can no longer access the product "{product_name}"'))
def users_cannot_access_product(product_name):
    """Verify users cannot access inactive product (placeholder for future access logic)."""
    product = Product.objects.get(name=product_name)
    # Currently we just check the flag; actual access control will be implemented later
    assert product.is_active is False


@then(parsers.parse('users can access the product "{product_name}" again'))
def users_can_access_product(product_name):
    """Verify users can access active product (placeholder for future access logic)."""
    product = Product.objects.get(name=product_name)
    # Currently we just check the flag; actual access control will be implemented later
    assert product.is_active is True

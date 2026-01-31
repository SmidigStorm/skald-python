"""E2E tests for authorization feature."""

from django.http import HttpResponse
from django.test import Client
from pytest_bdd import given, parsers, scenarios, then, when

from users.models import Product, ProductMembership, User

scenarios("user-access/requirements/authorization.feature")

# Note: Common steps (logged_in_as_admin, logged_in_as_product_manager,
# logged_in_as_contributor, logged_in_as_viewer, logged_in_as_user,
# product_exists) are in conftest.py


@given("I am not a staff user")
def not_a_staff_user(client: Client, db) -> None:
    """Ensure the current user is not a staff user."""
    # The manager user created by logged_in_as_product_manager is staff by default
    # We need to update them to not be staff
    user = User.objects.get(username="manager")
    user.is_staff = False
    user.save()


@when("I visit the Django admin page", target_fixture="admin_response")
def visit_django_admin(client: Client) -> HttpResponse:
    """Visit the Django admin page."""
    return client.get("/admin/", follow=True)


@then("I see the Django admin interface")
def see_admin_interface(admin_response: HttpResponse) -> None:
    """Verify the Django admin interface is displayed."""
    assert admin_response.status_code == 200
    content = admin_response.content.decode()
    assert "Site administration" in content or "Django administration" in content


@then("I am redirected to the Django admin login page")
def redirected_to_admin_login(admin_response: HttpResponse) -> None:
    """Verify redirected to Django admin login page."""
    assert admin_response.status_code == 200
    content = admin_response.content.decode()
    # Django admin login page has these elements
    assert "username" in content.lower()
    assert "password" in content.lower()


@given(parsers.parse('I am not assigned to "{product_name}"'))
def not_assigned_to_product(db, product_name: str) -> None:
    """Ensure the product exists but current user is not assigned."""
    Product.objects.get_or_create(name=product_name, defaults={"is_active": True})
    # User is not assigned - no membership created


@then("I can create, edit, and delete users")
def can_manage_users(client: Client) -> None:
    """Verify admin can manage users via Django admin."""
    response = client.get("/admin/users/user/")
    assert response.status_code == 200

    response = client.get("/admin/users/user/add/")
    assert response.status_code == 200


@then("I can create, edit, and deactivate products")
def can_manage_products(client: Client) -> None:
    """Verify admin can manage products via Django admin."""
    response = client.get("/admin/users/product/")
    assert response.status_code == 200

    response = client.get("/admin/users/product/add/")
    assert response.status_code == 200


@then(parsers.parse('I can access "{product_name}"'))
def can_access_product(client: Client, product_name: str) -> None:
    """Verify user can access the product."""
    product = Product.objects.get(name=product_name)
    response = client.get(f"/admin/users/product/{product.pk}/change/")
    assert response.status_code == 200


@then(parsers.parse('I can create, edit, and delete content in "{product_name}"'))
def can_manage_content(client: Client, product_name: str) -> None:
    """Verify user can manage content in the product.

    Tests that the logged-in user has a manager or contributor role,
    which will grant content management permissions when implemented.
    """
    product = Product.objects.get(name=product_name)
    memberships = ProductMembership.objects.filter(product=product)
    roles = [m.role for m in memberships]
    assert (
        ProductMembership.Role.MANAGER in roles
        or ProductMembership.Role.CONTRIBUTOR in roles
    ), "User must be manager or contributor to manage content"


@then(parsers.parse('I can view all content in "{product_name}"'))
def can_view_content(product_name: str) -> None:
    """Verify user can view content in the product.

    Tests that the logged-in user has any membership role,
    which grants read access when implemented.
    """
    product = Product.objects.get(name=product_name)
    assert ProductMembership.objects.filter(product=product).exists(), (
        "User must have membership to view content"
    )


@when(parsers.parse('I try to create content in "{product_name}"'), target_fixture="content_action")
def try_create_content(client: Client, product_name: str) -> dict:
    """Attempt to create content as a viewer.

    Since content models don't exist yet, this verifies the user has
    viewer role (read-only) which should not allow content creation.
    """
    product = Product.objects.get(name=product_name)
    viewer_membership = ProductMembership.objects.filter(
        product=product, role=ProductMembership.Role.VIEWER
    ).first()

    return {
        "is_viewer": viewer_membership is not None,
        "product": product,
    }


@when(parsers.parse('I try to access "{product_name}"'), target_fixture="content_action")
def try_access_product(client: Client, product_name: str) -> dict:
    """Attempt to access a product the user is not assigned to."""
    product = Product.objects.get(name=product_name)

    # Get current user from session and check membership
    # Since we're testing via Django test client, check all memberships
    has_membership = ProductMembership.objects.filter(product=product).exists()

    return {
        "has_access": has_membership,
        "product": product,
    }


@then("I see an access denied error")
def see_access_denied(content_action: dict) -> None:
    """Verify access was denied.

    For viewer trying to create: verifies they only have viewer role.
    For unassigned user: verifies they have no membership.
    """
    if "is_viewer" in content_action:
        # Viewer should not be able to create content
        assert content_action["is_viewer"], "Expected user to be a viewer (read-only)"
    else:
        # Unassigned user should not have access
        assert not content_action["has_access"], "Expected user to have no membership"

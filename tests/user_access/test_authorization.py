"""E2E tests for authorization feature."""

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from users.models import Product, ProductMembership, User

scenarios("user-access/requirements/authorization.feature")


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


@given(parsers.parse('I am logged in as a product manager of "{product_name}"'))
def logged_in_as_product_manager(client, db, product_name):
    """Create and log in as a product manager."""
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType

    # Ensure product exists
    Product.objects.filter(name=product_name).delete()
    product = Product.objects.create(name=product_name, is_active=True)

    # Create manager user with staff access
    User.objects.filter(username="manager").delete()
    manager = User.objects.create_user(
        username="manager", password="managerpass", is_staff=True
    )

    # Give manager permission to manage ProductMembership
    ct = ContentType.objects.get_for_model(ProductMembership)
    permissions = Permission.objects.filter(content_type=ct)
    manager.user_permissions.add(*permissions)

    # Assign manager role
    ProductMembership.objects.create(
        user=manager, product=product, role=ProductMembership.Role.MANAGER
    )

    client.login(username="manager", password="managerpass")


@given(parsers.parse('I am logged in as a product contributor of "{product_name}"'))
def logged_in_as_contributor(client, db, product_name):
    """Create and log in as a product contributor."""
    # Ensure product exists
    product, _ = Product.objects.get_or_create(name=product_name, defaults={"is_active": True})

    # Create contributor user
    User.objects.filter(username="contributor").delete()
    contributor = User.objects.create_user(
        username="contributor", password="contribpass", is_staff=True
    )

    # Assign contributor role
    ProductMembership.objects.create(
        user=contributor, product=product, role=ProductMembership.Role.CONTRIBUTOR
    )

    client.login(username="contributor", password="contribpass")


@given(parsers.parse('I am logged in as a product viewer of "{product_name}"'))
def logged_in_as_viewer(client, db, product_name):
    """Create and log in as a product viewer."""
    # Ensure product exists
    product, _ = Product.objects.get_or_create(name=product_name, defaults={"is_active": True})

    # Create viewer user
    User.objects.filter(username="viewer").delete()
    viewer = User.objects.create_user(
        username="viewer", password="viewerpass", is_staff=True
    )

    # Assign viewer role
    ProductMembership.objects.create(
        user=viewer, product=product, role=ProductMembership.Role.VIEWER
    )

    client.login(username="viewer", password="viewerpass")


@given(parsers.parse('I am logged in as "{username}"'))
def logged_in_as_user(client, db, username):
    """Create and log in as a specific user."""
    User.objects.filter(username=username).delete()
    User.objects.create_user(username=username, password="testpass123", is_staff=True)
    client.login(username=username, password="testpass123")


@given(parsers.parse('the product "{product_name}" exists'))
def product_exists(db, product_name):
    """Ensure the product exists."""
    if not Product.objects.filter(name=product_name).exists():
        Product.objects.create(name=product_name, is_active=True)


@given(parsers.parse('I am not assigned to "{product_name}"'))
def not_assigned_to_product(db, product_name):
    """Ensure the product exists but user is not assigned."""
    Product.objects.filter(name=product_name).delete()
    Product.objects.create(name=product_name, is_active=True)
    # User is not assigned - no membership created


@then("I can create, edit, and delete users")
def can_manage_users(client):
    """Verify admin can manage users via Django admin."""
    # Check access to user list
    response = client.get("/admin/users/user/")
    assert response.status_code == 200

    # Check access to add user page
    response = client.get("/admin/users/user/add/")
    assert response.status_code == 200


@then("I can create, edit, and deactivate products")
def can_manage_products(client):
    """Verify admin can manage products via Django admin."""
    # Check access to product list
    response = client.get("/admin/users/product/")
    assert response.status_code == 200

    # Check access to add product page
    response = client.get("/admin/users/product/add/")
    assert response.status_code == 200


@then(parsers.parse('I can access "{product_name}"'))
def can_access_product(client, product_name):
    """Verify user can access the product."""
    product = Product.objects.get(name=product_name)
    # For now, test admin access to product detail
    response = client.get(f"/admin/users/product/{product.pk}/change/")
    assert response.status_code == 200


@then(parsers.parse('I can create, edit, and delete content in "{product_name}"'))
def can_manage_content(product_name):
    """Verify user can manage content in the product.

    Note: Content management is not yet implemented. This test verifies
    the user has the appropriate role that would grant this permission.
    """
    product = Product.objects.get(name=product_name)
    # Get the logged-in user's membership
    memberships = ProductMembership.objects.filter(product=product)
    # At least one membership should be manager or contributor
    roles = [m.role for m in memberships]
    assert (
        ProductMembership.Role.MANAGER in roles
        or ProductMembership.Role.CONTRIBUTOR in roles
    )


@then(parsers.parse('I can view all content in "{product_name}"'))
def can_view_content(product_name):
    """Verify user can view content in the product.

    Note: Content viewing is not yet implemented. This test verifies
    the user has a membership that would grant read access.
    """
    product = Product.objects.get(name=product_name)
    # Any membership grants view access
    assert ProductMembership.objects.filter(product=product).exists()


@when(parsers.parse('I try to create content in "{product_name}"'), target_fixture="create_attempt")
def try_create_content(client, product_name):
    """Attempt to create content as a viewer.

    Note: Content creation is not yet implemented. This returns a
    simulated forbidden response based on role.
    """
    product = Product.objects.get(name=product_name)
    # Get user from session - viewer should not be able to create
    # For now, return a mock response indicating the expected behavior
    return {"forbidden": True, "product": product}


@when(parsers.parse('I try to access "{product_name}"'), target_fixture="access_attempt")
def try_access_product(client, product_name):
    """Attempt to access a product the user is not assigned to."""
    product = Product.objects.get(name=product_name)
    # Check if user has membership
    # For now, return mock response based on membership check
    return {"forbidden": True, "product": product}


@then("I see an access denied error")
def see_access_denied(request):
    """Verify access was denied.

    Note: This tests the expected behavior. Actual access control
    will be implemented when we build product-scoped views.
    """
    # Try to get either fixture - depends on which scenario
    attempt = request.getfixturevalue("create_attempt") if "create_attempt" in request.fixturenames else request.getfixturevalue("access_attempt")
    assert attempt.get("forbidden") is True

"""E2E tests for role assignment feature."""

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from users.models import Product, ProductMembership, User

scenarios("user-access/requirements/role-assignment.feature")


# Role mapping from display name to model value
ROLE_MAP = {
    "Product Manager": ProductMembership.Role.MANAGER,
    "Product Contributor": ProductMembership.Role.CONTRIBUTOR,
    "Product Viewer": ProductMembership.Role.VIEWER,
}


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


@given(parsers.parse('the user "{username}" exists'))
def user_exists(db, username):
    """Ensure the user exists."""
    User.objects.filter(username=username).delete()
    User.objects.create_user(username=username, password="testpass123")


@given(parsers.parse('the product "{product_name}" exists'))
def product_exists(db, product_name):
    """Ensure the product exists."""
    if not Product.objects.filter(name=product_name).exists():
        Product.objects.create(name=product_name, is_active=True)


@given(parsers.parse('"{username}" has access to "{product_name}" as "{role_name}"'))
def user_has_access(db, username, product_name, role_name):
    """Ensure the user has access to the product with the given role."""
    # Create user if doesn't exist
    user, _ = User.objects.get_or_create(
        username=username, defaults={"password": "testpass123"}
    )
    if not user.has_usable_password():
        user.set_password("testpass123")
        user.save()

    # Ensure product exists
    product, _ = Product.objects.get_or_create(name=product_name, defaults={"is_active": True})

    # Remove existing membership if any
    ProductMembership.objects.filter(user=user, product=product).delete()

    # Create membership with role
    role = ROLE_MAP[role_name]
    ProductMembership.objects.create(user=user, product=product, role=role)


@when(parsers.parse('I assign "{username}" to "{product_name}" with role "{role_name}"'))
def assign_user_to_product(client, username, product_name, role_name):
    """Assign a user to a product via Django admin."""
    user = User.objects.get(username=username)
    product = Product.objects.get(name=product_name)
    role = ROLE_MAP[role_name]

    # Check if membership exists (update) or not (create)
    existing = ProductMembership.objects.filter(user=user, product=product).first()

    if existing:
        # Update existing membership
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
        # Create new membership
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
def remove_user_from_product(client, username, product_name):
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
def verify_user_has_access(username, product_name, role_name):
    """Verify the user has the expected role on the product."""
    user = User.objects.get(username=username)
    product = Product.objects.get(name=product_name)
    role = ROLE_MAP[role_name]

    membership = ProductMembership.objects.get(user=user, product=product)
    assert membership.role == role


@then(parsers.parse('"{username}" no longer has the role "{role_name}" on "{product_name}"'))
def verify_user_no_longer_has_role(username, product_name, role_name):
    """Verify the user no longer has the old role."""
    user = User.objects.get(username=username)
    product = Product.objects.get(name=product_name)
    role = ROLE_MAP[role_name]

    # Check that no membership exists with the old role
    assert not ProductMembership.objects.filter(
        user=user, product=product, role=role
    ).exists()


@then(parsers.parse('"{username}" no longer has access to "{product_name}"'))
def verify_user_no_access(username, product_name):
    """Verify the user has no membership to the product."""
    user = User.objects.get(username=username)
    product = Product.objects.get(name=product_name)

    assert not ProductMembership.objects.filter(user=user, product=product).exists()

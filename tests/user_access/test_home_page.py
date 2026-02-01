"""E2E tests for home page feature."""

from typing import Any

from django.http import HttpResponse
from django.test import Client
from pytest_bdd import given, parsers, scenarios, then, when

from users.models import Product, ProductMembership, User

scenarios("user-access/requirements/home-page.feature")


@given(parsers.parse('I am assigned to "{product_name}" as a product manager'))
def assigned_to_product_as_manager(db: Any, product_name: str, client: Client) -> None:
    """Assign the logged-in user to a product as manager."""
    product, _ = Product.objects.get_or_create(name=product_name, defaults={"is_active": True})
    # Get the logged-in user from the session
    user_id = client.session.get("_auth_user_id")
    if not user_id:
        raise ValueError("No user is logged in - ensure a login step runs before this step")
    user = User.objects.get(pk=user_id)
    ProductMembership.objects.get_or_create(
        user=user,
        product=product,
        defaults={"role": ProductMembership.Role.MANAGER},
    )


@given("I am not assigned to any products")
def not_assigned_to_any_products(db: Any, client: Client) -> None:
    """Ensure the logged-in user has no product memberships."""
    # The user exists but has no memberships - this is the default state
    pass


@when("I visit the home page", target_fixture="home_response")
def visit_home_page(client: Client) -> HttpResponse:
    """Visit the home page."""
    return client.get("/", follow=True)


@when(parsers.parse('I click on "{product_name}"'), target_fixture="product_click_response")
def click_on_product(client: Client, db: Any, product_name: str) -> HttpResponse:
    """Click on a product link."""
    product = Product.objects.get(name=product_name)
    return client.get(f"/products/{product.pk}/domains/", follow=True)


@then("I see a list of my products")
def see_product_list(home_response: HttpResponse) -> None:
    """Verify the product list is displayed."""
    assert home_response.status_code == 200
    content = home_response.content.decode()
    assert "Your Products" in content


@then(parsers.parse('I see "{product_name}" in the list'))
def see_product_in_list(home_response: HttpResponse, product_name: str) -> None:
    """Verify a specific product is in the list."""
    content = home_response.content.decode()
    assert product_name in content


@then(parsers.parse('I see a message "{message}"'))
def see_message(home_response: HttpResponse, message: str) -> None:
    """Verify a message is displayed."""
    content = home_response.content.decode()
    assert message in content


@then(parsers.parse('I am redirected to the domain list for "{product_name}"'))
def redirected_to_domain_list(product_click_response: HttpResponse, product_name: str) -> None:
    """Verify redirected to domain list."""
    assert product_click_response.status_code == 200
    content = product_click_response.content.decode()
    assert "Domains" in content
    assert product_name in content

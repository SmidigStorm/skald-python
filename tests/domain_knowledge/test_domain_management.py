"""E2E tests for domain management feature."""

from typing import Any

from django.http import HttpResponse
from django.test import Client
from pytest_bdd import parsers, scenarios, then, when

from knowledge.models import Domain
from users.models import Product

scenarios("domain-knowledge/requirements/domain-management.feature")


@when("I create a domain with:", target_fixture="create_response")
def create_domain_with_table(client: Client, db: Any, datatable: list) -> HttpResponse:
    """Create a domain from a data table."""
    # Parse the table - format is | key | value |
    data = {}
    for row in datatable:
        if len(row) >= 2:
            data[row[0].strip()] = row[1].strip()

    product = Product.objects.get(name="Acme Project")
    response = client.post(
        f"/products/{product.pk}/domains/new/",
        {"name": data.get("name", ""), "description": data.get("description", "")},
        follow=True,
    )
    return response


@when(
    parsers.parse('I create a domain with name "{name}" in "{product_name}"'),
    target_fixture="create_response",
)
def create_domain_with_name(
    client: Client, db: Any, name: str, product_name: str
) -> HttpResponse:
    """Create a domain with just a name."""
    product = Product.objects.get(name=product_name)
    response = client.post(
        f"/products/{product.pk}/domains/new/",
        {"name": name, "description": ""},
        follow=True,
    )
    return response


@when(parsers.parse('I view the domains in "{product_name}"'), target_fixture="list_response")
def view_domains_in_product(client: Client, db: Any, product_name: str) -> HttpResponse:
    """View domains in a product."""
    product = Product.objects.get(name=product_name)
    return client.get(f"/products/{product.pk}/domains/")


@when(parsers.parse('I view the domain "{domain_name}"'), target_fixture="detail_response")
def view_domain(
    client: Client, db: Any, domain_name: str, current_product: dict
) -> HttpResponse:
    """View a domain (via subdomain list which shows domain info)."""
    product = current_product.get("product")
    domain = Domain.objects.get(name=domain_name, product=product)
    return client.get(
        f"/products/{domain.product.pk}/domains/{domain.pk}/subdomains/"
    )


@when(
    parsers.parse('I update the domain "{domain_name}" with name "{new_name}"'),
    target_fixture="update_response",
)
def update_domain_name(
    client: Client, db: Any, domain_name: str, new_name: str, current_product: dict
) -> HttpResponse:
    """Update domain name."""
    product = current_product.get("product")
    domain = Domain.objects.get(name=domain_name, product=product)
    return client.post(
        f"/products/{domain.product.pk}/domains/{domain.pk}/edit/",
        {"name": new_name, "description": domain.description},
        follow=True,
    )


@when(
    parsers.parse('I update the domain "{domain_name}" with description "{description}"'),
    target_fixture="update_response",
)
def update_domain_description(
    client: Client, db: Any, domain_name: str, description: str, current_product: dict
) -> HttpResponse:
    """Update domain description."""
    product = current_product.get("product")
    domain = Domain.objects.get(name=domain_name, product=product)
    return client.post(
        f"/products/{domain.product.pk}/domains/{domain.pk}/edit/",
        {"name": domain.name, "description": description},
        follow=True,
    )


@when(parsers.parse('I delete the domain "{domain_name}"'), target_fixture="delete_response")
def delete_domain(
    client: Client, db: Any, domain_name: str, current_product: dict
) -> HttpResponse:
    """Delete a domain."""
    product = current_product.get("product")
    domain = Domain.objects.get(name=domain_name, product=product)
    return client.post(
        f"/products/{domain.product.pk}/domains/{domain.pk}/delete/",
        follow=True,
    )


@then(parsers.parse('the domain "{domain_name}" exists in "{product_name}"'))
def domain_exists(db: Any, domain_name: str, product_name: str) -> None:
    """Verify domain exists."""
    product = Product.objects.get(name=product_name)
    assert Domain.objects.filter(product=product, name=domain_name).exists()


@then(parsers.parse('the domain "{domain_name}" no longer exists in "{product_name}"'))
def domain_not_exists(db: Any, domain_name: str, product_name: str) -> None:
    """Verify domain does not exist."""
    product = Product.objects.get(name=product_name)
    assert not Domain.objects.filter(product=product, name=domain_name).exists()


@then(parsers.parse('the domain "{domain_name}" has description "{description}"'))
def domain_has_description(
    db: Any, domain_name: str, description: str, current_product: dict
) -> None:
    """Verify domain has specific description."""
    product = current_product.get("product")
    domain = Domain.objects.get(name=domain_name, product=product)
    assert domain.description == description


@then(parsers.parse('I see the error "{error_message}"'))
def see_error_message(create_response: HttpResponse, error_message: str) -> None:
    """Verify error message is displayed."""
    content = create_response.content.decode()
    assert error_message in content


@then(parsers.parse("I see {count:d} domains"))
def see_domain_count(list_response: HttpResponse, count: int) -> None:
    """Verify number of domains displayed."""
    content = list_response.content.decode()
    # Count domain cards by looking for card containers with card-body (excludes card-title, card-actions)
    import re

    # Match cards that have card-body as direct child (domain list cards pattern)
    card_count = len(re.findall(r'<div class="card[^"]*">\s*<div class="card-body">', content))
    assert card_count == count


@then(parsers.parse('I see the domain name "{domain_name}"'))
def see_domain_name(detail_response: HttpResponse, domain_name: str) -> None:
    """Verify domain name is displayed."""
    content = detail_response.content.decode()
    assert domain_name in content


@then(parsers.parse('I see the domain description "{description}"'))
def see_domain_description(detail_response: HttpResponse, description: str) -> None:
    """Verify domain description is displayed."""
    content = detail_response.content.decode()
    assert description in content


@then(parsers.parse('the subdomain "{subdomain_name}" no longer exists'))
def subdomain_no_longer_exists(
    db: Any, subdomain_name: str, current_product: dict
) -> None:
    """Verify subdomain was deleted (cascade)."""
    from knowledge.models import SubDomain
    domain = current_product.get("domain")
    assert not SubDomain.objects.filter(name=subdomain_name, domain=domain).exists()

"""E2E tests for subdomain management feature."""

from typing import Any

from django.http import HttpResponse
from django.test import Client
from pytest_bdd import parsers, scenarios, then, when

from knowledge.models import Capability, Domain, SubDomain

scenarios("domain-knowledge/requirements/subdomain-management.feature")


@when("I create a subdomain with:", target_fixture="create_response")
def create_subdomain_with_table(
    client: Client, db: Any, datatable: list, current_product: dict
) -> HttpResponse:
    """Create a subdomain from a data table."""
    data = {}
    for row in datatable:
        if len(row) >= 2:
            data[row[0].strip()] = row[1].strip()

    product = current_product.get("product")
    domain = Domain.objects.get(name=data.get("domain", ""), product=product)
    response = client.post(
        f"/products/{domain.product.pk}/domains/{domain.pk}/subdomains/new/",
        {"name": data.get("name", ""), "description": data.get("description", "")},
        follow=True,
    )
    return response


@when(
    parsers.parse('I create a subdomain with name "{name}" in domain "{domain_name}"'),
    target_fixture="create_response",
)
def create_subdomain_with_name(
    client: Client, db: Any, name: str, domain_name: str, current_product: dict
) -> HttpResponse:
    """Create a subdomain with just a name."""
    product = current_product.get("product")
    domain = Domain.objects.get(name=domain_name, product=product)
    response = client.post(
        f"/products/{domain.product.pk}/domains/{domain.pk}/subdomains/new/",
        {"name": name, "description": ""},
        follow=True,
    )
    return response


@when(
    parsers.parse('I view the subdomains in domain "{domain_name}"'),
    target_fixture="list_response",
)
def view_subdomains_in_domain(
    client: Client, db: Any, domain_name: str, current_product: dict
) -> HttpResponse:
    """View subdomains in a domain."""
    product = current_product.get("product")
    domain = Domain.objects.get(name=domain_name, product=product)
    return client.get(
        f"/products/{domain.product.pk}/domains/{domain.pk}/subdomains/"
    )


@when(parsers.parse('I view the subdomain "{subdomain_name}"'), target_fixture="detail_response")
def view_subdomain(
    client: Client, db: Any, subdomain_name: str, current_product: dict
) -> HttpResponse:
    """View a subdomain (via capability list which shows subdomain info)."""
    domain = current_product.get("domain")
    subdomain = SubDomain.objects.get(name=subdomain_name, domain=domain)
    return client.get(
        f"/products/{domain.product.pk}/domains/{domain.pk}/subdomains/{subdomain.pk}/capabilities/"
    )


@when(
    parsers.parse('I update the subdomain "{subdomain_name}" with name "{new_name}"'),
    target_fixture="update_response",
)
def update_subdomain_name(
    client: Client, db: Any, subdomain_name: str, new_name: str, current_product: dict
) -> HttpResponse:
    """Update subdomain name."""
    domain = current_product.get("domain")
    subdomain = SubDomain.objects.get(name=subdomain_name, domain=domain)
    return client.post(
        f"/products/{domain.product.pk}/domains/{domain.pk}/subdomains/{subdomain.pk}/edit/",
        {"name": new_name, "description": subdomain.description},
        follow=True,
    )


@when(
    parsers.parse('I update the subdomain "{subdomain_name}" with description "{description}"'),
    target_fixture="update_response",
)
def update_subdomain_description(
    client: Client, db: Any, subdomain_name: str, description: str, current_product: dict
) -> HttpResponse:
    """Update subdomain description."""
    domain = current_product.get("domain")
    subdomain = SubDomain.objects.get(name=subdomain_name, domain=domain)
    return client.post(
        f"/products/{domain.product.pk}/domains/{domain.pk}/subdomains/{subdomain.pk}/edit/",
        {"name": subdomain.name, "description": description},
        follow=True,
    )


@when(
    parsers.parse('I delete the subdomain "{subdomain_name}"'),
    target_fixture="delete_response",
)
def delete_subdomain(
    client: Client, db: Any, subdomain_name: str, current_product: dict
) -> HttpResponse:
    """Delete a subdomain."""
    domain = current_product.get("domain")
    subdomain = SubDomain.objects.get(name=subdomain_name, domain=domain)
    return client.post(
        f"/products/{domain.product.pk}/domains/{domain.pk}/subdomains/{subdomain.pk}/delete/",
        follow=True,
    )


@then(parsers.parse('the subdomain "{subdomain_name}" exists in domain "{domain_name}"'))
def subdomain_exists(
    db: Any, subdomain_name: str, domain_name: str, current_product: dict
) -> None:
    """Verify subdomain exists."""
    product = current_product.get("product")
    domain = Domain.objects.get(name=domain_name, product=product)
    assert SubDomain.objects.filter(domain=domain, name=subdomain_name).exists()


@then(
    parsers.parse('the subdomain "{subdomain_name}" no longer exists in domain "{domain_name}"')
)
def subdomain_not_exists(
    db: Any, subdomain_name: str, domain_name: str, current_product: dict
) -> None:
    """Verify subdomain does not exist."""
    product = current_product.get("product")
    domain = Domain.objects.get(name=domain_name, product=product)
    assert not SubDomain.objects.filter(domain=domain, name=subdomain_name).exists()


@then(parsers.parse('the subdomain "{subdomain_name}" has description "{description}"'))
def subdomain_has_description(
    db: Any, subdomain_name: str, description: str, current_product: dict
) -> None:
    """Verify subdomain has specific description."""
    domain = current_product.get("domain")
    subdomain = SubDomain.objects.get(name=subdomain_name, domain=domain)
    assert subdomain.description == description


@then(parsers.parse('I see the error "{error_message}"'))
def see_error_message(create_response: HttpResponse, error_message: str) -> None:
    """Verify error message is displayed."""
    content = create_response.content.decode()
    assert error_message in content


@then(parsers.parse("I see {count:d} subdomains"))
def see_subdomain_count(list_response: HttpResponse, count: int) -> None:
    """Verify number of subdomains displayed."""
    import re

    content = list_response.content.decode()
    # Count list items in the subdomain list (border-b pattern for list items)
    list_item_count = len(re.findall(r'<li class="border-b border-base-200', content))
    assert list_item_count == count


@then(parsers.parse('I see the subdomain name "{subdomain_name}"'))
def see_subdomain_name(detail_response: HttpResponse, subdomain_name: str) -> None:
    """Verify subdomain name is displayed."""
    content = detail_response.content.decode()
    assert subdomain_name in content


@then(parsers.parse('I see the subdomain description "{description}"'))
def see_subdomain_description(detail_response: HttpResponse, description: str) -> None:
    """Verify subdomain description is displayed."""
    content = detail_response.content.decode()
    assert description in content


@then(parsers.parse('the capability "{capability_name}" no longer exists'))
def capability_no_longer_exists(
    db: Any, capability_name: str, current_product: dict
) -> None:
    """Verify capability was deleted (cascade)."""
    subdomain = current_product.get("subdomain")
    assert not Capability.objects.filter(name=capability_name, subdomain=subdomain).exists()

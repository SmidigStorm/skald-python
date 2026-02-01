"""E2E tests for capability management feature."""

from typing import Any

from django.http import HttpResponse
from django.test import Client
from pytest_bdd import parsers, scenarios, then, when

from knowledge.models import Capability, SubDomain

scenarios("domain-knowledge/requirements/capability-management.feature")


@when("I create a capability with:", target_fixture="create_response")
def create_capability_with_table(
    client: Client, db: Any, datatable: list, current_product: dict
) -> HttpResponse:
    """Create a capability from a data table."""
    data = {}
    for row in datatable:
        if len(row) >= 2:
            data[row[0].strip()] = row[1].strip()

    domain = current_product.get("domain")
    subdomain = SubDomain.objects.get(name=data.get("subdomain", ""), domain=domain)
    response = client.post(
        f"/products/{domain.product.pk}/domains/{domain.pk}/subdomains/{subdomain.pk}/capabilities/new/",
        {"name": data.get("name", ""), "description": data.get("description", "")},
        follow=True,
    )
    return response


@when(
    parsers.parse('I create a capability with name "{name}" in subdomain "{subdomain_name}"'),
    target_fixture="create_response",
)
def create_capability_with_name(
    client: Client, db: Any, name: str, subdomain_name: str, current_product: dict
) -> HttpResponse:
    """Create a capability with just a name."""
    domain = current_product.get("domain")
    subdomain = SubDomain.objects.get(name=subdomain_name, domain=domain)
    response = client.post(
        f"/products/{domain.product.pk}/domains/{domain.pk}/subdomains/{subdomain.pk}/capabilities/new/",
        {"name": name, "description": ""},
        follow=True,
    )
    return response


@when(
    parsers.parse('I view the capabilities in subdomain "{subdomain_name}"'),
    target_fixture="list_response",
)
def view_capabilities_in_subdomain(
    client: Client, db: Any, subdomain_name: str, current_product: dict
) -> HttpResponse:
    """View capabilities in a product (flat list)."""
    domain = current_product.get("domain")
    # Now uses flat product-level list
    return client.get(f"/products/{domain.product.pk}/capabilities/")


@when(
    parsers.parse('I view the capability "{capability_name}"'),
    target_fixture="detail_response",
)
def view_capability(
    client: Client, db: Any, capability_name: str, current_product: dict
) -> HttpResponse:
    """View a capability (via edit page which shows capability info)."""
    subdomain = current_product.get("subdomain")
    capability = Capability.objects.get(name=capability_name, subdomain=subdomain)
    domain = subdomain.domain
    return client.get(
        f"/products/{domain.product.pk}/domains/{domain.pk}/subdomains/{subdomain.pk}/capabilities/{capability.pk}/edit/"
    )


@when(
    parsers.parse('I update the capability "{capability_name}" with name "{new_name}"'),
    target_fixture="update_response",
)
def update_capability_name(
    client: Client, db: Any, capability_name: str, new_name: str, current_product: dict
) -> HttpResponse:
    """Update capability name."""
    subdomain = current_product.get("subdomain")
    capability = Capability.objects.get(name=capability_name, subdomain=subdomain)
    domain = subdomain.domain
    return client.post(
        f"/products/{domain.product.pk}/domains/{domain.pk}/subdomains/{subdomain.pk}/capabilities/{capability.pk}/edit/",
        {"name": new_name, "description": capability.description},
        follow=True,
    )


@when(
    parsers.parse('I update the capability "{capability_name}" with description "{description}"'),
    target_fixture="update_response",
)
def update_capability_description(
    client: Client, db: Any, capability_name: str, description: str, current_product: dict
) -> HttpResponse:
    """Update capability description."""
    subdomain = current_product.get("subdomain")
    capability = Capability.objects.get(name=capability_name, subdomain=subdomain)
    domain = subdomain.domain
    return client.post(
        f"/products/{domain.product.pk}/domains/{domain.pk}/subdomains/{subdomain.pk}/capabilities/{capability.pk}/edit/",
        {"name": capability.name, "description": description},
        follow=True,
    )


@when(
    parsers.parse('I delete the capability "{capability_name}"'),
    target_fixture="delete_response",
)
def delete_capability(
    client: Client, db: Any, capability_name: str, current_product: dict
) -> HttpResponse:
    """Delete a capability."""
    subdomain = current_product.get("subdomain")
    capability = Capability.objects.get(name=capability_name, subdomain=subdomain)
    domain = subdomain.domain
    return client.post(
        f"/products/{domain.product.pk}/domains/{domain.pk}/subdomains/{subdomain.pk}/capabilities/{capability.pk}/delete/",
        follow=True,
    )


@then(parsers.parse('the capability "{capability_name}" exists in subdomain "{subdomain_name}"'))
def capability_exists(
    db: Any, capability_name: str, subdomain_name: str, current_product: dict
) -> None:
    """Verify capability exists."""
    domain = current_product.get("domain")
    subdomain = SubDomain.objects.get(name=subdomain_name, domain=domain)
    assert Capability.objects.filter(subdomain=subdomain, name=capability_name).exists()


@then(
    parsers.parse(
        'the capability "{capability_name}" no longer exists in subdomain "{subdomain_name}"'
    )
)
def capability_not_exists(
    db: Any, capability_name: str, subdomain_name: str, current_product: dict
) -> None:
    """Verify capability does not exist."""
    domain = current_product.get("domain")
    subdomain = SubDomain.objects.get(name=subdomain_name, domain=domain)
    assert not Capability.objects.filter(subdomain=subdomain, name=capability_name).exists()


@then(parsers.parse('the capability "{capability_name}" has description "{description}"'))
def capability_has_description(
    db: Any, capability_name: str, description: str, current_product: dict
) -> None:
    """Verify capability has specific description."""
    subdomain = current_product.get("subdomain")
    capability = Capability.objects.get(name=capability_name, subdomain=subdomain)
    assert capability.description == description


@then(parsers.parse('I see the error "{error_message}"'))
def see_error_message(create_response: HttpResponse, error_message: str) -> None:
    """Verify error message is displayed."""
    content = create_response.content.decode()
    assert error_message in content


@then(parsers.parse("I see {count:d} capabilities"))
def see_capability_count(list_response: HttpResponse, count: int) -> None:
    """Verify number of capabilities displayed."""
    import re

    content = list_response.content.decode()
    # Count table rows in the capability list (hover pattern for table rows)
    row_count = len(re.findall(r'<tr class="hover">', content))
    assert row_count == count


@then(parsers.parse('I see the capability name "{capability_name}"'))
def see_capability_name(detail_response: HttpResponse, capability_name: str) -> None:
    """Verify capability name is displayed."""
    content = detail_response.content.decode()
    assert capability_name in content


@then(parsers.parse('I see the capability description "{description}"'))
def see_capability_description(detail_response: HttpResponse, description: str) -> None:
    """Verify capability description is displayed."""
    content = detail_response.content.decode()
    assert description in content

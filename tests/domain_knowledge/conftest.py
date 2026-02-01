"""Shared fixtures and step definitions for Domain Knowledge tests."""

from typing import Any

import pytest
from django.test import Client
from pytest_bdd import given, parsers

from knowledge.models import Capability, Domain, SubDomain
from users.models import Product, ProductMembership, User


@pytest.fixture
def current_product() -> dict[str, Any]:
    """Store the current product being tested."""
    return {}


@given(parsers.parse('I am logged in as a product manager of "{product_name}"'))
def logged_in_as_product_manager(
    client: Client, db: Any, product_name: str, current_product: dict[str, Any]
) -> None:
    """Create and log in as a product manager."""
    product, _ = Product.objects.get_or_create(
        name=product_name, defaults={"is_active": True}
    )
    current_product["product"] = product

    manager, _ = User.objects.get_or_create(
        username="manager",
        defaults={"is_staff": True},
    )
    if not manager.has_usable_password():
        manager.set_password("managerpass")
        manager.save()

    ProductMembership.objects.get_or_create(
        user=manager,
        product=product,
        defaults={"role": ProductMembership.Role.MANAGER},
    )

    client.force_login(manager)


@given(parsers.parse('the domain "{domain_name}" exists in "{product_name}"'))
def domain_exists_in_product(
    db: Any, domain_name: str, product_name: str, current_product: dict[str, Any]
) -> Domain:
    """Create a domain in a product."""
    product, _ = Product.objects.get_or_create(name=product_name, defaults={"is_active": True})
    current_product["product"] = product
    domain, _ = Domain.objects.get_or_create(
        product=product,
        name=domain_name,
        defaults={"description": ""},
    )
    current_product["domain"] = domain
    return domain


@given(
    parsers.parse(
        'the domain "{domain_name}" exists in "{product_name}" with description "{description}"'
    )
)
def domain_exists_with_description(
    db: Any, domain_name: str, product_name: str, description: str, current_product: dict[str, Any]
) -> Domain:
    """Create a domain with description."""
    product, _ = Product.objects.get_or_create(name=product_name, defaults={"is_active": True})
    current_product["product"] = product
    domain, _ = Domain.objects.update_or_create(
        product=product,
        name=domain_name,
        defaults={"description": description},
    )
    current_product["domain"] = domain
    return domain


@given(parsers.parse('the subdomain "{subdomain_name}" exists in domain "{domain_name}"'))
def subdomain_exists_in_domain(
    db: Any, subdomain_name: str, domain_name: str, current_product: dict[str, Any]
) -> SubDomain:
    """Create a subdomain in a domain."""
    product = current_product.get("product")
    if not product:
        raise ValueError("Product context required - ensure a product step runs before this step")
    domain = Domain.objects.get(product=product, name=domain_name)
    subdomain, _ = SubDomain.objects.get_or_create(
        domain=domain,
        name=subdomain_name,
        defaults={"description": ""},
    )
    current_product["domain"] = domain
    current_product["subdomain"] = subdomain
    return subdomain


@given(
    parsers.parse(
        'the subdomain "{subdomain_name}" exists in domain "{domain_name}" with description "{description}"'
    )
)
def subdomain_exists_with_description(
    db: Any, subdomain_name: str, domain_name: str, description: str, current_product: dict[str, Any]
) -> SubDomain:
    """Create a subdomain with description."""
    product = current_product.get("product")
    if not product:
        raise ValueError("Product context required - ensure a product step runs before this step")
    domain = Domain.objects.get(product=product, name=domain_name)
    subdomain, _ = SubDomain.objects.update_or_create(
        domain=domain,
        name=subdomain_name,
        defaults={"description": description},
    )
    current_product["domain"] = domain
    current_product["subdomain"] = subdomain
    return subdomain


@given(parsers.parse('the capability "{capability_name}" exists in subdomain "{subdomain_name}"'))
def capability_exists_in_subdomain(
    db: Any, capability_name: str, subdomain_name: str, current_product: dict[str, Any]
) -> Capability:
    """Create a capability in a subdomain."""
    domain = current_product.get("domain")
    if not domain:
        raise ValueError("Domain context required - ensure a domain step runs before this step")
    subdomain = SubDomain.objects.get(domain=domain, name=subdomain_name)
    capability, _ = Capability.objects.get_or_create(
        subdomain=subdomain,
        name=capability_name,
        defaults={"description": ""},
    )
    current_product["subdomain"] = subdomain
    current_product["capability"] = capability
    return capability


@given(
    parsers.parse(
        'the capability "{capability_name}" exists in subdomain "{subdomain_name}" with description "{description}"'
    )
)
def capability_exists_with_description(
    db: Any, capability_name: str, subdomain_name: str, description: str, current_product: dict[str, Any]
) -> Capability:
    """Create a capability with description."""
    domain = current_product.get("domain")
    if not domain:
        raise ValueError("Domain context required - ensure a domain step runs before this step")
    subdomain = SubDomain.objects.get(domain=domain, name=subdomain_name)
    capability, _ = Capability.objects.update_or_create(
        subdomain=subdomain,
        name=capability_name,
        defaults={"description": description},
    )
    current_product["subdomain"] = subdomain
    current_product["capability"] = capability
    return capability


@given(parsers.parse('the following domains exist in "{product_name}":'))
def domains_exist_in_product(
    db: Any, product_name: str, datatable: list[list[str]], current_product: dict[str, Any]
) -> None:
    """Create multiple domains from a data table."""
    product, _ = Product.objects.get_or_create(name=product_name, defaults={"is_active": True})
    current_product["product"] = product
    for row in datatable[1:]:  # Skip header row
        Domain.objects.get_or_create(
            product=product,
            name=row[0],
            defaults={"description": ""},
        )


@given(parsers.parse('the following subdomains exist in domain "{domain_name}":'))
def subdomains_exist_in_domain(
    db: Any, domain_name: str, datatable: list[list[str]], current_product: dict[str, Any]
) -> None:
    """Create multiple subdomains from a data table."""
    product = current_product.get("product")
    if not product:
        raise ValueError("Product context required - ensure a product step runs before this step")
    domain = Domain.objects.get(product=product, name=domain_name)
    current_product["domain"] = domain
    for row in datatable[1:]:  # Skip header row
        SubDomain.objects.get_or_create(
            domain=domain,
            name=row[0],
            defaults={"description": ""},
        )


@given(parsers.parse('the following capabilities exist in subdomain "{subdomain_name}":'))
def capabilities_exist_in_subdomain(
    db: Any, subdomain_name: str, datatable: list[list[str]], current_product: dict[str, Any]
) -> None:
    """Create multiple capabilities from a data table."""
    domain = current_product.get("domain")
    if not domain:
        raise ValueError("Domain context required - ensure a domain step runs before this step")
    subdomain = SubDomain.objects.get(domain=domain, name=subdomain_name)
    current_product["subdomain"] = subdomain
    for row in datatable[1:]:  # Skip header row
        Capability.objects.get_or_create(
            subdomain=subdomain,
            name=row[0],
            defaults={"description": ""},
        )

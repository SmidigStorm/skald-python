from django.urls import path

from . import views

app_name = "knowledge"

urlpatterns = [
    # Domain URLs
    path(
        "products/<int:product_id>/domains/",
        views.DomainListView.as_view(),
        name="domain_list",
    ),
    path(
        "products/<int:product_id>/domains/new/",
        views.DomainCreateView.as_view(),
        name="domain_create",
    ),
    path(
        "products/<int:product_id>/domains/<int:domain_id>/edit/",
        views.DomainUpdateView.as_view(),
        name="domain_update",
    ),
    path(
        "products/<int:product_id>/domains/<int:domain_id>/delete/",
        views.DomainDeleteView.as_view(),
        name="domain_delete",
    ),
    # SubDomain URLs
    path(
        "products/<int:product_id>/domains/<int:domain_id>/subdomains/",
        views.SubDomainListView.as_view(),
        name="subdomain_list",
    ),
    path(
        "products/<int:product_id>/domains/<int:domain_id>/subdomains/new/",
        views.SubDomainCreateView.as_view(),
        name="subdomain_create",
    ),
    path(
        "products/<int:product_id>/domains/<int:domain_id>/subdomains/<int:subdomain_id>/edit/",
        views.SubDomainUpdateView.as_view(),
        name="subdomain_update",
    ),
    path(
        "products/<int:product_id>/domains/<int:domain_id>/subdomains/<int:subdomain_id>/delete/",
        views.SubDomainDeleteView.as_view(),
        name="subdomain_delete",
    ),
    # Capability URLs
    path(
        "products/<int:product_id>/domains/<int:domain_id>/subdomains/<int:subdomain_id>/capabilities/",
        views.CapabilityListView.as_view(),
        name="capability_list",
    ),
    path(
        "products/<int:product_id>/domains/<int:domain_id>/subdomains/<int:subdomain_id>/capabilities/new/",
        views.CapabilityCreateView.as_view(),
        name="capability_create",
    ),
    path(
        "products/<int:product_id>/domains/<int:domain_id>/subdomains/<int:subdomain_id>/capabilities/<int:capability_id>/edit/",
        views.CapabilityUpdateView.as_view(),
        name="capability_update",
    ),
    path(
        "products/<int:product_id>/domains/<int:domain_id>/subdomains/<int:subdomain_id>/capabilities/<int:capability_id>/delete/",
        views.CapabilityDeleteView.as_view(),
        name="capability_delete",
    ),
]

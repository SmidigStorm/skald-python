from django.contrib import messages
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .mixins import ProductAccessMixin, ProductEditMixin
from .models import Capability, Domain, SubDomain

# =============================================================================
# Domain Views
# =============================================================================


class DomainListView(ProductAccessMixin, ListView):
    """List all domains in a product."""

    model = Domain
    template_name = "knowledge/domain_list.html"
    context_object_name = "domains"

    def get_queryset(self):
        return Domain.objects.filter(product=self.product)


class DomainCreateView(ProductEditMixin, CreateView):
    """Create a new domain in a product."""

    model = Domain
    template_name = "knowledge/domain_form.html"
    fields = ["name", "description"]

    def form_valid(self, form):
        form.instance.product = self.product
        try:
            with transaction.atomic():
                return super().form_valid(form)
        except IntegrityError:
            form.add_error("name", "A domain with this name already exists")
            return self.form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, f'Domain "{self.object.name}" created.')
        return reverse("knowledge:domain_list", kwargs={"product_id": self.product.pk})


class DomainUpdateView(ProductEditMixin, UpdateView):
    """Update a domain."""

    model = Domain
    template_name = "knowledge/domain_form.html"
    fields = ["name", "description"]
    pk_url_kwarg = "domain_id"

    def get_queryset(self):
        return Domain.objects.filter(product=self.product)

    def form_valid(self, form):
        try:
            with transaction.atomic():
                return super().form_valid(form)
        except IntegrityError:
            form.add_error("name", "A domain with this name already exists")
            return self.form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, f'Domain "{self.object.name}" updated.')
        return reverse("knowledge:domain_list", kwargs={"product_id": self.product.pk})


class DomainDeleteView(ProductEditMixin, DeleteView):
    """Delete a domain (cascades to subdomains and capabilities)."""

    model = Domain
    template_name = "knowledge/domain_confirm_delete.html"
    pk_url_kwarg = "domain_id"

    def get_queryset(self):
        return Domain.objects.filter(product=self.product)

    def get_success_url(self):
        messages.success(self.request, f'Domain "{self.object.name}" deleted.')
        return reverse("knowledge:domain_list", kwargs={"product_id": self.product.pk})


# =============================================================================
# SubDomain Views
# =============================================================================


class SubDomainListView(ProductAccessMixin, ListView):
    """List all subdomains in a domain."""

    model = SubDomain
    template_name = "knowledge/subdomain_list.html"
    context_object_name = "subdomains"

    def get_queryset(self):
        domain_id = self.kwargs.get("domain_id")
        return SubDomain.objects.filter(domain_id=domain_id, domain__product=self.product)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["domain"] = get_object_or_404(
            Domain, pk=self.kwargs.get("domain_id"), product=self.product
        )
        context["all_domains"] = Domain.objects.filter(product=self.product)
        return context


class SubDomainCreateView(ProductEditMixin, CreateView):
    """Create a new subdomain in a domain."""

    model = SubDomain
    template_name = "knowledge/subdomain_form.html"
    fields = ["name", "description"]

    def get_domain(self):
        if not hasattr(self, "_domain"):
            self._domain = get_object_or_404(
                Domain, pk=self.kwargs.get("domain_id"), product=self.product
            )
        return self._domain

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["domain"] = self.get_domain()
        context["all_domains"] = Domain.objects.filter(product=self.product)
        return context

    def form_valid(self, form):
        form.instance.domain = self.get_domain()
        try:
            with transaction.atomic():
                return super().form_valid(form)
        except IntegrityError:
            form.add_error("name", "A subdomain with this name already exists in this domain")
            return self.form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, f'SubDomain "{self.object.name}" created.')
        return reverse(
            "knowledge:subdomain_list",
            kwargs={"product_id": self.product.pk, "domain_id": self.get_domain().pk},
        )


class SubDomainUpdateView(ProductEditMixin, UpdateView):
    """Update a subdomain."""

    model = SubDomain
    template_name = "knowledge/subdomain_form.html"
    fields = ["name", "description"]
    pk_url_kwarg = "subdomain_id"

    def get_domain(self):
        if not hasattr(self, "_domain"):
            self._domain = get_object_or_404(
                Domain, pk=self.kwargs.get("domain_id"), product=self.product
            )
        return self._domain

    def get_queryset(self):
        return SubDomain.objects.filter(domain__product=self.product)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["domain"] = self.get_domain()
        context["all_domains"] = Domain.objects.filter(product=self.product)
        return context

    def form_valid(self, form):
        try:
            with transaction.atomic():
                return super().form_valid(form)
        except IntegrityError:
            form.add_error("name", "A subdomain with this name already exists in this domain")
            return self.form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, f'SubDomain "{self.object.name}" updated.')
        return reverse(
            "knowledge:subdomain_list",
            kwargs={"product_id": self.product.pk, "domain_id": self.get_domain().pk},
        )


class SubDomainDeleteView(ProductEditMixin, DeleteView):
    """Delete a subdomain (cascades to capabilities)."""

    model = SubDomain
    template_name = "knowledge/subdomain_confirm_delete.html"
    pk_url_kwarg = "subdomain_id"

    def get_domain(self):
        if not hasattr(self, "_domain"):
            self._domain = get_object_or_404(
                Domain, pk=self.kwargs.get("domain_id"), product=self.product
            )
        return self._domain

    def get_queryset(self):
        return SubDomain.objects.filter(domain__product=self.product)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["domain"] = self.get_domain()
        context["all_domains"] = Domain.objects.filter(product=self.product)
        return context

    def get_success_url(self):
        messages.success(self.request, f'SubDomain "{self.object.name}" deleted.')
        return reverse(
            "knowledge:subdomain_list",
            kwargs={"product_id": self.product.pk, "domain_id": self.get_domain().pk},
        )


# =============================================================================
# Capability Views
# =============================================================================


class CapabilityListView(ProductAccessMixin, ListView):
    """List all capabilities in a subdomain."""

    model = Capability
    template_name = "knowledge/capability_list.html"
    context_object_name = "capabilities"

    def get_queryset(self):
        subdomain_id = self.kwargs.get("subdomain_id")
        return Capability.objects.filter(
            subdomain_id=subdomain_id, subdomain__domain__product=self.product
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        domain = get_object_or_404(
            Domain, pk=self.kwargs.get("domain_id"), product=self.product
        )
        subdomain = get_object_or_404(
            SubDomain, pk=self.kwargs.get("subdomain_id"), domain=domain
        )
        context["domain"] = domain
        context["subdomain"] = subdomain
        context["all_subdomains"] = SubDomain.objects.filter(domain=domain)
        return context


class CapabilityCreateView(ProductEditMixin, CreateView):
    """Create a new capability in a subdomain."""

    model = Capability
    template_name = "knowledge/capability_form.html"
    fields = ["name", "description"]

    def get_domain(self):
        if not hasattr(self, "_domain"):
            self._domain = get_object_or_404(
                Domain, pk=self.kwargs.get("domain_id"), product=self.product
            )
        return self._domain

    def get_subdomain(self):
        if not hasattr(self, "_subdomain"):
            self._subdomain = get_object_or_404(
                SubDomain, pk=self.kwargs.get("subdomain_id"), domain=self.get_domain()
            )
        return self._subdomain

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["domain"] = self.get_domain()
        context["subdomain"] = self.get_subdomain()
        context["all_subdomains"] = SubDomain.objects.filter(domain=self.get_domain())
        return context

    def form_valid(self, form):
        form.instance.subdomain = self.get_subdomain()
        try:
            with transaction.atomic():
                return super().form_valid(form)
        except IntegrityError:
            form.add_error("name", "A capability with this name already exists in this subdomain")
            return self.form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, f'Capability "{self.object.name}" created.')
        return reverse(
            "knowledge:capability_list",
            kwargs={
                "product_id": self.product.pk,
                "domain_id": self.get_domain().pk,
                "subdomain_id": self.get_subdomain().pk,
            },
        )


class CapabilityUpdateView(ProductEditMixin, UpdateView):
    """Update a capability."""

    model = Capability
    template_name = "knowledge/capability_form.html"
    fields = ["name", "description"]
    pk_url_kwarg = "capability_id"

    def get_domain(self):
        if not hasattr(self, "_domain"):
            self._domain = get_object_or_404(
                Domain, pk=self.kwargs.get("domain_id"), product=self.product
            )
        return self._domain

    def get_subdomain(self):
        if not hasattr(self, "_subdomain"):
            self._subdomain = get_object_or_404(
                SubDomain, pk=self.kwargs.get("subdomain_id"), domain=self.get_domain()
            )
        return self._subdomain

    def get_queryset(self):
        return Capability.objects.filter(subdomain__domain__product=self.product)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["domain"] = self.get_domain()
        context["subdomain"] = self.get_subdomain()
        context["all_subdomains"] = SubDomain.objects.filter(domain=self.get_domain())
        return context

    def form_valid(self, form):
        try:
            with transaction.atomic():
                return super().form_valid(form)
        except IntegrityError:
            form.add_error("name", "A capability with this name already exists in this subdomain")
            return self.form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, f'Capability "{self.object.name}" updated.')
        return reverse(
            "knowledge:capability_list",
            kwargs={
                "product_id": self.product.pk,
                "domain_id": self.get_domain().pk,
                "subdomain_id": self.get_subdomain().pk,
            },
        )


class CapabilityDeleteView(ProductEditMixin, DeleteView):
    """Delete a capability."""

    model = Capability
    template_name = "knowledge/capability_confirm_delete.html"
    pk_url_kwarg = "capability_id"

    def get_domain(self):
        if not hasattr(self, "_domain"):
            self._domain = get_object_or_404(
                Domain, pk=self.kwargs.get("domain_id"), product=self.product
            )
        return self._domain

    def get_subdomain(self):
        if not hasattr(self, "_subdomain"):
            self._subdomain = get_object_or_404(
                SubDomain, pk=self.kwargs.get("subdomain_id"), domain=self.get_domain()
            )
        return self._subdomain

    def get_queryset(self):
        return Capability.objects.filter(subdomain__domain__product=self.product)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["domain"] = self.get_domain()
        context["subdomain"] = self.get_subdomain()
        context["all_subdomains"] = SubDomain.objects.filter(domain=self.get_domain())
        return context

    def get_success_url(self):
        messages.success(self.request, f'Capability "{self.object.name}" deleted.')
        return reverse(
            "knowledge:capability_list",
            kwargs={
                "product_id": self.product.pk,
                "domain_id": self.get_domain().pk,
                "subdomain_id": self.get_subdomain().pk,
            },
        )

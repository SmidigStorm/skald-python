from django.contrib import admin

from .models import Capability, Domain, SubDomain


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ["name", "product", "created_at"]
    list_filter = ["product"]
    search_fields = ["name", "description"]
    ordering = ["product", "name"]


@admin.register(SubDomain)
class SubDomainAdmin(admin.ModelAdmin):
    list_display = ["name", "domain", "get_product", "created_at"]
    list_filter = ["domain__product", "domain"]
    search_fields = ["name", "description"]
    ordering = ["domain__product", "domain", "name"]

    @admin.display(description="Product")
    def get_product(self, obj):
        return obj.domain.product


@admin.register(Capability)
class CapabilityAdmin(admin.ModelAdmin):
    list_display = ["name", "subdomain", "get_domain", "get_product", "created_at"]
    list_filter = ["subdomain__domain__product", "subdomain__domain", "subdomain"]
    search_fields = ["name", "description"]
    ordering = ["subdomain__domain__product", "subdomain__domain", "subdomain", "name"]

    @admin.display(description="Domain")
    def get_domain(self, obj):
        return obj.subdomain.domain

    @admin.display(description="Product")
    def get_product(self, obj):
        return obj.subdomain.domain.product

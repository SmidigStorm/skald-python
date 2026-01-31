from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Product, ProductMembership, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "created_at"]
    list_filter = ["is_active"]
    search_fields = ["name"]


@admin.register(ProductMembership)
class ProductMembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "role", "created_at"]
    list_filter = ["role", "product"]
    search_fields = ["user__username", "product__name"]

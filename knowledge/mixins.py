from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from users.models import Product, ProductMembership


class ProductAccessMixin(LoginRequiredMixin):
    """Mixin that checks user has access to the product.

    Expects 'product_id' in URL kwargs.
    Sets self.product for use in views.
    """

    # Roles that can access (override in subclass for different permissions)
    allowed_roles: list[str] = [
        ProductMembership.Role.MANAGER,
        ProductMembership.Role.CONTRIBUTOR,
        ProductMembership.Role.VIEWER,
    ]

    def dispatch(self, request, *args, **kwargs):
        # Get product from URL
        product_id = kwargs.get("product_id")
        self.product = get_object_or_404(Product, pk=product_id, is_active=True)

        # Check user has membership with allowed role
        if not request.user.is_superuser:
            has_access = ProductMembership.objects.filter(
                user=request.user,
                product=self.product,
                role__in=self.allowed_roles,
            ).exists()

            if not has_access:
                raise PermissionDenied("You do not have access to this product.")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = self.product
        return context


class ProductEditMixin(ProductAccessMixin):
    """Mixin for views that require edit access (Manager or Contributor)."""

    allowed_roles = [
        ProductMembership.Role.MANAGER,
        ProductMembership.Role.CONTRIBUTOR,
    ]


class ProductManagerMixin(ProductAccessMixin):
    """Mixin for views that require manager access only."""

    allowed_roles = [
        ProductMembership.Role.MANAGER,
    ]

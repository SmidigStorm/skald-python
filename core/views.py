from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["memberships"] = (
            self.request.user.product_memberships.select_related("product")
            .filter(product__is_active=True)
            .order_by("product__name")
        )
        return context

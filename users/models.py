from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model extending Django's AbstractUser."""

    pass


class Product(models.Model):
    """Tenant boundary. All domain data is scoped to a product."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class ProductMembership(models.Model):
    """Links a user to a product with a specific role."""

    class Role(models.TextChoices):
        MANAGER = "manager", "Product Manager"
        CONTRIBUTOR = "contributor", "Product Contributor"
        VIEWER = "viewer", "Product Viewer"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="product_memberships",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(max_length=20, choices=Role.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "product"]

    def __str__(self) -> str:
        return f"{self.user.username} - {self.product.name} ({self.get_role_display()})"

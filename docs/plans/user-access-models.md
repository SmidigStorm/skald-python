# User Access Domain Models

## Summary

Implement the User Access domain database models (User, Product, ProductMembership) using Django's built-in auth system with minimal extensions.

## Requirements

From `docs/domains/user-access/requirements/`:

- [ ] `user-login.feature` - Username/password authentication
- [ ] `user-management.feature` - System admins create/delete users
- [ ] `product-management.feature` - Create/deactivate products
- [ ] `role-assignment.feature` - Assign users to products with roles
- [ ] `authorization.feature` - Role-based access control

## Architecture Approach

**Extend Django's auth** - Use `AbstractUser` for full compatibility with Django's authentication, sessions, and admin. Keep it simple.

## Decisions

| Decision | Rationale |
|----------|-----------|
| `Role` as TextChoices | Simple, no extra table, only 3 per-product values |
| System Admin = `is_superuser` | Uses Django's built-in, no custom code needed |
| `unique_together` on membership | Enforces one role per user per product |
| Single `users` app | All User Access models in one place |
| Product `is_active` blocks access | Deactivated products are inaccessible to members |

## Implementation Steps

### Step 1: Create the users app

```bash
python manage.py startapp users
```

**Files created:**
- `users/__init__.py`
- `users/models.py`
- `users/admin.py`
- `users/apps.py`

### Step 2: Define models in `users/models.py`

```python
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

    def __str__(self):
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

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.get_role_display()})"
```

### Step 3: Configure settings

In `skald_project/settings.py`:

```python
INSTALLED_APPS = [
    # ... existing apps ...
    "users",
]

AUTH_USER_MODEL = "users.User"
```

### Step 4: Register admin in `users/admin.py`

```python
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
```

### Step 5: Create and run migrations

```bash
python manage.py makemigrations users
python manage.py migrate
```

### Step 6: Create superuser for testing

```bash
python manage.py createsuperuser
```

## Acceptance Criteria

- [ ] User can log in with username/password
- [ ] Superuser can create/delete users via admin
- [ ] Superuser can create/deactivate products via admin
- [ ] Superuser can assign users to products with roles via admin
- [ ] Each user can only have one role per product

## Open Questions

- Validation rules for username/password (deferred - using Django defaults)
- What distinguishes Product Manager from Contributor? (deferred - same permissions for now)

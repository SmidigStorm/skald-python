# User Login, Logout, and Home Page

**Completed: 2026-01-31**

## Summary

Implement user-facing authentication (login/logout) and a home page that shows the user's assigned products. Uses Django's built-in auth views for login/logout.

## Requirements

- [x] **User Login**: Successful login redirects to home page
- [x] **User Login**: Invalid credentials show "Login failed" error
- [x] **User Login**: Unauthenticated users redirected to login
- [x] **User Logout**: Logout terminates session and redirects to login
- [x] **Home Page**: Shows list of user's assigned products
- [x] **Home Page**: Empty state for users with no products
- [x] **Home Page**: Clicking product navigates to domain list
- [x] **Authorization**: Normal users cannot access Django admin

## Architecture Approach

**Minimal changes using Django's built-in auth views:**
- `LoginView` and `LogoutView` from `django.contrib.auth.views`
- Custom `HomeView` for the landing page
- Login/logout in `users` app (authentication-related)
- Home page in new `core` app (cross-cutting concern)
- Shared base template in `core/templates/base.html` for DRY CSS

## Codebase Patterns

- **Mixins**: `LoginRequiredMixin` pattern from `knowledge/mixins.py`
- **Templates**: Block structure from `core/templates/base.html`
- **Product query**: `ProductMembership.objects.filter(user=request.user)`

## Implementation Steps

### Step 1: Add auth settings

**Files:**
- `skald_project/settings.py` - Add LOGIN_URL, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL

```python
LOGIN_URL = reverse_lazy("users:login")
LOGIN_REDIRECT_URL = reverse_lazy("core:home")
LOGOUT_REDIRECT_URL = reverse_lazy("users:login")
```

### Step 2: Create core app

**Files:**
- `core/__init__.py` - Empty
- `core/apps.py` - Django app config
- `core/views.py` - HomeView
- `core/urls.py` - URL routing

### Step 3: Create users URLs

**Files:**
- `users/urls.py` - New file with login/logout routes

### Step 4: Update main URL router

**Files:**
- `skald_project/urls.py` - Include users and core URLs

### Step 5: Create login template

**Files:**
- `users/templates/registration/login.html`

### Step 6: Create home template

**Files:**
- `core/templates/core/home.html`

### Step 7: Add core to INSTALLED_APPS

**Files:**
- `skald_project/settings.py` - Add "core" to INSTALLED_APPS

### Step 8 (Added): Create shared base template

**Files:**
- `core/templates/base.html` - Shared CSS and layout
- Updated `knowledge/templates/knowledge/base.html` to extend base.html

## Acceptance Criteria

- [x] User can visit `/login/` and see login form
- [x] Valid credentials redirect to `/` (home page)
- [x] Invalid credentials show "Login failed" on login page
- [x] Home page lists user's products
- [x] Clicking product goes to `/products/<id>/domains/`
- [x] User with no products sees "You are not assigned to any products"
- [x] Logout at `/logout/` terminates session and redirects to `/login/`
- [x] Accessing `/` without login redirects to `/login/`
- [x] Non-staff users accessing `/admin/` see admin login (not app content)

## Decisions Made

- **Login/logout in users app**: Authentication is user-related
- **Home in core app**: Cross-cutting landing page, not user-specific
- **Django built-in views**: Minimal code, standard behavior, secure by default
- **Simple product list**: No role display, just product names as links
- **Shared base template**: Created `core/templates/base.html` to eliminate CSS duplication
- **reverse_lazy for URLs**: Used instead of hardcoded strings to avoid magic strings

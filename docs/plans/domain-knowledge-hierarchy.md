# Domain Knowledge Hierarchy Implementation

## Summary
Implement Domain, SubDomain, and Capability models with custom Django views and per-model authorization. Product Managers can manage the domain hierarchy within their products.

## Requirements
- domain-management.feature (8 scenarios): CRUD for domains, scoped to Product
- subdomain-management.feature (9 scenarios): CRUD for subdomains, scoped to Domain
- capability-management.feature (8 scenarios): CRUD for capabilities, scoped to SubDomain

## Architecture Approach
- **New app**: `knowledge` (follows domain-per-app pattern)
- **Views**: Custom Django views with templates (prototype)
- **Authorization**: Per-model check via ProductMembership role
- **No API**: REST API deferred to later iteration
- **No tests**: Tests deferred until feature is stable

## Codebase Patterns to Follow
- Model structure: `users/models.py` (name, description, timestamps, `__str__`)
- ForeignKey: `on_delete=CASCADE`, explicit `related_name`
- Unique constraints: `unique_together` in Meta class

## Implementation Steps

### Step 1: Create knowledge app
```bash
python manage.py startapp knowledge
```
Add to `INSTALLED_APPS` in settings.py

### Step 2: Create models
**File**: `knowledge/models.py`
- Domain: name, description, product (FK), timestamps
- SubDomain: name, description, domain (FK), timestamps
- Capability: name, description, subdomain (FK), timestamps
- Unique constraints at parent level

### Step 3: Create authorization mixin
**File**: `knowledge/mixins.py`
- `ProductAccessMixin`: Check user has ProductMembership with appropriate role
- Returns 403 Forbidden if unauthorized

### Step 4: Create views
**File**: `knowledge/views.py`
- DomainListView, DomainCreateView, DomainUpdateView, DomainDeleteView
- SubDomainListView, SubDomainCreateView, SubDomainUpdateView, SubDomainDeleteView
- CapabilityListView, CapabilityCreateView, CapabilityUpdateView, CapabilityDeleteView

### Step 5: Create templates
**Directory**: `knowledge/templates/knowledge/`
- domain_list.html, domain_form.html, domain_confirm_delete.html
- subdomain_list.html, subdomain_form.html, subdomain_confirm_delete.html
- capability_list.html, capability_form.html, capability_confirm_delete.html

### Step 6: Wire up URLs
**Files**: `knowledge/urls.py`, `skald_project/urls.py`
- URL pattern: `/products/<product_id>/domains/...`

### Step 7: Run migrations
```bash
python manage.py makemigrations knowledge
python manage.py migrate
```

## Decisions Made
- **App location**: New `knowledge` app (not in `users`)
- **Authorization**: Per-model via ProductMembership.role check
- **Interface**: Views first, API later
- **Tests**: Deferred until feature stable

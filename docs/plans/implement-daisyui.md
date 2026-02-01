# Implement UI with DaisyUI

**Completed: 2026-02-01**

## Summary

Set up Tailwind CSS + DaisyUI integration for the Skald application using a Node.js build pipeline (following django-daisy patterns). This establishes the foundation for a consistent, themeable design system with sidebar navigation.

## Requirements

From `docs/domains/website/requirements/`:

- [ ] design-system.feature: DaisyUI component styling
- [ ] design-system.feature: Theme follows system preference
- [ ] design-system.feature: Manual theme switching with persistence
- [ ] design-system.feature: Cards as primary content container
- [ ] design-system.feature: Button visual hierarchy
- [ ] navigation.feature: Sidebar + main content layout
- [ ] navigation.feature: Breadcrumbs always visible
- [ ] navigation.feature: User info and logout in header
- [ ] forms.feature: DaisyUI form input styling

## Architecture Approach

**Chosen: django-daisy build pattern**

- Node.js + npm for Tailwind CLI build
- Tailwind CSS v4 with DaisyUI plugin
- CSS compiled to `static/css/` directory
- Theme switching via `data-theme` attribute + localStorage
- Custom Ubuntu font for typography

**Rationale:**
- Production-ready with CSS purging (~20KB vs ~300KB CDN)
- Full customization control
- Proven pattern from django-daisy reference
- Build only needed during development

## Codebase Patterns

From django-daisy reference:

- Theme detection: `docs/reference/django-daisy-main/django_daisy/templates/admin/base.html:13-58`
- Build config: `docs/reference/django-daisy-main/package.json`
- Tailwind v4 syntax: `docs/reference/django-daisy-main/build-styles/app.css`
- Sidebar layout: `docs/reference/django-daisy-main/django_daisy/templates/admin/base.html:111-142`
- Toast messages: `docs/reference/django-daisy-main/django_daisy/templates/admin/base.html:167-184`

## Implementation Steps

### Step 1: Set up Node.js build pipeline

**Implements**: Build infrastructure

**Files**:
- `package.json` - Create with tailwindcss, daisyui, @tailwindcss/cli dependencies
- `tailwind.config.js` - Configure content paths for Django templates
- `static/css/input.css` - Tailwind directives with DaisyUI plugin
- `.gitignore` - Add `node_modules/`, keep `static/css/output.css`

**Details**:
```json
// package.json
{
  "scripts": {
    "dev": "npx @tailwindcss/cli -i static/css/input.css -o static/css/output.css --watch",
    "build": "npx @tailwindcss/cli -i static/css/input.css -o static/css/output.css --minify"
  },
  "devDependencies": {
    "tailwindcss": "^4.1.13",
    "daisyui": "^5.1.10",
    "@tailwindcss/cli": "^4.1.13"
  }
}
```

```css
/* static/css/input.css - Tailwind v4 syntax */
@import "tailwindcss" source(none);
@plugin "daisyui" {
    themes: light --default, dark --prefersdark;
}
@source "../../**/templates/**/*.html";
```

### Step 2: Add custom fonts

**Implements**: design-system.feature (typography)

**Files**:
- `static/fonts/Ubuntu/` - Download Ubuntu font family (Regular, Medium, Bold)
- `static/css/input.css` - Add @font-face declarations

**Details**:
- Download from Google Fonts or use django-daisy's font files
- Define `body-font` font-face in CSS

### Step 3: Create new base template

**Implements**: design-system.feature, navigation.feature

**Files**:
- `core/templates/base.html` - Replace with DaisyUI version

**Template structure**:
```html
<!DOCTYPE html>
<html data-theme="">
<head>
    <script>
        /* Theme detection before page load */
        function getSystemColorScheme() { ... }
        document.documentElement.setAttribute('data-theme',
            localStorage.getItem('theme') || getSystemColorScheme()
        );
    </script>
    <link href="{% static 'css/output.css' %}" rel="stylesheet">
</head>
<body class="bg-base-200 min-h-screen">
    <div class="flex">
        <!-- Sidebar -->
        {% block sidebar %}
        <aside class="w-64 bg-base-100 min-h-screen p-4">
            {% block sidebar_content %}{% endblock %}
        </aside>
        {% endblock %}

        <!-- Main content -->
        <main class="flex-1 p-6">
            {% block breadcrumb %}{% endblock %}
            {% block content %}{% endblock %}
        </main>
    </div>

    <!-- Toast messages -->
    {% if messages %}
    <div class="toast toast-top toast-end">
        {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">{{ message }}</div>
        {% endfor %}
    </div>
    {% endif %}
</body>
</html>
```

### Step 4: Add theme switcher component

**Implements**: design-system.feature (theme switching)

**Files**:
- `core/templates/components/theme_switcher.html` - Theme dropdown partial
- `static/js/theme.js` - Theme switching logic (optional, can be inline)

**Details**:
- Dropdown with Light/Dark options
- Updates `data-theme` attribute on `<html>`
- Saves to localStorage
- Include in header/navbar area

### Step 5: Convert login page

**Implements**: forms.feature

**Files**:
- `users/templates/registration/login.html` - Convert to DaisyUI

**Component mapping**:
| Current | DaisyUI |
|---------|---------|
| `.card` | `card bg-base-100 shadow-xl` |
| `input[type="text"]` | `input input-bordered w-full` |
| `.btn` | `btn btn-primary` |
| `.errorlist` | `text-error text-sm` |

### Step 6: Convert home page with sidebar

**Implements**: navigation.feature, design-system.feature

**Files**:
- `core/templates/core/home.html` - Add sidebar, convert to DaisyUI

**Details**:
- Sidebar shows: Logo, product list, user info, logout
- Main content: Welcome message, product cards
- Use `card` component for products
- Breadcrumb: `breadcrumbs text-sm`

### Step 7: Create knowledge base template

**Implements**: Establishes pattern for knowledge app

**Files**:
- `knowledge/templates/knowledge/base.html` - Extend core base with knowledge sidebar

**Details**:
- Inherits from `core/base.html`
- Sidebar shows: Product name, Domains/SubDomains/Capabilities nav
- Pattern for all knowledge templates to follow

### Step 8: Convert domain list page

**Implements**: Proof of concept for knowledge pages

**Files**:
- `knowledge/templates/knowledge/domain_list.html` - Convert to DaisyUI

**Component mapping**:
| Current | DaisyUI |
|---------|---------|
| `.breadcrumb` | `breadcrumbs text-sm` |
| `.card` | `card bg-base-100 shadow` |
| `.btn` | `btn btn-primary btn-sm` |
| `.btn-danger` | `btn btn-error btn-sm` |
| `.empty-state` | `text-center py-10 text-base-content/60` |

### Step 9: Update Django settings

**Implements**: Static files configuration

**Files**:
- `skald_project/settings.py` - Add STATICFILES_DIRS

**Details**:
```python
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

## Acceptance Criteria

- [x] `npm run dev` watches and compiles CSS
- [x] `npm run build` produces minified CSS
- [x] Theme automatically matches system preference (light/dark)
- [x] User can manually switch theme via dropdown
- [x] Theme preference persists across page reloads (localStorage)
- [x] Login page displays with DaisyUI styling
- [x] Home page shows sidebar with navigation
- [x] Domain list page uses DaisyUI cards and buttons
- [x] All existing tests still pass (54/54)

## Open Questions (Resolved)

- ~~Should we add `django-widget-tweaks` for easier form field styling?~~ **Yes, added**
- ~~Do we want to add FontAwesome icons (like django-daisy) or keep iconless for now?~~ **Yes, added FontAwesome 6.5.1 via CDN**

## Decisions Made

1. **Node.js build over CDN**: Better for production (smaller CSS, customizable)
2. **Skip HTMX for now**: Keep initial scope simple, add later
3. **localStorage for theme**: No server-side persistence needed
4. **Custom Ubuntu font**: Matches django-daisy reference, better typography
5. **Main app only**: Don't restyle Django admin (Option A from discussion)

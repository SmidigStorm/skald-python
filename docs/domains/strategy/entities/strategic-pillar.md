# StrategicPillar

A high-level theme or focus area that guides product direction. Strategic pillars are independent of OKRs and time horizons.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | Pillar name (e.g., "User Growth", "Platform Stability") |
| description | string | no | What this pillar means and why it matters |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Product | N:1 | The product this pillar guides |

## Notes

- Strategic pillars are independent concepts - not tied to Objectives
- They represent long-term themes that persist across time horizons
- Examples: "Developer Experience", "Enterprise Readiness", "Mobile First"

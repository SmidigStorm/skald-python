# SubDomain

A nested area within a domain. Sub-domains are where the actual modeling happens - they contain entities, capabilities, and glossary terms.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | Sub-domain name |
| description | string | no | Sub-domain description |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Domain | N:1 | A sub-domain belongs to one domain |
| contains | Entity | 1:N | A sub-domain contains multiple entities |
| contains | Capability | 1:N | A sub-domain contains multiple capabilities |
| contains | GlossaryTerm | 1:N | A sub-domain contains multiple glossary terms |

---

## Entity Model

Entities within a sub-domain are modeled in an object-oriented style with attributes, functions, and relationships.

### Entity Structure

| Field | Type | Description |
|-------|------|-------------|
| name | string | Entity name |
| description | string | Entity description |
| attributes | Attribute[] | Properties of the entity |
| functions | Function[] | Business rules / behaviors |
| relationships | Relationship[] | Connections to other entities |

### Attribute Structure

| Field | Type | Description |
|-------|------|-------------|
| name | string | Attribute name |
| type | string | Data type (string, number, boolean, date, etc.) |
| description | string | Attribute description |
| required | boolean | Whether the attribute is required |

### Function Structure

Business rules expressed as functions:

| Field | Type | Description |
|-------|------|-------------|
| name | string | Function name |
| description | string | What the function does (business rule) |
| parameters | Parameter[] | Input parameters (name, type, description) |
| return_type | string | What the function returns |

### Relationship Structure

| Field | Type | Description |
|-------|------|-------------|
| name | string | Relationship name (e.g., "places", "contains") |
| target | Entity | The entity this relationship points to |
| cardinality | enum | 1:1, 1:N, or N:M |
| attributes | Attribute[] | Properties on the relationship itself |

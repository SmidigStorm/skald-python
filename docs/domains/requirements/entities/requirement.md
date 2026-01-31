# Requirement

A capability need expressed as a user story or direct requirement ("The system shall..."). Requirements follow Example Mapping: they have rules (business logic) and examples (Gherkin scenarios).

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | yes | Format: `DOM-SUB-CAP-001` (derived from domain hierarchy) |
| name | string | yes | Short requirement name |
| description | string | yes | User story or "system shall" format |
| priority | enum | yes | MoSCoW: Must, Should, Could, Won't |
| status | enum | yes | Draft, Approved, Implemented |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | Capability | N:1 | Requirements belong to a capability |
| has | Rule | 1:N | Business rules for this requirement |
| has | OpenQuestion | 1:N | Unresolved ambiguities |
| solved by | BacklogItem | N:1 | Many requirements solved by one backlog item |
| links to | Entity | N:M | Wiki-style `[[Entity]]` links in description |

## ID Format

The requirement ID encodes its location in the domain hierarchy:

```
UAC-AUTH-LOG-001
│   │    │   └── Sequential number
│   │    └────── Capability: Login
│   └─────────── Sub-domain: Authentication
└─────────────── Domain: User Access
```

## Example

```markdown
**ID:** UAC-AUTH-LOG-001
**Name:** User Login
**Description:** As a [[User]], I want to login with my credentials so that I can access my [[Product]]s.
**Priority:** Must
**Status:** Draft
```

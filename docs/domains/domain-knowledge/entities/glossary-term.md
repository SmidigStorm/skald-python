# GlossaryTerm

A domain vocabulary definition. Part of the ubiquitous language that ensures everyone uses the same terms with the same meaning.

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | The term |
| definition | string | yes | What the term means in this domain |

## Relationships

| Relationship | Target | Cardinality | Description |
|--------------|--------|-------------|-------------|
| belongs to | SubDomain | N:1 | A glossary term belongs to one sub-domain |
| relates to | Entity | N:M | Terms can reference entities they describe |

## Examples

| Term | Definition |
|------|------------|
| Backlog Item | A unit of work that delivers value, prioritized in the backlog |
| Ubiquitous Language | Shared vocabulary used by all team members |
| Bounded Context | A boundary within which a domain model applies |

# Product Vision

## Target Customer

Product managers and developers who need AI assistance across the full product lifecycle - from idea to working code in production. Teams who want guidance, not just tools.

## Customer Problem

- Knowledge is scattered across tools and people's heads
- Priorities are unclear and constantly shifting
- Requirements are vague or tangled with implementation details
- Hard to separate "what we're building" from "how we'll build it"
- Tests are an afterthought, disconnected from specifications

## Value Proposition

Skald is an opinionated, AI-native product development platform. Unlike Jira (a blank canvas), Skald guides teams through a best-practice workflow. AI assistance is built into both the GUI and developer tools via MCP, so developers have full access to domain knowledge, requirements, and priorities while coding in Claude Code.

## Key Benefits

Two axes of success:

1. **Build the right thing** - validated understanding of what users actually need
2. **Build it right** - technical excellence through executable specifications and tests

## Product Principles

1. **Opinionated over flexible** - guide users through best practices, don't give them a blank canvas
2. **Executable specs, not documentation** - requirements should run as tests, not rot in a wiki
3. **Domain language everywhere** - ubiquitous language flows through UI, specs, and code

## Success Looks Like

Teams have a smooth, AI-assisted development flow where every step connects to the next:

**Domain Knowledge → Requirements → Initiatives → Code → Tests**

Nothing gets lost in translation. AI helps at each step without getting in the way. The domain model is the shared foundation that keeps everyone aligned.

---

## Domains

| Domain | Purpose |
|--------|---------|
| **User Access** | Multi-tenancy, users, products, roles |
| **Domain Knowledge** | Entities, relationships, ubiquitous language, documentation (Diataxis) |
| **Requirements** | BDD features, scenarios, executable specs |
| **Insights** | User research, Atomic UX observations |
| **Planning** | Releases, Backlog Items, Plans |
| **Architecture** | ADRs, tech stack, system design decisions |
| **Testing** | E2E tests tied to specifications |

## Methodology Foundations

| Area | Inspiration |
|------|-------------|
| Requirements & E2E Tests | BDD, ATDD, Specification by Example |
| Domain Knowledge | Domain-Driven Design, Wiki, OWL Ontology, Diataxis |
| User Insights | Atomic UX Design |
| Planning | Simple hierarchy: Release → Backlog Item → Plan |
| Architecture | Architecture Decision Records (ADRs) |
| Deployment | MinimalCD.org |

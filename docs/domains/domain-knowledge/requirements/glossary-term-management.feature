Feature: Glossary Term Management
  As a product manager
  I want to manage glossary terms within a subdomain
  So that my team uses consistent vocabulary across the product.

  Rule: Product managers can create glossary terms

    Scenario: Create a new glossary term
      Given I am logged in as a product manager of "Acme Project"
      And the domain "Planning" exists in "Acme Project"
      And the subdomain "Backlog" exists in domain "Planning"
      When I create a glossary term with:
        | name       | Backlog Item                                               |
        | definition | A unit of work that delivers value, prioritized in the backlog |
        | subdomain  | Backlog                                                    |
      Then the glossary term "Backlog Item" exists in subdomain "Backlog"

    Scenario: Glossary term names must be globally unique
      Given I am logged in as a product manager of "Acme Project"
      And the glossary term "Backlog Item" exists
      When I create a glossary term with name "Backlog Item"
      Then I see the error "A glossary term with this name already exists"

  Rule: Product managers can view glossary terms

    Scenario: View all glossary terms in a subdomain
      Given I am logged in as a product manager of "Acme Project"
      And the domain "Planning" exists in "Acme Project"
      And the subdomain "Backlog" exists in domain "Planning"
      And the following glossary terms exist in subdomain "Backlog":
        | name              |
        | Backlog Item      |
        | Sprint            |
        | Definition of Done |
      When I view the glossary terms in subdomain "Backlog"
      Then I see 3 glossary terms

    Scenario: View glossary term details
      Given I am logged in as a product manager of "Acme Project"
      And the glossary term "Backlog Item" exists with definition "A unit of work that delivers value"
      When I view the glossary term "Backlog Item"
      Then I see the glossary term name "Backlog Item"
      And I see the glossary term definition "A unit of work that delivers value"

  Rule: Product managers can update glossary terms

    Scenario: Update glossary term name
      Given I am logged in as a product manager of "Acme Project"
      And the glossary term "Backlog Item" exists
      When I update the glossary term "Backlog Item" with name "Work Item"
      Then the glossary term "Work Item" exists
      And the glossary term "Backlog Item" no longer exists

    Scenario: Update glossary term definition
      Given I am logged in as a product manager of "Acme Project"
      And the glossary term "Backlog Item" exists
      When I update the glossary term "Backlog Item" with definition "A prioritized unit of deliverable work"
      Then the glossary term "Backlog Item" has definition "A prioritized unit of deliverable work"

  Rule: Product managers can delete glossary terms

    Scenario: Delete a glossary term
      Given I am logged in as a product manager of "Acme Project"
      And the glossary term "Backlog Item" exists
      When I delete the glossary term "Backlog Item"
      Then the glossary term "Backlog Item" no longer exists

  Rule: Glossary terms can be linked to entities

    Scenario: Link a glossary term to an entity
      Given I am logged in as a product manager of "Acme Project"
      And the glossary term "Backlog Item" exists
      And the entity "BacklogItem" exists
      When I link the glossary term "Backlog Item" to entity "BacklogItem"
      Then the glossary term "Backlog Item" is linked to entity "BacklogItem"

    Scenario: Unlink a glossary term from an entity
      Given I am logged in as a product manager of "Acme Project"
      And the glossary term "Backlog Item" exists
      And the entity "BacklogItem" exists
      And the glossary term "Backlog Item" is linked to entity "BacklogItem"
      When I unlink the glossary term "Backlog Item" from entity "BacklogItem"
      Then the glossary term "Backlog Item" is not linked to entity "BacklogItem"

    Scenario: View entities linked to a glossary term
      Given I am logged in as a product manager of "Acme Project"
      And the glossary term "Backlog Item" exists
      And the entity "BacklogItem" exists
      And the entity "UserStory" exists
      And the glossary term "Backlog Item" is linked to entity "BacklogItem"
      And the glossary term "Backlog Item" is linked to entity "UserStory"
      When I view the entities linked to glossary term "Backlog Item"
      Then I see 2 linked entities

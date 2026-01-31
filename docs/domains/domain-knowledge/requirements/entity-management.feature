Feature: Entity Management
  As a product manager
  I want to manage entities within a subdomain
  So that I can model the business objects in my domain.

  Rule: Product managers can create entities

    Scenario: Create a new entity
      Given I am logged in as a product manager of "Acme Project"
      And the domain "Planning" exists in "Acme Project"
      And the subdomain "Backlog" exists in domain "Planning"
      When I create an entity with:
        | name        | BacklogItem                    |
        | description | A unit of work to be delivered |
        | subdomain   | Backlog                        |
      Then the entity "BacklogItem" exists in subdomain "Backlog"

    Scenario: Entity names must be globally unique
      Given I am logged in as a product manager of "Acme Project"
      And the entity "BacklogItem" exists
      When I create an entity with name "BacklogItem"
      Then I see the error "An entity with this name already exists"

  Rule: Product managers can view entities

    Scenario: View all entities in a subdomain
      Given I am logged in as a product manager of "Acme Project"
      And the domain "Planning" exists in "Acme Project"
      And the subdomain "Backlog" exists in domain "Planning"
      And the following entities exist in subdomain "Backlog":
        | name        |
        | BacklogItem |
        | Sprint      |
        | Release     |
      When I view the entities in subdomain "Backlog"
      Then I see 3 entities

    Scenario: View entity details
      Given I am logged in as a product manager of "Acme Project"
      And the entity "BacklogItem" exists with description "A unit of work to be delivered"
      When I view the entity "BacklogItem"
      Then I see the entity name "BacklogItem"
      And I see the entity description "A unit of work to be delivered"

  Rule: Product managers can update entities

    Scenario: Update entity name
      Given I am logged in as a product manager of "Acme Project"
      And the entity "BacklogItem" exists
      When I update the entity "BacklogItem" with name "WorkItem"
      Then the entity "WorkItem" exists
      And the entity "BacklogItem" no longer exists

    Scenario: Update entity description
      Given I am logged in as a product manager of "Acme Project"
      And the entity "BacklogItem" exists
      When I update the entity "BacklogItem" with description "A prioritized unit of work"
      Then the entity "BacklogItem" has description "A prioritized unit of work"

  Rule: Product managers can delete entities

    Scenario: Delete an entity
      Given I am logged in as a product manager of "Acme Project"
      And the entity "BacklogItem" exists
      When I delete the entity "BacklogItem"
      Then the entity "BacklogItem" no longer exists

  Rule: Product managers can manage entity attributes

    Scenario: Add an attribute to an entity
      Given I am logged in as a product manager of "Acme Project"
      And the entity "BacklogItem" exists
      When I add an attribute to "BacklogItem" with:
        | name     | title  |
        | type     | string |
        | required | yes    |
      Then the entity "BacklogItem" has attribute "title"

    Scenario: Remove an attribute from an entity
      Given I am logged in as a product manager of "Acme Project"
      And the entity "BacklogItem" exists
      And the entity "BacklogItem" has attribute "title"
      When I remove the attribute "title" from "BacklogItem"
      Then the entity "BacklogItem" does not have attribute "title"

  Rule: Product managers can manage entity functions

    Scenario: Add a function to an entity
      Given I am logged in as a product manager of "Acme Project"
      And the entity "BacklogItem" exists
      When I add a function to "BacklogItem" with:
        | name        | prioritize                          |
        | description | Sets the priority of the item       |
        | return_type | void                                |
      Then the entity "BacklogItem" has function "prioritize"

    Scenario: Remove a function from an entity
      Given I am logged in as a product manager of "Acme Project"
      And the entity "BacklogItem" exists
      And the entity "BacklogItem" has function "prioritize"
      When I remove the function "prioritize" from "BacklogItem"
      Then the entity "BacklogItem" does not have function "prioritize"

  Rule: Product managers can manage entity relationships

    Scenario: Add a relationship to an entity
      Given I am logged in as a product manager of "Acme Project"
      And the entity "BacklogItem" exists
      And the entity "Sprint" exists
      When I add a relationship to "BacklogItem" with:
        | name        | assigned to |
        | target      | Sprint      |
        | cardinality | N:1         |
      Then the entity "BacklogItem" has relationship "assigned to" to "Sprint"

    Scenario: Remove a relationship from an entity
      Given I am logged in as a product manager of "Acme Project"
      And the entity "BacklogItem" exists
      And the entity "BacklogItem" has relationship "assigned to" to "Sprint"
      When I remove the relationship "assigned to" from "BacklogItem"
      Then the entity "BacklogItem" does not have relationship "assigned to"

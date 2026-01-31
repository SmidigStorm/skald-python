Feature: Domain Management
  As a product manager
  I want to manage domains within my product
  So that I can organize requirements by business area.

  Rule: Product managers can create domains

    Scenario: Create a new domain
      Given I am logged in as a product manager of "Acme Project"
      When I create a domain with:
        | name        | User Access                    |
        | description | Authentication and permissions |
      Then the domain "User Access" exists in "Acme Project"

    Scenario: Domain names must be unique within a product
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      When I create a domain with name "User Access" in "Acme Project"
      Then I see the error "A domain with this name already exists"

  Rule: Product managers can view domains

    Scenario: View all domains in a product
      Given I am logged in as a product manager of "Acme Project"
      And the following domains exist in "Acme Project":
        | name           |
        | User Access    |
        | Planning       |
        | Domain Knowledge |
      When I view the domains in "Acme Project"
      Then I see 3 domains

    Scenario: View domain details
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project" with description "Authentication and permissions"
      When I view the domain "User Access"
      Then I see the domain name "User Access"
      And I see the domain description "Authentication and permissions"

  Rule: Product managers can update domains

    Scenario: Update domain name
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      When I update the domain "User Access" with name "User Management"
      Then the domain "User Management" exists in "Acme Project"
      And the domain "User Access" no longer exists in "Acme Project"

    Scenario: Update domain description
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      When I update the domain "User Access" with description "Users, roles, and permissions"
      Then the domain "User Access" has description "Users, roles, and permissions"

  Rule: Product managers can delete domains

    Scenario: Delete an empty domain
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      When I delete the domain "User Access"
      Then the domain "User Access" no longer exists in "Acme Project"

    Scenario: Deleting a domain cascades to subdomains
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      And the subdomain "Authentication" exists in domain "User Access"
      When I delete the domain "User Access"
      Then the domain "User Access" no longer exists in "Acme Project"
      And the subdomain "Authentication" no longer exists

Feature: SubDomain Management
  As a product manager
  I want to manage subdomains within a domain
  So that I can further organize requirements into logical groups.

  Rule: Product managers can create subdomains

    Scenario: Create a new subdomain
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      When I create a subdomain with:
        | name        | Authentication          |
        | description | Login and session management |
        | domain      | User Access             |
      Then the subdomain "Authentication" exists in domain "User Access"

    Scenario: SubDomain names must be unique within a domain
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      And the subdomain "Authentication" exists in domain "User Access"
      When I create a subdomain with name "Authentication" in domain "User Access"
      Then I see the error "A subdomain with this name already exists in this domain"

    Scenario: Same subdomain name can exist in different domains
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      And the domain "API" exists in "Acme Project"
      And the subdomain "Authentication" exists in domain "User Access"
      When I create a subdomain with name "Authentication" in domain "API"
      Then the subdomain "Authentication" exists in domain "API"

  Rule: Product managers can view subdomains

    Scenario: View all subdomains in a domain
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      And the following subdomains exist in domain "User Access":
        | name           |
        | Authentication |
        | Authorization  |
        | User Profile   |
      When I view the subdomains in domain "User Access"
      Then I see 3 subdomains

    Scenario: View subdomain details
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      And the subdomain "Authentication" exists in domain "User Access" with description "Login and session management"
      When I view the subdomain "Authentication"
      Then I see the subdomain name "Authentication"
      And I see the subdomain description "Login and session management"

  Rule: Product managers can update subdomains

    Scenario: Update subdomain name
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      And the subdomain "Authentication" exists in domain "User Access"
      When I update the subdomain "Authentication" with name "Login"
      Then the subdomain "Login" exists in domain "User Access"
      And the subdomain "Authentication" no longer exists in domain "User Access"

    Scenario: Update subdomain description
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      And the subdomain "Authentication" exists in domain "User Access"
      When I update the subdomain "Authentication" with description "User login and logout"
      Then the subdomain "Authentication" has description "User login and logout"

  Rule: Product managers can delete subdomains

    Scenario: Delete an empty subdomain
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      And the subdomain "Authentication" exists in domain "User Access"
      When I delete the subdomain "Authentication"
      Then the subdomain "Authentication" no longer exists in domain "User Access"

    Scenario: Deleting a subdomain cascades to capabilities
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      And the subdomain "Authentication" exists in domain "User Access"
      And the capability "Login" exists in subdomain "Authentication"
      When I delete the subdomain "Authentication"
      Then the subdomain "Authentication" no longer exists in domain "User Access"
      And the capability "Login" no longer exists

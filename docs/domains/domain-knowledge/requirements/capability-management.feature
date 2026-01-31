Feature: Capability Management
  As a product manager
  I want to manage capabilities within a subdomain
  So that I can define specific functional areas for requirements.

  Rule: Product managers can create capabilities

    Scenario: Create a new capability
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      And the subdomain "Authentication" exists in domain "User Access"
      When I create a capability with:
        | name        | Login                        |
        | description | User login functionality     |
        | subdomain   | Authentication               |
      Then the capability "Login" exists in subdomain "Authentication"

    Scenario: Capability names must be unique within a subdomain
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      And the subdomain "Authentication" exists in domain "User Access"
      And the capability "Login" exists in subdomain "Authentication"
      When I create a capability with name "Login" in subdomain "Authentication"
      Then I see the error "A capability with this name already exists in this subdomain"

    Scenario: Same capability name can exist in different subdomains
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      And the subdomain "Authentication" exists in domain "User Access"
      And the subdomain "Authorization" exists in domain "User Access"
      And the capability "Validation" exists in subdomain "Authentication"
      When I create a capability with name "Validation" in subdomain "Authorization"
      Then the capability "Validation" exists in subdomain "Authorization"

  Rule: Product managers can view capabilities

    Scenario: View all capabilities in a subdomain
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      And the subdomain "Authentication" exists in domain "User Access"
      And the following capabilities exist in subdomain "Authentication":
        | name              |
        | Login             |
        | Logout            |
        | Password Reset    |
      When I view the capabilities in subdomain "Authentication"
      Then I see 3 capabilities

    Scenario: View capability details
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      And the subdomain "Authentication" exists in domain "User Access"
      And the capability "Login" exists in subdomain "Authentication" with description "User login functionality"
      When I view the capability "Login"
      Then I see the capability name "Login"
      And I see the capability description "User login functionality"

  Rule: Product managers can update capabilities

    Scenario: Update capability name
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      And the subdomain "Authentication" exists in domain "User Access"
      And the capability "Login" exists in subdomain "Authentication"
      When I update the capability "Login" with name "User Login"
      Then the capability "User Login" exists in subdomain "Authentication"
      And the capability "Login" no longer exists in subdomain "Authentication"

    Scenario: Update capability description
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      And the subdomain "Authentication" exists in domain "User Access"
      And the capability "Login" exists in subdomain "Authentication"
      When I update the capability "Login" with description "Username and password login"
      Then the capability "Login" has description "Username and password login"

  Rule: Product managers can delete capabilities

    Scenario: Delete a capability
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      And the subdomain "Authentication" exists in domain "User Access"
      And the capability "Login" exists in subdomain "Authentication"
      When I delete the capability "Login"
      Then the capability "Login" no longer exists in subdomain "Authentication"

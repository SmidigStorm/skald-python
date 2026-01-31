Feature: Product Management
  As a system administrator
  I want to manage products
  So that I can set up tenant boundaries for teams.

  Rule: System administrators can create products

    Scenario: Create a new product
      Given I am logged in as a system administrator
      When I create a product with:
        | name        | Acme Project            |
        | description | Project management tool |
      Then the product "Acme Project" exists in the system

  Rule: Products can be deactivated but not deleted

    Scenario: Deactivate a product
      Given I am logged in as a system administrator
      And the product "Acme Project" exists
      When I deactivate the product "Acme Project"
      Then the product "Acme Project" is marked as inactive
      And users can no longer access the product "Acme Project"

    Scenario: Reactivate a product
      Given I am logged in as a system administrator
      And the product "Acme Project" is inactive
      When I reactivate the product "Acme Project"
      Then the product "Acme Project" is marked as active
      And users can access the product "Acme Project" again

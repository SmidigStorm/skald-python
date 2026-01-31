Feature: Role Assignment
  As an administrator
  I want to assign users to products with roles
  So that users can access the products they need.

  Rule: System administrators can assign users to any product

    Scenario: System administrator assigns a user to a product
      Given I am logged in as a system administrator
      And the user "jane_doe" exists
      And the product "Acme Project" exists
      When I assign "jane_doe" to "Acme Project" with role "Product Contributor"
      Then "jane_doe" has access to "Acme Project" as "Product Contributor"

  Rule: Product managers can assign users to their product

    Scenario: Product manager assigns a user to their product
      Given I am logged in as a product manager of "Acme Project"
      And the user "jane_doe" exists
      When I assign "jane_doe" to "Acme Project" with role "Product Viewer"
      Then "jane_doe" has access to "Acme Project" as "Product Viewer"

  Rule: Users can only have one role per product

    Scenario: Changing a user's role replaces the previous role
      Given I am logged in as a system administrator
      And "jane_doe" has access to "Acme Project" as "Product Viewer"
      When I assign "jane_doe" to "Acme Project" with role "Product Contributor"
      Then "jane_doe" has access to "Acme Project" as "Product Contributor"
      And "jane_doe" no longer has the role "Product Viewer" on "Acme Project"

  Rule: Users can be removed from a product

    Scenario: Remove a user from a product
      Given I am logged in as a system administrator
      And "jane_doe" has access to "Acme Project" as "Product Contributor"
      When I remove "jane_doe" from "Acme Project"
      Then "jane_doe" no longer has access to "Acme Project"

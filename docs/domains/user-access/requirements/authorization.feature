Feature: Authorization
  As a product member
  I want my access to be restricted based on my role
  So that the system enforces appropriate permissions.

  # OPEN QUESTIONS:
  # - What distinguishes Product Manager from Product Contributor?
  #   (Currently they seem to have the same permissions)

  Rule: System administrators have full access to everything

    Scenario: System administrator can manage users
      Given I am logged in as a system administrator
      Then I can create, edit, and delete users

    Scenario: System administrator can manage products
      Given I am logged in as a system administrator
      Then I can create, edit, and deactivate products

    Scenario: System administrator can access all products
      Given I am logged in as a system administrator
      And the product "Acme Project" exists
      Then I can access "Acme Project"

  Rule: Product managers and contributors can edit content within their product

    Scenario: Product manager can edit content
      Given I am logged in as a product manager of "Acme Project"
      Then I can create, edit, and delete content in "Acme Project"

    Scenario: Product contributor can edit content
      Given I am logged in as a product contributor of "Acme Project"
      Then I can create, edit, and delete content in "Acme Project"

  Rule: Product viewers have read-only access

    Scenario: Product viewer can view all content
      Given I am logged in as a product viewer of "Acme Project"
      Then I can view all content in "Acme Project"

    Scenario: Product viewer cannot edit content
      Given I am logged in as a product viewer of "Acme Project"
      When I try to create content in "Acme Project"
      Then I see an access denied error

  Rule: Users cannot access products they are not assigned to

    Scenario: User cannot access unassigned product
      Given I am logged in as "jane_doe"
      And I am not assigned to "Secret Project"
      When I try to access "Secret Project"
      Then I see an access denied error

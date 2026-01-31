Feature: User Management
  As a system administrator
  I want to manage users
  So that I can control who has access to the system.

  # OPEN QUESTIONS:
  # - What validation rules for username? (min/max length, allowed characters?)
  # - What validation rules for password? (min length, complexity?)
  # - Must email be unique?
  # - Must username be unique?

  Rule: System administrators can create users

    Scenario: Create a new user
      Given I am logged in as a system administrator
      When I create a user with:
        | username | jane_doe         |
        | email    | jane@example.com |
        | password | secret123        |
        | name     | Jane Doe         |
      Then the user "jane_doe" exists in the system

  Rule: System administrators can delete users

    Scenario: Delete a user
      Given I am logged in as a system administrator
      And the user "john_doe" exists
      When I delete the user "john_doe"
      Then the user "john_doe" no longer exists in the system

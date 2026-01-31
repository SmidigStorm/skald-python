Feature: Home Page
  As an authenticated user
  I want to see a home page after login
  So that I can navigate to my products.

  Rule: Home page shows user's assigned products

    Scenario: User sees their products on the home page
      Given I am logged in as "alice"
      And I am assigned to "Skald" as a product manager
      And I am assigned to "Acme App" as a product manager
      When I visit the home page
      Then I see a list of my products
      And I see "Skald" in the list
      And I see "Acme App" in the list

    Scenario: User with no products sees empty state
      Given I am logged in as "newuser"
      And I am not assigned to any products
      When I visit the home page
      Then I see a message "You are not assigned to any products"

  Rule: Users can navigate to their products

    Scenario: User clicks on a product to access it
      Given I am logged in as "alice"
      And I am assigned to "Skald" as a product manager
      When I visit the home page
      And I click on "Skald"
      Then I am redirected to the domain list for "Skald"

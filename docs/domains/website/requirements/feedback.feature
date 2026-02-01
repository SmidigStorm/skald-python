Feature: User Feedback and Notifications
  As a user
  I want clear feedback on my actions
  So that I know what happened and what to do next.

  Rule: Success messages appear as auto-dismissing toasts

    Scenario: Creating an item shows success toast
      Given I am logged in as a product manager of "Acme Project"
      When I create a domain with name "User Access"
      Then I see a success toast message "Domain created successfully"
      And the toast automatically disappears after a few seconds

    Scenario: Updating an item shows success toast
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      When I update the domain name to "User Management"
      Then I see a success toast message "Domain updated successfully"

    Scenario: Deleting an item shows success toast
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      When I delete the domain "User Access"
      Then I see a success toast message "Domain deleted successfully"

  Rule: Error messages appear as toasts for action failures

    Scenario: Server error shows error toast
      Given I am logged in as a product manager of "Acme Project"
      When I try to create a domain but the server returns an error
      Then I see an error toast message indicating the failure
      And the toast uses error styling

  Rule: Toasts appear in a consistent position

    Scenario: Toasts appear at the top of the screen
      Given I am logged in as a product manager of "Acme Project"
      When an action triggers a toast notification
      Then the toast appears at the top right of the screen
      And it does not obstruct the main content

    Scenario: Multiple toasts stack vertically
      Given I am logged in as a product manager of "Acme Project"
      When multiple actions trigger toast notifications
      Then the toasts stack vertically
      And each toast is visible

  Rule: Empty states provide guidance

    Scenario: Empty domain list shows helpful message
      Given I am logged in as a product manager of "Acme Project"
      And there are no domains in "Acme Project"
      When I view the domains page
      Then I see a message "No domains yet"
      And I see a call to action to create the first domain

    Scenario: Empty subdomain list shows helpful message
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      And there are no subdomains in "User Access"
      When I view the subdomains page for "User Access"
      Then I see a message "No subdomains yet"
      And I see a call to action to create the first subdomain

    Scenario: Empty capability list shows helpful message
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      And the subdomain "Authentication" exists in domain "User Access"
      And there are no capabilities in "Authentication"
      When I view the capabilities page for "Authentication"
      Then I see a message "No capabilities yet"
      And I see a call to action to create the first capability

  Rule: Loading states are indicated

    Scenario: Page shows loading indicator while fetching data
      Given I am logged in as a product manager of "Acme Project"
      When I navigate to a page that is loading data
      Then I see a loading indicator
      And the indicator disappears when data is loaded

  Rule: Confirmation dialogs prevent accidental destructive actions

    Scenario: Delete requires confirmation
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      When I click the delete button for "User Access"
      Then I am taken to a confirmation page
      And I must confirm to proceed with deletion

    Scenario: Canceling delete returns to previous page
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      When I click the delete button for "User Access"
      And I click cancel on the confirmation page
      Then I am returned to the domains list
      And the domain "User Access" still exists

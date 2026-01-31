Feature: User Login and Logout
  As a user
  I want to log in and out of the system
  So that I can access protected content and secure my session.

  Rule: Users can log in with valid credentials

    Scenario: Successful login
      Given the user "john_doe" exists with password "secret123"
      When the user visits the login page
      And the user logs in with username "john_doe" and password "secret123"
      Then the user is redirected to the home page

  Rule: Invalid credentials are rejected with a generic error

    Scenario: Login fails with wrong password
      Given the user "john_doe" exists with password "secret123"
      When the user visits the login page
      And the user logs in with username "john_doe" and password "wrongpassword"
      Then the user sees the error "Login failed"
      And the user remains on the login page

    Scenario: Login fails with unknown username
      Given no user exists with username "unknown_user"
      When the user visits the login page
      And the user logs in with username "unknown_user" and password "anypassword"
      Then the user sees the error "Login failed"
      And the user remains on the login page

  Rule: Unauthenticated users are redirected to login

    Scenario: Accessing protected page redirects to login
      Given I am not logged in
      When I try to access the home page
      Then I am redirected to the login page

  Rule: Users can log out and their session is terminated

    Scenario: Successful logout
      Given I am logged in as "john_doe"
      When I click the logout button
      Then I am redirected to the login page
      And my session is terminated

    Scenario: After logout, protected pages require login
      Given I am logged in as "john_doe"
      When I click the logout button
      And I try to access the home page
      Then I am redirected to the login page

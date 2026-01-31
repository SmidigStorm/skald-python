Feature: User Login
  As an unauthenticated user
  I want to log in with my username and password
  So that I can access the system.

  Rule: Users can log in with valid credentials

    Scenario: Successful login
      Given the user "john_doe" exists with password "secret123"
      When the user logs in with username "john_doe" and password "secret123"
      Then the user is redirected to the dashboard

  Rule: Invalid credentials are rejected with a generic error

    Scenario: Login fails with wrong password
      Given the user "john_doe" exists with password "secret123"
      When the user logs in with username "john_doe" and password "wrongpassword"
      Then the user sees the error "Login failed"
      And the user remains on the login page

    Scenario: Login fails with unknown username
      Given no user exists with username "unknown_user"
      When the user logs in with username "unknown_user" and password "anypassword"
      Then the user sees the error "Login failed"
      And the user remains on the login page

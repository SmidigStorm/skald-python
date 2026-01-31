Feature: Health Check
  As a developer
  I want to verify the application is running
  So that I can confirm the test setup works

  Scenario: Application responds to health check
    Given the application is running
    When I request the admin login page
    Then I receive a successful response

Feature: Navigation and Layout
  As a user
  I want clear navigation throughout the application
  So that I can easily find and access different areas.

  Rule: The layout has a sidebar and main content area

    Scenario: Logged in user sees sidebar navigation
      Given I am logged in as a product manager
      When I view any page in the application
      Then I see a sidebar on the left side
      And I see the main content area on the right

    Scenario: Sidebar shows main navigation items
      Given I am logged in as a product manager
      When I view any page in the application
      Then the sidebar shows navigation links
      And the current section is highlighted in the sidebar

  Rule: Breadcrumbs are always visible

    Scenario: Breadcrumbs show navigation path on home page
      Given I am logged in as a product manager
      When I visit the home page
      Then I see breadcrumbs showing "Home"

    Scenario: Breadcrumbs show full path on nested pages
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      And the subdomain "Authentication" exists in domain "User Access"
      When I view the capabilities in subdomain "Authentication"
      Then I see breadcrumbs showing "Home > Acme Project > User Access > Authentication > Capabilities"
      And each breadcrumb segment is a clickable link except the current page

    Scenario: Clicking a breadcrumb navigates to that level
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      And the subdomain "Authentication" exists in domain "User Access"
      When I view the capabilities in subdomain "Authentication"
      And I click the "User Access" breadcrumb
      Then I am taken to the subdomains page for "User Access"

  Rule: The sidebar shows product context

    Scenario: Sidebar shows current product name
      Given I am logged in as a product manager of "Acme Project"
      When I view the domains for "Acme Project"
      Then the sidebar shows "Acme Project" as the current product

    Scenario: User can switch products from sidebar
      Given I am logged in as a product manager of "Acme Project"
      And I am also a product manager of "Beta Product"
      When I click on the product switcher in the sidebar
      Then I see a list of my products
      And I can select "Beta Product" to switch to it

  Rule: Navigation items indicate the current location

    Scenario: Current page is highlighted in sidebar
      Given I am logged in as a product manager of "Acme Project"
      When I view the domains for "Acme Project"
      Then the "Domains" link in the sidebar is highlighted
      And other navigation links are not highlighted

  Rule: The header shows user information

    Scenario: User sees their name in the header
      Given I am logged in as "alice"
      When I view any page in the application
      Then I see my username "alice" in the header area

    Scenario: User can access logout from header
      Given I am logged in as "alice"
      When I view any page in the application
      Then I see a logout option in the header area

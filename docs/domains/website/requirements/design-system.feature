Feature: Design System
  As a user
  I want a consistent visual design across the application
  So that the interface is intuitive and pleasant to use.

  Rule: The application uses DaisyUI components with Tailwind CSS

    Scenario: Pages use DaisyUI component styling
      Given I am logged in as a product manager
      When I view any page in the application
      Then I see styled components using DaisyUI classes
      And the styling is consistent across all pages

  Rule: Theme follows system preference

    Scenario: Light theme is applied when system prefers light
      Given my system is set to light mode
      When I visit the application
      Then the application displays in light theme

    Scenario: Dark theme is applied when system prefers dark
      Given my system is set to dark mode
      When I visit the application
      Then the application displays in dark theme

  Rule: Users can manually override the theme

    Scenario: User switches to dark theme
      Given I am logged in as a product manager
      And the application is displaying in light theme
      When I select "Dark" from the theme switcher
      Then the application displays in dark theme
      And my theme preference is saved

    Scenario: User switches to light theme
      Given I am logged in as a product manager
      And the application is displaying in dark theme
      When I select "Light" from the theme switcher
      Then the application displays in light theme
      And my theme preference is saved

    Scenario: Manual theme preference persists across sessions
      Given I am logged in as a product manager
      And I have previously selected dark theme
      When I log out and log back in
      Then the application displays in dark theme

  Rule: Cards are the primary content container

    Scenario: Content is displayed in cards
      Given I am logged in as a product manager
      When I view a list of domains
      Then each domain is displayed in a card
      And the card shows the domain name and description

    Scenario: Cards have consistent styling
      Given I am logged in as a product manager
      When I view any list page
      Then cards have a white background in light theme
      And cards have subtle shadow and rounded corners

  Rule: Typography follows a consistent hierarchy

    Scenario: Page titles use heading styles
      Given I am logged in as a product manager
      When I view the domains page
      Then the page title "Domains" is displayed as a large heading
      And section headings are visually distinct from body text

  Rule: Buttons have clear visual hierarchy

    Scenario: Primary actions use primary button style
      Given I am logged in as a product manager
      When I view a page with a primary action
      Then the primary action button is visually prominent
      And it uses the primary color

    Scenario: Destructive actions use danger button style
      Given I am logged in as a product manager
      When I view a delete confirmation page
      Then the delete button is styled as a danger button
      And it is visually distinct from cancel

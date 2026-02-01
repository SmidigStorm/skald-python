Feature: Form Styling and Validation
  As a user
  I want clear and consistent forms
  So that I can easily enter data and understand any errors.

  Rule: Form inputs use DaisyUI styling

    Scenario: Text inputs have consistent styling
      Given I am logged in as a product manager
      When I view a form with text inputs
      Then text inputs have borders and proper padding
      And inputs have labels above them
      And placeholder text is visible when the field is empty

    Scenario: Textareas have consistent styling
      Given I am logged in as a product manager
      When I view a form with a description field
      Then the textarea has the same styling as text inputs
      And it is tall enough for multi-line content

    Scenario: Select dropdowns have consistent styling
      Given I am logged in as a product manager
      When I view a form with a dropdown
      Then the dropdown matches the input styling
      And it shows a clear indicator that it is selectable

  Rule: Form validation happens on submit

    Scenario: Valid form submits successfully
      Given I am logged in as a product manager of "Acme Project"
      When I create a domain with name "User Access" and description "User management"
      Then the domain is created
      And I see a success message

    Scenario: Invalid form shows errors on submit
      Given I am logged in as a product manager of "Acme Project"
      When I try to create a domain with an empty name
      And I click the submit button
      Then the form is not submitted
      And I see an error message for the name field

  Rule: Validation errors appear inline under fields

    Scenario: Required field error appears under the field
      Given I am logged in as a product manager of "Acme Project"
      When I submit a domain form with an empty name field
      Then I see the error "This field is required" under the name field
      And the name field is highlighted as invalid

    Scenario: Multiple field errors are shown together
      Given I am logged in as a product manager of "Acme Project"
      When I submit a form with multiple invalid fields
      Then I see error messages under each invalid field
      And all invalid fields are highlighted

    Scenario: Errors clear when form is corrected and resubmitted
      Given I am logged in as a product manager of "Acme Project"
      And I submitted a form with an invalid name field
      When I correct the name field
      And I submit the form again
      Then the error message disappears
      And the form is submitted successfully

  Rule: Buttons have clear labels and positioning

    Scenario: Submit button is clearly labeled
      Given I am logged in as a product manager
      When I view a create form
      Then I see a submit button with a clear action label like "Create" or "Save"

    Scenario: Cancel option is available on forms
      Given I am logged in as a product manager of "Acme Project"
      When I view the create domain form
      Then I see a cancel link or button
      And clicking cancel returns me to the previous page without saving

    Scenario: Delete forms show clear warning
      Given I am logged in as a product manager of "Acme Project"
      And the domain "User Access" exists in "Acme Project"
      When I click delete on the domain "User Access"
      Then I see a confirmation page
      And the delete button is styled as a danger button
      And there is a cancel option to go back

  Rule: Forms are accessible

    Scenario: Labels are associated with inputs
      Given I am logged in as a product manager
      When I view a form
      Then each input has a label
      And clicking the label focuses the corresponding input

    Scenario: Required fields are indicated
      Given I am logged in as a product manager
      When I view a form with required fields
      Then required fields are marked with an indicator

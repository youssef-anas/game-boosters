$(document).ready(function () {
  $toggleMenu = $('.main-nav .toggle-menu');
  $links = $('.main-nav .links');
  $toggleMenu.click(function () {
    $links.toggleClass('shown')
  })

  // Function to enable/disable the submit button for a specific form
  function toggleSubmitButton(form, disable) {
    let submitButton = form.find('button[type="submit"]');
    let submitInput = form.find('input[type="submit"]');

    submitButton.prop('disabled', disable);
    submitInput.prop('disabled', disable);
  }

  // Disable submit buttons initially for all forms
  $('form').each(function() {
    toggleSubmitButton($(this), true);
  });

  // Add event listener to form fields
  $('form').on('input change', function () {
    // Enable submit button for the changed form
    toggleSubmitButton($(this), false);
  });

  // Add event listener to submit buttons
  $('form').on('submit', function () {
    var form = $(this);
    // Disable submit button after form submission
    setTimeout(function() {
      toggleSubmitButton(form, true);
    }, 0); // Use setTimeout to ensure the button is disabled after form submission
  });


});
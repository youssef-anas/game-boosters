// Make Nav Fixed

// JavaScript to add fixed class to navigation on scroll
window.addEventListener('scroll', function() {
  let nav = document.getElementById('nav');
  let scrollPosition = window.scrollY;

  if (scrollPosition > 100) { 
    nav.classList.add('fixed');
  } else {
    nav.classList.remove('fixed');
  }
});

$(document).ready(function () {
  $toggleMenu = $('.main-nav .toggle-menu');
  $nav = $('.nav#nav');
  $links = $('.main-nav .links');

  $toggleMenu.click(function () {
    $links.toggleClass('shown')
    $nav.toggleClass('shown')
  })

  $closeIcon = $('.links .close-icon')
  $closeIcon.click(function () {
    $links.removeClass('shown')
    $nav.removeClass('shown')
  })

  // Function to enable/disable the submit button for a specific form
  function toggleSubmitButton(form, disable) {
    let submitButton = form.find('button[type="submit"]');
    let submitInput = form.find('input[type="submit"]');

    submitButton.prop('disabled', disable);
    submitInput.prop('disabled', disable);
  }

  // Function to check if the form is empty
  function isFormEmpty(form) {
    let isEmpty = true;
    form.find('input[type="text"], input[type="password"], input[type="email"], textarea').each(function() {
      if ($(this).val().trim() !== '') {
        isEmpty = false;
        return false; // Exit the loop if a non-empty field is found
      }
    });
    form.find('input[type="radio"], input[type="checkbox"]').each(function() {
      if ($(this).is(':checked')) {
        isEmpty = false;
        return false; // Exit the loop if a checked radio button or checkbox is found
      }
    });
    form.find('select').each(function() {
      if ($(this).val() !== '') {
        isEmpty = false;
        return false; // Exit the loop if a select element has a value selected
      }
    });
    return isEmpty;
  }

  // Disable submit buttons initially for all forms
  $('form:not(.no-disabled-form)').each(function() {
    toggleSubmitButton($(this), true);
  });

  // Add event listener to form fields
  $('form:not(.no-disabled-form)').on('input change keyup', function () {
    // Enable submit button if the form is not empty
    toggleSubmitButton($(this), isFormEmpty($(this)));
  });

  // Add event listener to submit buttons
  $('form:not(.no-disabled-form)').on('submit', function () {
    var form = $(this);
    // Disable submit button after form submission
    setTimeout(function() {
      toggleSubmitButton(form, true);
    }, 0); // Use setTimeout to ensure the button is disabled after form submission
  });

});
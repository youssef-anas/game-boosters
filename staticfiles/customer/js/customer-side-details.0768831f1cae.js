$(document).ready(function() {
  function toggleEdit() {
    $('#gameNameText').toggleClass('d-none');
    $('#gameNameInput').toggleClass('d-none');

    $('#serverText').toggleClass('d-none');
    $('#serverSelect').toggleClass('d-none');

    $('#usernameText').toggleClass('d-none');
    $('#usernameInput').toggleClass('d-none');

    $('#passwordText').toggleClass('d-none');
    $('#passwordInput').toggleClass('d-none');

    $('#updateDetailsBtn').toggleClass('d-none');
    $('#saveDetailsBtn').toggleClass('d-none');
  }

  // Validation Before Submit
  // Validate gameName
  $('#gameNameInput').on('input', function(){
    let value = $(this).val().trim();

    value = value.replace(/\s/g, '');

    if(value.length > 300) {
      value = value.substring(0, 300);
    }

    $(this).val(value);
  })

  // Validate username
  $('#usernameInput').on('input', function(){
    let value = $(this).val().trim();

    value = value.replace(/\s/g, '');

    if(value.length > 300) {
      value = value.substring(0, 300);
    }

    $(this).val(value);
  })

  function saveChanges(event) {
    event.preventDefault(); // Prevent default form submission
    
    let formData = {
      'order_id': $('#order_id').val(),
      'customer_gamename': $('#gameNameInput').val(),
      'customer_password': $('#passwordInput').val(),
      'customer_server': $('#serverSelect select').val(),
      'customer_username': $('#usernameInput').val(),
      'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
    };
  
    $.ajax({
      type: 'POST',
      url: '/customer/set_customer_data/',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val() // Include CSRF token in headers
      },
      data: formData,
      success: function(response) {
        if (response.success) {
          $('#error-success').text(response.message);
          $('#gameNameText').text(response.updated_data.customer_gamename);
          $('#serverText').text(response.updated_data.customer_server);
          $('#usernameText').text(response.updated_data.customer_username);
          $('#passwordText').text(response.updated_data.customer_password);
          $('#data-incorrect').text('').remove();
          scrollToBottom();
        } else {
          $('#error-success').text(response.message);
        }
      },
      error: function(xhr, status, error) {
        $('#error-success').text('Error: ' + xhr.status + ' - ' + xhr.statusText);
      }
    });
  
    // Switch back to view mode (assuming this function exists and toggles the view mode)
    toggleEdit();
  }
  

  $('#updateDetailsBtn').click(toggleEdit);
  $('#saveDetailsBtn').click(saveChanges);
});

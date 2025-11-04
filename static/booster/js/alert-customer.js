const alertForms = document.querySelectorAll('.alert-customer-form');

if (alertForms && alertForms.length) {
  alertForms.forEach((formEl) => {
    formEl.addEventListener('submit', function (event) {
      event.preventDefault();

      const form = this;
      const formData = new FormData(form);
      const requestData = new URLSearchParams();

      for (const [key, value] of formData.entries()) {
        requestData.append(key, value);
      }

      fetch(form.action, {
        method: form.method,
        body: requestData,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.text();
      })
      .then(data => {
        console.log('Success:', data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
    });
  });
}

// $('.drop-order-form').on("submit", function (event) {
//   // Prevent the default form submission behavior
//   event.preventDefault();
//   // Submit the form via AJAX
//   let form = $(this);
//   let id = form.data("id")
//   $.ajax({
//     type: form.attr('method'),
//     url: form.attr('action'),
//     data: form.serialize(),
//     success: function (data) {
//       $(`.order-${id}`).remove()
//     },
//     error: function (xhr, status, error) {
//       // Handle error response here
//       console.error(xhr.responseText);
//       // alert('Error sending alert to customer!');
//     }
//   });
// });
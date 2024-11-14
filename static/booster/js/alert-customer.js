document.querySelector('.alert-customer-form').addEventListener('submit', function (event) {
  // Prevent the default form submission behavior
  event.preventDefault();

  let form = this;
  let formData = new FormData(form);
  let requestData = new URLSearchParams();

  for (let [key, value] of formData.entries()) {
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
    return response.text(); // or response.json() if you expect JSON
  })
  .then(data => {
    // Handle success response here
    // alert('Alert sent to customer successfully!');
    console.log('Success:', data);
  })
  .catch(error => {
    // Handle error response here
    console.error('Error:', error);
    // alert('Error sending alert to customer!');
  });
});

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
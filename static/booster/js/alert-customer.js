$('.alert-customer-form').on("submit", function (event) {
  // Prevent the default form submission behavior
  event.preventDefault();
  // Submit the form via AJAX
  let form = $(this);
  
  $.ajax({
    type: form.attr('method'),
    url: form.attr('action'),
    data: form.serialize(),
    success: function (data) {
      // Handle success response here
      // alert('Alert sent to customer successfully!');
    },
    error: function (xhr, status, error) {
      // Handle error response here
      console.error(xhr.responseText);
      // alert('Error sending alert to customer!');
    }
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
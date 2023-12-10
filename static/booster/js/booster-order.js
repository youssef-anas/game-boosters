$('document').ready(function() {
  let ordersDivs = $('.order');
  let ordersRadio = $('input[name="radio-order"]')

  // Intial 
  let intialOrderId = $('input[name="radio-order"]:checked').data('order');
  console.log('intialOrderId: ', intialOrderId)
  ordersDivs.each(function() {
    let currentOrderId = $(this).data('order');
    console.log('currentOrderId: ', currentOrderId)
    if (currentOrderId == intialOrderId) {
      $(this).show();
    } else {
      $(this).hide();
    }
  })

  ordersRadio.each(function() {
    let orderId = $(this).data('order');
    $(this).on('change', function() {
      ordersDivs.each(function() {
        let currentOrderId = $(this).data('order');
        if (currentOrderId == orderId) {
          $(this).show();
        } else {
          $(this).hide();
        }
      })
    })
  })

})
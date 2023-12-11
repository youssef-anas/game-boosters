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


  var rankSelect = $('#reached_rank');
  var divisionSelect = $('#reached_division');
  var marksSelect = $('#reached_marks');
  
  var originalDivisionOptions = divisionSelect.html();
  var originalMarksOptions = marksSelect.html();

  function updateOptions() {
    var selectedRank = rankSelect.find(':selected');
    console.log('select Rank', selectedRank)
    var markNumber = selectedRank.data('mark');

    divisionSelect.html(originalDivisionOptions);
    marksSelect.html(originalMarksOptions);

    if (selectedRank.text().toLowerCase() === "master") {
      divisionSelect.find('option').hide();
      marksSelect.find('option').hide();
    } else {
      marksSelect.find('option').each(function () {
        if ($(this).val() > markNumber) {
          $(this).hide();
        } else {
          $(this).show();
        }
      });
    }
  }

  updateOptions();

  rankSelect.change(updateOptions);

  $('#finish_image').on('change', function () {
    previewImage(this);
  });

  function previewImage(input) {
    var preview = $('#image-preview')[0];
    var file = input.files[0];

    if (file) {
      var reader = new FileReader();

      reader.onload = function (e) {
          $(preview).attr('src', e.target.result);
          $(preview).css('display', 'block');
      };

      reader.readAsDataURL(file);
    } else {
        $(preview).css('display', 'none');
    }
  }

  const dropContainer = document.getElementById("dropcontainer")
  const fileInput = document.getElementById("finish_image")

  dropContainer.addEventListener("dragover", (e) => {
    e.preventDefault()
  }, false)

  dropContainer.addEventListener("dragenter", () => {
    dropContainer.classList.add("drag-active")
  })

  dropContainer.addEventListener("dragleave", () => {
    dropContainer.classList.remove("drag-active")
  })

  dropContainer.addEventListener("drop", (e) => {
    e.preventDefault()
    dropContainer.classList.remove("drag-active")
    fileInput.files = e.dataTransfer.files
    previewImage(fileInput);
  })

})
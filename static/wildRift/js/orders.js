$(document).ready(function () {
  const divisionBoostOrderRadio = $('#division-boost-order')[0];
  const placementBoostOrderRadio = $('#placements-boost-order')[0];

  const divisionBoostOrderDiv = $('.division-boost-order')[0];
  const placementBoostOrderDiv = $('.placements-boost-order')[0];

  if (divisionBoostOrderRadio.checked) {
    divisionBoostOrderDiv.classList.remove('d-none');
    placementBoostOrderDiv.classList.add('d-none');
  } else {
    divisionBoostOrderDiv.classList.add('d-none');
    placementBoostOrderDiv.classList.remove('d-none');
  }

  $(divisionBoostOrderRadio).on('change', function () {
    if (divisionBoostOrderRadio.checked) {
      divisionBoostOrderDiv.classList.remove('d-none');
      placementBoostOrderDiv.classList.add('d-none');
    } else {
      divisionBoostOrderDiv.classList.add('d-none');
    }
  })

  $(placementBoostOrderRadio).on('change', function () {
    if (placementBoostOrderRadio.checked) {
      divisionBoostOrderDiv.classList.add('d-none');
      placementBoostOrderDiv.classList.remove('d-none');
    } else {
      placementBoostOrderDiv.classList.add('d-none');
    }
  })

  $('.division-price').each(function (index, paragraph) {
    let divisionPrice = parseFloat($(paragraph).data('price'));
    let divisionPercent;

    function updatePrice(i) {
      divisionPercent = $(paragraph).data(`percent${i}`);
      let divisionRealPrice = divisionPrice * (divisionPercent / 100);
      $(paragraph).text(`${divisionRealPrice.toFixed(2)}$`);

      // Schedule the next update after 1000 milliseconds
      if (i < 4) {
        setTimeout(function () {
          updatePrice(i + 1);
        }, 60000);
      }
    }

    // Start the update sequence
    updatePrice(1);
  });
  
  $('.placement-price').each(function (index, paragraph) {
    let divisionPrice = parseFloat($(paragraph).data('price'));
    let divisionPercent;

    function updatePrice(i) {
      divisionPercent = $(paragraph).data(`percent${i}`);
      let divisionRealPrice = divisionPrice * (divisionPercent / 100);
      $(paragraph).text(`${divisionRealPrice.toFixed(2)}$`);

      // Schedule the next update after 1000 milliseconds
      if (i < 4) {
        setTimeout(function () {
          updatePrice(i + 1);
        }, 60000);
      }
    }

    // Start the update sequence
    updatePrice(1);
  });
})
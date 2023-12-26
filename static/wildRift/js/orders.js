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
})
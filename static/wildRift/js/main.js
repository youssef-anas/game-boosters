document.addEventListener("DOMContentLoaded", function () {
  const divisionBoostRadio = document.getElementById('division-boost');
  const placementsBoostRadio = document.getElementById('placements-boost');

  const divisionBoostDiv = document.querySelectorAll('.division-boost');
  const placementsBoostDiv = document.querySelectorAll('.placements-boost');

  // Initial setup
  if (divisionBoostRadio.checked) {
    divisionBoostDiv.forEach(div => div.classList.remove('d-none'));
    placementsBoostDiv.forEach(div => div.classList.add('d-none'));
  } else {
    divisionBoostDiv.forEach(div => div.classList.add('d-none'));
    placementsBoostDiv.forEach(div => div.classList.remove('d-none'));
  }

  // Event listener for division-boost radio button
  divisionBoostRadio.addEventListener('change', function () {
    if (divisionBoostRadio.checked) {
      divisionBoostDiv.forEach(div => div.classList.remove('d-none'));
      placementsBoostDiv.forEach(div => div.classList.add('d-none'));
    } else {
      divisionBoostDiv.forEach(div => div.classList.add('d-none'));
    }
  });

  // Event listener for placements-boost radio button
  placementsBoostRadio.addEventListener('change', function () {
    if (placementsBoostRadio.checked) {
      divisionBoostDiv.forEach(div => div.classList.add('d-none'));
      placementsBoostDiv.forEach(div => div.classList.remove('d-none'));
    } else {
      placementsBoostDiv.forEach(div => div.classList.add('d-none'));
    }
  });
});
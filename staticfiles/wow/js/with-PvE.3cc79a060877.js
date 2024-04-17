document.addEventListener("DOMContentLoaded", function () {
  const arena2vs2Radio = document.getElementById('arena-2vs2');
  const arena3vs3Radio = document.getElementById('arena-3vs3');
  const PvEBoostingRadio = document.getElementById('PvE-boosting');

  const arena2vs2Div = document.querySelectorAll('.arena-2vs2');
  const arena3vs3Div = document.querySelectorAll('.arena-3vs3');
  const PvEBoostingDiv = document.querySelectorAll('.PvE-boosting');

  // Initial setup
  if (arena3vs3Radio.checked) {
    arena2vs2Div.forEach(div => div.classList.remove('d-none'));
    arena3vs3Div.forEach(div => div.classList.add('d-none'));

    PvEBoostingDiv.forEach(div => div.classList.add('d-none'));
  } else if (arena2vs2Radio.checked) {
    arena2vs2Div.forEach(div => div.classList.add('d-none'));
    PvEBoostingDiv.forEach(div => div.classList.add('d-none'));
    arena3vs3Div.forEach(div => div.classList.remove('d-none'));
  } else {
    PvEBoostingDiv.forEach(div => div.classList.remove('d-none'));
    arena2vs2Div.forEach(div => div.classList.add('d-none'));
    arena3vs3Div.forEach(div => div.classList.add('d-none'));
  }

  // Event listener for division-boost radio button
  arena3vs3Radio.addEventListener('change', function () {
    if (arena3vs3Radio.checked) {
      arena2vs2Div.forEach(div => div.classList.remove('d-none'));
      PvEBoostingDiv.forEach(div => div.classList.add('d-none'));
      arena3vs3Div.forEach(div => div.classList.add('d-none'));
    } else {
      arena2vs2Div.forEach(div => div.classList.add('d-none'));
    }
  });

  // Event listener for placements-boost radio button
  arena2vs2Radio.addEventListener('change', function () {
    if (arena2vs2Radio.checked) {
      arena2vs2Div.forEach(div => div.classList.add('d-none'));
      PvEBoostingDiv.forEach(div => div.classList.add('d-none'));
      arena3vs3Div.forEach(div => div.classList.remove('d-none'));
    } else {
      arena3vs3Div.forEach(div => div.classList.add('d-none'));
    }
  });

  // Event listener for arena-boost radio button
  PvEBoostingRadio.addEventListener('change', function () {
    if (PvEBoostingRadio.checked) {
      arena2vs2Div.forEach(div => div.classList.add('d-none'));
      arena3vs3Div.forEach(div => div.classList.add('d-none'));
      PvEBoostingDiv.forEach(div => div.classList.remove('d-none'));
    } else {
      PvEBoostingDiv.forEach(div => div.classList.add('d-none'));
    }
  });
});
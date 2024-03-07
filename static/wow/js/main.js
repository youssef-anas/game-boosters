document.addEventListener("DOMContentLoaded", function () {
  const arena2vs2Radio = document.getElementById('arena-2vs2');
  const arena3vs3Radio = document.getElementById('arena-3vs3');

  const arena2vs2Div = document.querySelectorAll('.arena-2vs2');
  const arena3vs3Div = document.querySelectorAll('.arena-3vs3');

  // Initial setup
  if (arena2vs2Radio.checked) {
    arena2vs2Div.forEach(div => div.classList.remove('d-none'));
    arena3vs3Div.forEach(div => div.classList.add('d-none'));
    get2vs2ArenaPrice()

  } else {
    arena2vs2Div.forEach(div => div.classList.add('d-none'));
    arena3vs3Div.forEach(div => div.classList.remove('d-none'));
    get3vs3ArenaPrice()

  }

  // Event listener for division-boost radio button
  arena2vs2Radio.addEventListener('change', function () {
    if (arena2vs2Radio.checked) {
      arena2vs2Div.forEach(div => div.classList.remove('d-none'));
      arena3vs3Div.forEach(div => div.classList.add('d-none'));
      get2vs2ArenaPrice()

    } else {
      arena2vs2Div.forEach(div => div.classList.add('d-none'));
      get3vs3ArenaPrice();
      
    }
  });

  // Event listener for placements-boost radio button
  arena3vs3Radio.addEventListener('change', function () {
    if (arena3vs3Radio.checked) {
      arena2vs2Div.forEach(div => div.classList.add('d-none'));
      arena3vs3Div.forEach(div => div.classList.remove('d-none'));
      get3vs3ArenaPrice();

    } else {
      arena3vs3Div.forEach(div => div.classList.add('d-none'));
      get2vs2ArenaPrice()
    }
  });

});
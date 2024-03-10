document.addEventListener("DOMContentLoaded", function () {
  const arena2vs2Radio = document.getElementById('arena-2vs2');
  const arena3vs3Radio = document.getElementById('arena-3vs3');

  const arena2vs2Div = document.querySelectorAll('.arena-2vs2');
  const arena3vs3Div = document.querySelectorAll('.arena-3vs3');

  function arena2vs2Action() {
    arena2vs2Div.forEach(div => div.classList.remove('d-none'));
    arena3vs3Div.forEach(div => div.classList.add('d-none'));
    $('#arena-form').data('type', 'arena2vs2');
    get2vs2ArenaPrice()
  }

  function arena3vs3Action() {
    arena2vs2Div.forEach(div => div.classList.add('d-none'));
    arena3vs3Div.forEach(div => div.classList.remove('d-none'));
    $('#arena-form').data('type', 'arena3vs3');
    get3vs3ArenaPrice();
  }

  // Initial setup
  if (arena2vs2Radio.checked) {
    arena2vs2Action()
  } else {
    arena3vs3Action()
  }

  // Extend 
  extend_order && (valuesToSetExtra[0] ? arena2vs2Action() : arena3vs3Action())

  // Event listener for division-boost radio button
  arena2vs2Radio.addEventListener('change', function () {
    if (arena2vs2Radio.checked) {
      arena2vs2Action()
    } else {
      arena3vs3Action()
    }
  });

  // Event listener for placements-boost radio button
  arena3vs3Radio.addEventListener('change', function () {
    if (arena3vs3Radio.checked) {
      arena3vs3Action()
    } else {
      arena3vs3Action()
    }
  });

});
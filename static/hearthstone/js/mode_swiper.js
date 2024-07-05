document.addEventListener("DOMContentLoaded", function () {
    const divisionBoostRadio = document.getElementById('division-boost');
    const battlegroundsRadio = document.getElementById('battlegrounds-boost');
  
    const divisionBoostDiv = document.querySelectorAll('.division-boost');
    const battlegroundsDiv = document.querySelectorAll('.battlegrounds-boost');

    // const divisionForm = document.getElementById('division-boost-form');
    // const battlegroundsForm = document.getElementById('battlegrounds-boost-form');
  
    function divisionBoostAction() {
        divisionBoostDiv.forEach(div => div.classList.remove('d-none'));
        battlegroundsDiv.forEach(div => div.classList.add('d-none'));
    }
  
    function battlegroundsAction() {
        divisionBoostDiv.forEach(div => div.classList.add('d-none'));
        battlegroundsDiv.forEach(div => div.classList.remove('d-none'));
        $('.desired').removeClass().addClass(`desired gold`);
        $('.current').removeClass().addClass(`current gold`);
    }
  
    // Initial setup
    if (divisionBoostRadio.checked) {
      divisionBoostAction()
    } else {
      battlegroundsAction()
    }
  
    // Extend 
    extend_order && (valuesToSetExtra[0] ? divisionBoostAction() : battlegroundsAction())
  
    // Event listener for division-boost radio button
    divisionBoostRadio.addEventListener('change', function () {
      if (divisionBoostRadio.checked) {
        divisionBoostAction()
      } else {
        battlegroundsAction()
      }
    });
  
    // Event listener for battlegrounds-boost radio button
    battlegroundsRadio.addEventListener('change', function () {
      if (battlegroundsRadio.checked) {
        battlegroundsAction()
      } else {
        divisionBoostAction()
      }
    });

    if (extend_order){

      if(valuesAsList.at(-1) === '1'){
        divisionBoostAction()
        console.log('extend_order for division')
        //   battlegroundsDiv.forEach(function(element) {
        //     element.remove();
        // });
      }
      else if(valuesAsList.at(-1) === '2'){
        battlegroundsAction()
        console.log('extend_order for battlegrounds')
      //   divisionBoostDiv.forEach(function(element) {
      //     element.remove();
      // });
      }
      $('#mode_swiper').remove();
    }
  });
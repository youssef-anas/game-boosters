document.addEventListener("DOMContentLoaded", function() {
  const radioButtonsCurrent = document.querySelectorAll('input[name="radio-group-current"]');
  const radioButtonsDesired = document.querySelectorAll('input[name="radio-group-desired"]');
  const radioButtonsCurrentDivision = document.querySelectorAll('input[name="radio-group-current-division"]');
  const radioButtonsDesiredDivision = document.querySelectorAll('input[name="radio-group-desired-division"]');
  
  // Find the initially checked radio button and log its index
  const initiallyCheckedIndexCurrent = Array.from(radioButtonsCurrent).findIndex(radio => radio.checked)+1;
  const initiallyCheckedIndexDesired  = Array.from(radioButtonsDesired).findIndex(radio => radio.checked)+1;

  const initiallyCheckedIndexCurrentDivision  = Array.from(radioButtonsCurrentDivision).findIndex(radio => radio.checked)+1;
  const initiallyCheckedIndexDesiredDivision  = Array.from(radioButtonsDesiredDivision).findIndex(radio => radio.checked)+1;


  if (initiallyCheckedIndexCurrent !== -1 && initiallyCheckedIndexDesired !== -1 && initiallyCheckedIndexCurrentDivision !== -1
    && initiallyCheckedIndexDesiredDivision !== -1)  {
    console.log('Initially checked index For Current:', initiallyCheckedIndexCurrent);
    console.log('Initially checked index For Desired:', initiallyCheckedIndexDesired);
    console.log('Initially checked index For CurrentDivision :', initiallyCheckedIndexCurrentDivision);
    console.log('Initially checked index For CurrentDivision:', initiallyCheckedIndexDesiredDivision);
  } else {
    console.log('No radio buttons is initially checked.');
  }

  function sliceArray(array, start, end) {
    return array.slice(start, end + 1);
  }


  // --------------------->  Sarah Mohamed  (:
  // --------> 
  // -------->
  // pls add real price here in this list , but dont remove 0 number 
  // const divisionPrices [0, listed list of price from iron IV to master  -- listed listed listed **** listed and try (: ]
  const divisionPrices = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29];


  var current_rank = initiallyCheckedIndexCurrent;
  var desired_rank = initiallyCheckedIndexDesired;
  var current_division = initiallyCheckedIndexCurrentDivision;
  var desired_division = initiallyCheckedIndexDesiredDivision;

  function getResult(){
    const startt = ((current_rank-1)*4)+1 + current_division;
    const endd = ((desired_rank-1)*4) + desired_division;
    const slicedArray = sliceArray(divisionPrices, startt, endd);
    console.log(slicedArray);
    const summ = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
    const pricee = document.getElementById('price');
    pricee.innerText = summ;
    console.log(summ);
  }
  getResult();

  // Add change event listener to log the index when a radio button is changed
  radioButtonsCurrent.forEach(function(radio, index) {
    radio.addEventListener('change', function() {
      const selectedIndex = Array.from(radioButtonsCurrent).indexOf(radio);
      console.log('Selected index:', selectedIndex+1);
      current_rank = selectedIndex+1;
      getResult()
    });
  });

  radioButtonsDesired.forEach(function(radio, index) {
    radio.addEventListener('change', function() {
      const selectedIndex = Array.from(radioButtonsDesired).indexOf(radio);
      console.log('Selected index:', selectedIndex+1);
      desired_rank = selectedIndex+1;
      const desired_division_to_hide =  document.getElementById('desired-division');
      if (desired_rank == 8){ 
        desired_division_to_hide.classList.add('d-none');
      }
      else{
        desired_division_to_hide.classList.remove('d-none');
      }
      getResult();
    });
  });

  radioButtonsCurrentDivision.forEach(function(radio, index) {
    radio.addEventListener('change', function() {
      const selectedIndex = Array.from(radioButtonsCurrentDivision).indexOf(radio);
      console.log('Selected Division index:', selectedIndex+1);
      current_division = selectedIndex+1;
      getResult();
    });
  });

  radioButtonsDesiredDivision.forEach(function(radio, index) {
    radio.addEventListener('change', function() {
      const selectedIndex = Array.from(radioButtonsDesiredDivision).indexOf(radio);
      console.log('Selected Division index:', selectedIndex+1);
      desired_division = selectedIndex+1;
      getResult()
    });
  });
});

document.addEventListener("DOMContentLoaded", function() {

  let tairs = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
  let start = 1
  let end = 29
  console.log('hi')


  const radioButtonsCurrent = document.querySelectorAll('input[name="radio-group-current"]');
  const radioButtonsDesired = document.querySelectorAll('input[name="radio-group-desired"]');
  const radioButtonsCurrentDivision = document.querySelectorAll('input[name="radio-group-current-division"]');
  const radioButtonsDesiredDivision = document.querySelectorAll('input[name="radio-group-desired-division"]');
  
  // Find the initially checked radio button and log its index
  const initiallyCheckedIndexCurrent = Array.from(radioButtonsCurrent).findIndex(radio => radio.checked);
  const initiallyCheckedIndexDesired  = Array.from(radioButtonsDesired).findIndex(radio => radio.checked);
  const initiallyCheckedIndexCurrentDivision  = Array.from(radioButtonsCurrentDivision).findIndex(radio => radio.checked);
  const initiallyCheckedIndexDesiredDivision  = Array.from(radioButtonsDesiredDivision).findIndex(radio => radio.checked);

  if (initiallyCheckedIndexCurrent !== -1 && initiallyCheckedIndexDesired !== -1 && initiallyCheckedIndexCurrentDivision !== -1 
    && initiallyCheckedIndexDesiredDivision !== -1)  {
    console.log('Initially checked index For Current:', initiallyCheckedIndexCurrent);
    console.log('Initially checked index For Desired:', initiallyCheckedIndexDesired);
    console.log('Initially checked index For CurrentDivision :', initiallyCheckedIndexCurrentDivision);
    console.log('Initially checked index For CurrentDivision:', initiallyCheckedIndexDesiredDivision);
  } else {
    console.log('No radio buttons is initially checked.');
  }

  // Add change event listener to log the index when a radio button is changed
  radioButtonsCurrent.forEach(function(radio, index) {
    radio.addEventListener('change', function() {
      const selectedIndex = Array.from(radioButtonsCurrent).indexOf(radio);
      console.log('Selected index:', selectedIndex);
    });
  });

  radioButtonsDesired.forEach(function(radio, index) {
    radio.addEventListener('change', function() {
      const selectedIndex = Array.from(radioButtonsDesired).indexOf(radio);
      console.log('Selected index:', selectedIndex);
    });
  });

  radioButtonsCurrentDivision.forEach(function(radio, index) {
    radio.addEventListener('change', function() {
      const selectedIndex = Array.from(radioButtonsCurrentDivision).indexOf(radio);
      console.log('Selected Division index:', selectedIndex);
    });
  });

  radioButtonsDesiredDivision.forEach(function(radio, index) {
    radio.addEventListener('change', function() {
      const selectedIndex = Array.from(radioButtonsDesiredDivision).indexOf(radio);
      console.log('Selected Division index:', selectedIndex);
    });
  });
});

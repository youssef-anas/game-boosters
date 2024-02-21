// Array For Names 
const ranksNames = ['UNRANK', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'CHAMPION', 'GRAND CHAMPION', 'SUPERSONIC LEGEND']

const divisionNames = [0, 'I', 'II', 'III']
// --------- If Customer Come After Choose Booster or For Extend Order ---------
// Get Params
// Assume you have a reference to the HTML element
const orderContainer = document.getElementById('order-container');
const urlParams = new URLSearchParams(window.location.search);
const extend_order = urlParams.get('extend');

// Access the data attribute and convert it to a JavaScript variable
const orderValue = orderContainer.dataset.order;

const valuesAsList = orderValue.split(',')
const rankedtype = valuesAsList[0]
const list1 = valuesAsList.slice(0, 5);
const list2 = valuesAsList.slice(5, 9);

const valuesToSet = list1.map(function(item) {
  return parseInt(item, 10); // Use parseFloat if you have decimal numbers
});

const valuesToSetAdditional = list2.map(value => JSON.parse(value.toLowerCase()));
console.log(valuesAsList)
console.log(valuesToSetAdditional)
console.log(valuesToSet);

// Get the 'choose-booster' query parameter value from the URL
const chooseBoosterValue = urlParams.get('choose_booster');
let chooseBoosterInt = 0
let autoSelectBooster = document.getElementById('selectBoosterApplyButton')
if (chooseBoosterValue != null) {
  chooseBoosterInt = parseInt(chooseBoosterValue, 10);
  autoSelectBooster.click()
}
// Set the value of the input field to the obtained 'choose-booster' value
document.getElementById('chooseBoosterInput').value = chooseBoosterInt;

// Extra Charges Part
// Buttons 
const buttons = {
  duoBoosting: document.querySelector('#duoBoostingButton'),
  selectBooster: document.querySelector('#selectBoosterButton'),
  turboBoost: document.querySelector('#turboBoostButton'),
  streaming: document.querySelector('#streamingButton'),
};

// Content
const contents = {
  duoBoosting: document.querySelector('.duoBoostingContent'),
  selectBooster: document.querySelector('.selectBoosterContent'),
  turboBoost: document.querySelector('.turboBoostContent'),
  streaming: document.querySelector('.streamingContent'),
};

// Apply
const Applybuttons = {
  duoBoosting: document.querySelector('#duoBoostingApplyButton'),
  selectBooster: document.querySelector('#selectBoosterApplyButton'),
  turboBoost: document.querySelector('#turboBoostApplyButton'),
  streaming: document.querySelector('#streamingApplyButton'),
};

// Toggle Function
function toggleContent(content) {
  for (const key in contents) {
    contents[key].style.display = key === content && contents[key].style.display !== 'block' ? 'block' : 'none';
  }
}

// Toggle click event
function setupButtonClickEvent(button, content) {
  button.addEventListener('click', function () {
    toggleContent(content);
  });
}

// Update Percentege
function updateTotalPercentage(percentage, add = true, button) {
  let buttonOldName = buttons[button].innerHTML
  if (add) {
    total_Percentage += percentage;
    $(`.ranked-boost #${button}`).val(true);
    $(`.placements-boost #${button}`).val(true);
    $(`.seasonal-reward #${button}`).val(true);
    $(`.tournament-boost #${button}`).val(true);
    buttons[button].innerHTML = '<i class="fa-solid fa-check"></i>' + buttonOldName;
    Applybuttons[button].innerHTML = 'Cancel'
    Applybuttons[button].classList.remove('applyButton');
    Applybuttons[button].classList.add('cancelButton');
  } else {
    $(`.ranked-boost #${button}`).val(false);
    $(`.placements-boost #${button}`).val(false);
    $(`.seasonal-reward #${button}`).val(false);
    $(`.tournament-boost #${button}`).val(false);
    total_Percentage -= percentage;
    buttons[button].innerHTML = buttonOldName.replace('<i class="fa-solid fa-check"></i>', '');
    Applybuttons[button].innerHTML = 'Apply'
    Applybuttons[button].classList.remove('cancelButton');
    Applybuttons[button].classList.add('applyButton');
  }
}

// Additional Initial Percent
var total_Percentage = 0;

// ----------------------------- Ranked Boost ---------------------------------

// 3vs3 Buttons
const radioButtons3vs3Current = document.querySelectorAll('input[name="radio-group-3vs3-current"]');
const radioButtons3vs3Desired = document.querySelectorAll('input[name="radio-group-3vs3-desired"]');
const radioButtons3vs3CurrentDivision = document.querySelectorAll('input[name="radio-group-current-3vs3-division"]');
const radioButtons3vs3DesiredDivision = document.querySelectorAll('input[name="radio-group-desired-3vs3-division"]');

// 2vs2 Buttons
const radioButtons2vs2Current = document.querySelectorAll('input[name="radio-group-2vs2-current"]');
const radioButtons2vs2Desired = document.querySelectorAll('input[name="radio-group-2vs2-desired"]');
const radioButtons2vs2CurrentDivision = document.querySelectorAll('input[name="radio-group-current-2vs2-division"]');
const radioButtons2vs2DesiredDivision = document.querySelectorAll('input[name="radio-group-desired-2vs2-division"]');

// 1vs1 Buttons
const radioButtons1vs1Current = document.querySelectorAll('input[name="radio-group-1vs1-current"]');
const radioButtons1vs1Desired = document.querySelectorAll('input[name="radio-group-1vs1-desired"]');
const radioButtons1vs1CurrentDivision = document.querySelectorAll('input[name="radio-group-current-1vs1-division"]');
const radioButtons1vs1DesiredDivision = document.querySelectorAll('input[name="radio-group-desired-1vs1-division"]');

// Disable Functions
function setRadioButtonStateWithDisable(radioButtons, values) {
  radioButtons.forEach((radio, index) => {
    // Assuming values in the specified order correspond to radio button indices
    radio.checked = (index === values);
    radio.disabled = true;
  });
}
function setRadioButtonState(radioButtons, values) {
  radioButtons.forEach((radio, index) => {
    radio.checked = (index === values);
    if (index<values){
      radio.disabled = true;
    }
  });
}
function setRadioButtonStateForDesiredDivision(radioButtons, values) {
  radioButtons.forEach((radio, index) => {
    radio.checked = (index === values);
  });
}

// Slice Function
function sliceArray(array, start, end) {
  return array.slice(start, end + 1);
}

// Initail Values
// 3vs3
const initiallyCheckedIndex3vs3Current = Array.from(radioButtons3vs3Current).findIndex(radio => radio.checked) + 1;
const initiallyCheckedIndex3vs3Desired = Array.from(radioButtons3vs3Desired).findIndex(radio => radio.checked) + 1;

const initiallyCheckedIndex3vs3CurrentDivision = Array.from(radioButtons3vs3CurrentDivision).findIndex(radio => radio.checked) + 1;
const initiallyCheckedIndex3vs3DesiredDivision = Array.from(radioButtons3vs3DesiredDivision).findIndex(radio => radio.checked) + 1;

// 2vs2
const initiallyCheckedIndex2vs2Current = Array.from(radioButtons2vs2Current).findIndex(radio => radio.checked) + 1;
const initiallyCheckedIndex2vs2Desired = Array.from(radioButtons2vs2Desired).findIndex(radio => radio.checked) + 1;

const initiallyCheckedIndex2vs2CurrentDivision = Array.from(radioButtons2vs2CurrentDivision).findIndex(radio => radio.checked) + 1;
const initiallyCheckedIndex2vs2DesiredDivision = Array.from(radioButtons2vs2DesiredDivision).findIndex(radio => radio.checked) + 1;

// 1vs1
const initiallyCheckedIndex1vs1Current = Array.from(radioButtons1vs1Current).findIndex(radio => radio.checked) + 1;
const initiallyCheckedIndex1vs1Desired = Array.from(radioButtons1vs1Desired).findIndex(radio => radio.checked) + 1;

const initiallyCheckedIndex1vs1CurrentDivision = Array.from(radioButtons1vs1CurrentDivision).findIndex(radio => radio.checked) + 1;
const initiallyCheckedIndex1vs1DesiredDivision = Array.from(radioButtons1vs1DesiredDivision).findIndex(radio => radio.checked) + 1;

// Read Values From Json File
let divisionPrices = [0];
let marks_price = [[0, 0, 0, 0, 0]];
Promise.all([
  new Promise(function (resolve, reject) {
    $.getJSON('/static/rocketLeague/data/divisions_data.json', function (data) {
      divisionPrices = divisionPrices.concat(...data);
      resolve();
    });
  })
]).then(function () {
  // Variable That I Use
  // 3vs3
  var current_rank_3vs3 = initiallyCheckedIndex3vs3Current;
  var desired_rank_3vs3 = initiallyCheckedIndex3vs3Desired;
  var current_division_3vs3 = initiallyCheckedIndex3vs3CurrentDivision;
  var desired_division_3vs3 = initiallyCheckedIndex3vs3DesiredDivision;
  var current_rank_name_3vs3 = ranksNames[initiallyCheckedIndex3vs3Current];
  var desired_rank_name_3vs3 = ranksNames[initiallyCheckedIndex3vs3Desired];
  var current_division_name_3vs3 = divisionNames[initiallyCheckedIndex3vs3CurrentDivision];
  var desired_division_name_3vs3 = divisionNames[initiallyCheckedIndex3vs3DesiredDivision];

  // 2vs2
  var current_rank_2vs2 = initiallyCheckedIndex2vs2Current;
  var desired_rank_2vs2 = initiallyCheckedIndex2vs2Desired;
  var current_division_2vs2 = initiallyCheckedIndex2vs2CurrentDivision;
  var desired_division_2vs2 = initiallyCheckedIndex2vs2DesiredDivision;
  var current_rank_name_2vs2 = ranksNames[initiallyCheckedIndex2vs2Current];
  var desired_rank_name_2vs2 = ranksNames[initiallyCheckedIndex2vs2Desired];
  var current_division_name_2vs2 = divisionNames[initiallyCheckedIndex2vs2CurrentDivision];
  var desired_division_name_2vs2 = divisionNames[initiallyCheckedIndex2vs2DesiredDivision];

  // 1vs1
  var current_rank_1vs1 = initiallyCheckedIndex1vs1Current;
  var desired_rank_1vs1 = initiallyCheckedIndex1vs1Desired;
  var current_division_1vs1 = initiallyCheckedIndex1vs1CurrentDivision;
  var desired_division_1vs1 = initiallyCheckedIndex1vs1DesiredDivision;
  var current_rank_name_1vs1 = ranksNames[initiallyCheckedIndex1vs1Current];
  var desired_rank_name_1vs1 = ranksNames[initiallyCheckedIndex1vs1Desired];
  var current_division_name_1vs1 = divisionNames[initiallyCheckedIndex1vs1CurrentDivision];
  var desired_division_name_1vs1 = divisionNames[initiallyCheckedIndex1vs1DesiredDivision];

  // Apply Extra Button
  function setupApplyButtonClickEvent(button, percentage) {
    Applybuttons[button].addEventListener('click', function () {
      updateTotalPercentage(percentage, !Applybuttons[button].classList.contains('cancelButton'), button);
      get3vs3RankedPrice();
      get2vs2RankedPrice();
      get1vs1RankedPrice();
      getPlacementPrice();
      getSeasonalPrice();
    });
  }

  // Setup click events for each button
  for (const key in buttons) {
    setupButtonClickEvent(buttons[key], key);
  }
  setupApplyButtonClickEvent('duoBoosting', 0.65);
  setupApplyButtonClickEvent('selectBooster', 0.05);
  setupApplyButtonClickEvent('turboBoost', 0.20);
  setupApplyButtonClickEvent('streaming', 0.15);

  // Extend
  if (extend_order) {
    let orderID = parseInt(extend_order, 10);
    document.getElementById('extendOrder').value = orderID;

    // Set the checked state for each group of radio buttons using the specified order
    // 3vs3
    if(rankedtype == 3) {
      setRadioButtonStateWithDisable(radioButtons3vs3Current, valuesToSet[1]-1);
      setRadioButtonStateWithDisable(radioButtons3vs3CurrentDivision, valuesToSet[2]-1);
      setRadioButtonState(radioButtons3vs3Desired, valuesToSet[3]-1, true);
      setRadioButtonStateForDesiredDivision(radioButtons3vs3DesiredDivision, valuesToSet[4]-1);
    } 
    // 2vs2
    else if(rankedtype == 2) {
      setRadioButtonStateWithDisable(radioButtons2vs2Current, valuesToSet[1]-1);
      setRadioButtonStateWithDisable(radioButtons2vs2CurrentDivision, valuesToSet[2]-1);
      setRadioButtonState(radioButtons2vs2Desired, valuesToSet[3]-1, true);
      setRadioButtonStateForDesiredDivision(radioButtons2vs2DesiredDivision, valuesToSet[4]-1);
    }
    // 1vs1
    else if(rankedtype == 1) {
      setRadioButtonStateWithDisable(radioButtons1vs1Current, valuesToSet[1]-1);
      setRadioButtonStateWithDisable(radioButtons1vs1CurrentDivision, valuesToSet[2]-1);
      setRadioButtonState(radioButtons1vs1Desired, valuesToSet[3]-1, true);
      setRadioButtonStateForDesiredDivision(radioButtons1vs1DesiredDivision, valuesToSet[4]-1);
    }

    // 3vs3
    current_rank_3vs3 = valuesToSet[1];
    current_division_3vs3 = valuesToSet[2];
    desired_rank_3vs3 = valuesToSet[3];
    desired_division_3vs3 = valuesToSet[4];
    var current_rank_name_3vs3 = ranksNames[current_rank_3vs3];
    var desired_rank_name_3vs3 = ranksNames[desired_rank_3vs3];
    var current_division_name_3vs3 = divisionNames[current_division_3vs3];
    var desired_division_name_3vs3 = divisionNames[desired_division_3vs3];

    // 2vs2
    current_rank_2vs2 = valuesToSet[1];
    current_division_2vs2 = valuesToSet[2];
    desired_rank_2vs2 = valuesToSet[3];
    desired_division_2vs2 = valuesToSet[4];
    var current_rank_name_2vs2 = ranksNames[current_rank_2vs2];
    var desired_rank_name_2vs2 = ranksNames[desired_rank_2vs2];
    var current_division_name_2vs2 = divisionNames[current_division_2vs2];
    var desired_division_name_3vs3 = divisionNames[desired_division_2vs2];

    // 1vs1
    current_rank_1vs1 = valuesToSet[1];
    current_division_1vs1 = valuesToSet[2];
    desired_rank_1vs1 = valuesToSet[3];
    desired_division_1vs1 = valuesToSet[4];
    var current_rank_name_1vs1 = ranksNames[current_rank_1vs1];
    var desired_rank_name_1vs1 = ranksNames[desired_rank_1vs1];
    var current_division_name_1vs1 = divisionNames[current_division_1vs1];
    var desired_division_name_1vs1 = divisionNames[desired_division_1vs1];

    let duoBoostingApply= document.getElementById('duoBoostingApplyButton')
    let turboBoostApply = document.getElementById('turboBoostApplyButton')
    let streamingApply = document.getElementById('streamingApplyButton')

    // Function to set checkbox state based on values
    function setCheckboxState(button, value) {
      console.log('Setting button state for', button.id, 'to', value);
      if (value === true) {
        $(button).trigger('click');
        console.log('Checkbox clicked successfully');
      }
    }

    // Set the state of each checkbox based on the values list
    setCheckboxState(duoBoostingApply, valuesToSetAdditional[0]);
    setCheckboxState(autoSelectBooster, valuesToSetAdditional[1]);
    setCheckboxState(turboBoostApply, valuesToSetAdditional[2]);
    setCheckboxState(streamingApply, valuesToSetAdditional[3]);
  }

  if (extend_order) {
    if(rankedtype == 3) {
      $("#ranked3vs3-boost").click()
      // 3vs3
      function get3vs3RankedPrice() {
        const startRank = ((valuesToSet[3] - 1) * 3) + valuesToSet[4];
        const endRank = ((desired_rank_3vs3 - 1) * 3) + desired_division_3vs3-1;
        const slicedArray = sliceArray(divisionPrices, startRank, endRank);
        let sum = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
        console.log(slicedArray)
        console.log(divisionPrices)
  
        // Apply extra charges to the result
        sum += sum * total_Percentage;
        sum = parseFloat(sum.toFixed(2)); 
  
        const pricee = document.querySelector('.price-data.ranked3vs3-boost');
        pricee.innerHTML = `
        <p class='fs-5 text-uppercase my-4 text-secondary'>Boosting <span class='fw-bold text-white'>From ${current_rank_name_3vs3} ${current_division_name_3vs3} to ${ranksNames[valuesToSet[3]]} ${divisionNames[valuesToSet[4]] } </span></p>
        <p class='fs-5 text-uppercase my-4 text-secondary'>Extend <span class='fw-bold text-white'>From ${ranksNames[valuesToSet[3]]} ${divisionNames[valuesToSet[4]]} to ${desired_rank_name_3vs3} ${desired_division_name_3vs3} </span></p>
        <span class='fs-5 text-uppercase fw-bold'>Extra Cost: $${sum}</span>
      `;
  
        // From Value
        if ($('.ranked-boost input[name="ranked_type"]').val() == 3) {
          $('.ranked-boost input[name="current_rank"]').val(current_rank_3vs3);
          $('.ranked-boost input[name="current_division"]').val(current_division_3vs3);
          $('.ranked-boost input[name="desired_rank"]').val(desired_rank_3vs3);
          $('.ranked-boost input[name="desired_division"]').val(desired_division_3vs3);
          $('.ranked-boost input[name="price"]').val(sum);
        }
      }

      // 2vs2
      function get2vs2RankedPrice() {
        const startRank = ((current_rank_2vs2 - 1) * 3) + current_division_2vs2;
        const endRank = ((desired_rank_2vs2 - 1) * 3) + desired_division_2vs2 - 1;
        const slicedArray = sliceArray(divisionPrices, startRank, endRank);
        let result = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
    
        // Apply extra charges to the result
        result += result * total_Percentage;
        result = parseFloat(result.toFixed(2)); 
    
        const pricee = document.querySelector('.price-data.ranked2vs2-boost');
        pricee.innerHTML = `<p class='fs-5 text-uppercase my-4 text-secondary'>Boosting <span class='fw-bold text-white'>From ${current_rank_name_2vs2} ${current_division_name_2vs2} to ${desired_rank_name_2vs2} ${desired_division_name_2vs2} </span></p>
        <span class='fs-5 text-uppercase fw-bold'>Total Cost: $${result}</span>`;
    
        console.log('Result', result)
        // From Value
        if ($('.ranked-boost input[name="game_type"]').val() == 'D' && $('.ranked-boost input[name="ranked_type"]').val() == 2) {
          $('.ranked-boost input[name="current_rank"]').val(current_rank_2vs2);
          $('.ranked-boost input[name="current_division"]').val(current_division_2vs2);
          $('.ranked-boost input[name="desired_rank"]').val(desired_rank_2vs2);
          $('.ranked-boost input[name="desired_division"]').val(desired_division_2vs2);
          $('.ranked-boost input[name="price"]').val(result);
        }
      }

      // 1vs1
      function get1vs1RankedPrice() {
        const startRank = ((current_rank_1vs1 - 1) * 3) + current_division_1vs1;
        const endRank = ((desired_rank_1vs1 - 1) * 3) + desired_division_1vs1 - 1;
        const slicedArray = sliceArray(divisionPrices, startRank, endRank);
        let result = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
    
        // Apply extra charges to the result
        result += result * total_Percentage;
        result = parseFloat(result.toFixed(2)); 
    
        const pricee = document.querySelector('.price-data.ranked1vs1-boost');
        pricee.innerHTML = `<p class='fs-5 text-uppercase my-4 text-secondary'>Boosting <span class='fw-bold text-white'>From ${current_rank_name_1vs1} ${current_division_name_1vs1} to ${desired_rank_name_1vs1} ${desired_division_name_1vs1} </span></p>
        <span class='fs-5 text-uppercase fw-bold'>Total Cost: $${result}</span>`;
    
        console.log('Result', result)
        // From Value
        if ($('.ranked-boost input[name="game_type"]').val() == 'D' && $('.ranked-boost input[name="ranked_type"]').val() == 1) {
          $('.ranked-boost input[name="current_rank"]').val(current_rank_1vs1);
          $('.ranked-boost input[name="current_division"]').val(current_division_1vs1);
          $('.ranked-boost input[name="desired_rank"]').val(desired_rank_1vs1);
          $('.ranked-boost input[name="desired_division"]').val(desired_division_1vs1);
          $('.ranked-boost input[name="price"]').val(result);
        }
      }
    } else if (rankedtype == 2) {
      $("#ranked2vs2-boost").click()
      // 2vs2
      function get2vs2RankedPrice() {
        const startRank = ((valuesToSet[3] - 1) * 3) + valuesToSet[4];
        const endRank = ((desired_rank_2vs2 - 1) * 3) + desired_division_2vs2-1;
        const slicedArray = sliceArray(divisionPrices, startRank, endRank);
        let sum = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
        console.log(slicedArray)
        console.log(divisionPrices)
  
        // Apply extra charges to the result
        sum += sum * total_Percentage;
        sum = parseFloat(sum.toFixed(2)); 
  
        const pricee = document.querySelector('.price-data.ranked2vs2-boost');
        pricee.innerHTML = `
        <p class='fs-5 text-uppercase my-4 text-secondary'>Boosting <span class='fw-bold text-white'>From ${current_rank_name_2vs2} ${current_division_name_2vs2} to ${ranksNames[valuesToSet[3]]} ${divisionNames[valuesToSet[4]] } </span></p>
        <p class='fs-5 text-uppercase my-4 text-secondary'>Extend <span class='fw-bold text-white'>From ${ranksNames[valuesToSet[3]]} ${divisionNames[valuesToSet[4]]} to ${desired_rank_name_2vs2} ${desired_division_name_2vs2} </span></p>
        <span class='fs-5 text-uppercase fw-bold'>Extra Cost: $${sum}</span>
      `;
  
        // From Value
        if ($('.ranked-boost input[name="ranked_type"]').val() == 2) { 
          $('.ranked-boost input[name="current_rank"]').val(current_rank_2vs2);
          $('.ranked-boost input[name="current_division"]').val(current_division_2vs2);
          $('.ranked-boost input[name="desired_rank"]').val(desired_rank_2vs2);
          $('.ranked-boost input[name="desired_division"]').val(desired_division_2vs2);
          $('.ranked-boost input[name="price"]').val(sum);
        }
      }

      // 3vs3
      function get3vs3RankedPrice() {
        const startRank = ((current_rank_3vs3 - 1) * 3) + current_division_3vs3;
        const endRank = ((desired_rank_3vs3 - 1) * 3) + desired_division_3vs3 - 1;
        const slicedArray = sliceArray(divisionPrices, startRank, endRank);
        let result = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
    
        // Apply extra charges to the result
        result += result * total_Percentage;
        result = parseFloat(result.toFixed(2)); 
    
        const pricee = document.querySelector('.price-data.ranked3vs3-boost');
        pricee.innerHTML = `
        <p class='fs-5 text-uppercase my-4 text-secondary'>Boosting <span class='fw-bold text-white'>From ${current_rank_name_3vs3} ${current_division_name_3vs3} to ${desired_rank_name_3vs3} ${desired_division_name_3vs3} </span></p>
        <span class='fs-5 text-uppercase fw-bold'>Total Cost: $${result}</span>
      `;
    
        console.log('Result', result)
        // From Value
        if ($('.ranked-boost input[name="game_type"]').val() == 'D' && $('.ranked-boost input[name="ranked_type"]').val() == 3) {
          $('.ranked-boost input[name="current_rank"]').val(current_rank_3vs3);
          $('.ranked-boost input[name="current_division"]').val(current_division_3vs3);
          $('.ranked-boost input[name="desired_rank"]').val(desired_rank_3vs3);
          $('.ranked-boost input[name="desired_division"]').val(desired_division_3vs3);
          $('.ranked-boost input[name="price"]').val(result);
        }
      }

      // 1vs1
      function get1vs1RankedPrice() {
        const startRank = ((current_rank_1vs1 - 1) * 3) + current_division_1vs1;
        const endRank = ((desired_rank_1vs1 - 1) * 3) + desired_division_1vs1 - 1;
        const slicedArray = sliceArray(divisionPrices, startRank, endRank);
        let result = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
    
        // Apply extra charges to the result
        result += result * total_Percentage;
        result = parseFloat(result.toFixed(2)); 
    
        const pricee = document.querySelector('.price-data.ranked1vs1-boost');
        pricee.innerHTML = `<p class='fs-5 text-uppercase my-4 text-secondary'>Boosting <span class='fw-bold text-white'>From ${current_rank_name_1vs1} ${current_division_name_1vs1} to ${desired_rank_name_1vs1} ${desired_division_name_1vs1} </span></p>
        <span class='fs-5 text-uppercase fw-bold'>Total Cost: $${result}</span>`;
    
        console.log('Result', result)
        // From Value
        if ($('.ranked-boost input[name="game_type"]').val() == 'D' && $('.ranked-boost input[name="ranked_type"]').val() == 1) {
          $('.ranked-boost input[name="current_rank"]').val(current_rank_1vs1);
          $('.ranked-boost input[name="current_division"]').val(current_division_1vs1);
          $('.ranked-boost input[name="desired_rank"]').val(desired_rank_1vs1);
          $('.ranked-boost input[name="desired_division"]').val(desired_division_1vs1);
          $('.ranked-boost input[name="price"]').val(result);
        }
      }
    } else if (rankedtype == 1) {
      $("#ranked1vs1-boost").click()
      // 1vs1
      function get1vs1RankedPrice() {
        const startRank = ((valuesToSet[3] - 1) * 3) + valuesToSet[4];
        const endRank = ((desired_rank_1vs1 - 1) * 3) + desired_division_1vs1-1;
        const slicedArray = sliceArray(divisionPrices, startRank, endRank);
        let sum = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
        console.log(slicedArray)
        console.log(divisionPrices)
  
        // Apply extra charges to the result
        sum += sum * total_Percentage;
        sum = parseFloat(sum.toFixed(2)); 
  
        const pricee = document.querySelector('.price-data.ranked1vs1-boost');
        pricee.innerHTML = `
        <p class='fs-5 text-uppercase my-4 text-secondary'>Boosting <span class='fw-bold text-white'>From ${current_rank_name_1vs1} ${current_division_name_1vs1} to ${ranksNames[valuesToSet[3]]} ${divisionNames[valuesToSet[4]] } </span></p>
        <p class='fs-5 text-uppercase my-4 text-secondary'>Extend <span class='fw-bold text-white'>From ${ranksNames[valuesToSet[3]]} ${divisionNames[valuesToSet[4]]} to ${desired_rank_name_1vs1} ${desired_division_name_1vs1} </span></p>
        <span class='fs-5 text-uppercase fw-bold'>Extra Cost: $${sum}</span>
      `;
  
        // From Value
        if ($('.ranked-boost input[name="ranked_type"]').val() == 1) {
          $('.ranked-boost input[name="current_rank"]').val(current_rank_1vs1);
          $('.ranked-boost input[name="current_division"]').val(current_division_1vs1);
          $('.ranked-boost input[name="desired_rank"]').val(desired_rank_1vs1);
          $('.ranked-boost input[name="desired_division"]').val(desired_division_1vs1);
          $('.ranked-boost input[name="price"]').val(sum);
        }
      }

      // 3vs3
      function get3vs3RankedPrice() {
        const startRank = ((current_rank_3vs3 - 1) * 3) + current_division_3vs3;
        const endRank = ((desired_rank_3vs3 - 1) * 3) + desired_division_3vs3 - 1;
        const slicedArray = sliceArray(divisionPrices, startRank, endRank);
        let result = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
    
        // Apply extra charges to the result
        result += result * total_Percentage;
        result = parseFloat(result.toFixed(2)); 
    
        const pricee = document.querySelector('.price-data.ranked3vs3-boost');
        pricee.innerHTML = `
        <p class='fs-5 text-uppercase my-4 text-secondary'>Boosting <span class='fw-bold text-white'>From ${current_rank_name_3vs3} ${current_division_name_3vs3} to ${desired_rank_name_3vs3} ${desired_division_name_3vs3} </span></p>
        <span class='fs-5 text-uppercase fw-bold'>Total Cost: $${result}</span>
      `;
    
        console.log('Result', result)
        // From Value
        if ($('.ranked-boost input[name="game_type"]').val() == 'D' && $('.ranked-boost input[name="ranked_type"]').val() == 3) {
          $('.ranked-boost input[name="current_rank"]').val(current_rank_3vs3);
          $('.ranked-boost input[name="current_division"]').val(current_division_3vs3);
          $('.ranked-boost input[name="desired_rank"]').val(desired_rank_3vs3);
          $('.ranked-boost input[name="desired_division"]').val(desired_division_3vs3);
          $('.ranked-boost input[name="price"]').val(result);
        }
      }

      // 2vs2
      function get2vs2RankedPrice() {
        const startRank = ((current_rank_2vs2 - 1) * 3) + current_division_2vs2;
        const endRank = ((desired_rank_2vs2 - 1) * 3) + desired_division_2vs2 - 1;
        const slicedArray = sliceArray(divisionPrices, startRank, endRank);
        let result = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
    
        // Apply extra charges to the result
        result += result * total_Percentage;
        result = parseFloat(result.toFixed(2)); 
    
        const pricee = document.querySelector('.price-data.ranked2vs2-boost');
        pricee.innerHTML = `<p class='fs-5 text-uppercase my-4 text-secondary'>Boosting <span class='fw-bold text-white'>From ${current_rank_name_2vs2} ${current_division_name_2vs2} to ${desired_rank_name_2vs2} ${desired_division_name_2vs2} </span></p>
        <span class='fs-5 text-uppercase fw-bold'>Total Cost: $${result}</span>`;
    
        console.log('Result', result)
        // From Value
        if ($('.ranked-boost input[name="game_type"]').val() == 'D' && $('.ranked-boost input[name="ranked_type"]').val() == 2) {
          $('.ranked-boost input[name="current_rank"]').val(current_rank_2vs2);
          $('.ranked-boost input[name="current_division"]').val(current_division_2vs2);
          $('.ranked-boost input[name="desired_rank"]').val(desired_rank_2vs2);
          $('.ranked-boost input[name="desired_division"]').val(desired_division_2vs2);
          $('.ranked-boost input[name="price"]').val(result);
        }
      }
    }
  } else {
    // Get Result Function
    // 3vs3
    function get3vs3RankedPrice() {
      const startRank = ((current_rank_3vs3 - 1) * 3) + current_division_3vs3;
      const endRank = ((desired_rank_3vs3 - 1) * 3) + desired_division_3vs3 - 1;
      const slicedArray = sliceArray(divisionPrices, startRank, endRank);
      let result = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
  
      // Apply extra charges to the result
      result += result * total_Percentage;
      result = parseFloat(result.toFixed(2)); 
  
      const pricee = document.querySelector('.price-data.ranked3vs3-boost');
      pricee.innerHTML = `
      <p class='fs-5 text-uppercase my-4 text-secondary'>Boosting <span class='fw-bold text-white'>From ${current_rank_name_3vs3} ${current_division_name_3vs3} to ${desired_rank_name_3vs3} ${desired_division_name_3vs3} </span></p>
      <span class='fs-5 text-uppercase fw-bold'>Total Cost: $${result}</span>
    `;
  
      console.log('Result', result)
      // From Value
      if ($('.ranked-boost input[name="game_type"]').val() == 'D' && $('.ranked-boost input[name="ranked_type"]').val() == 3) {
        $('.ranked-boost input[name="current_rank"]').val(current_rank_3vs3);
        $('.ranked-boost input[name="current_division"]').val(current_division_3vs3);
        $('.ranked-boost input[name="desired_rank"]').val(desired_rank_3vs3);
        $('.ranked-boost input[name="desired_division"]').val(desired_division_3vs3);
        $('.ranked-boost input[name="price"]').val(result);
      }
    }

    // 2vs2
    function get2vs2RankedPrice() {
      const startRank = ((current_rank_2vs2 - 1) * 3) + current_division_2vs2;
      const endRank = ((desired_rank_2vs2 - 1) * 3) + desired_division_2vs2 - 1;
      const slicedArray = sliceArray(divisionPrices, startRank, endRank);
      let result = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
  
      // Apply extra charges to the result
      result += result * total_Percentage;
      result = parseFloat(result.toFixed(2)); 
  
      const pricee = document.querySelector('.price-data.ranked2vs2-boost');
      pricee.innerHTML = `<p class='fs-5 text-uppercase my-4 text-secondary'>Boosting <span class='fw-bold text-white'>From ${current_rank_name_2vs2} ${current_division_name_2vs2} to ${desired_rank_name_2vs2} ${desired_division_name_2vs2} </span></p>
      <span class='fs-5 text-uppercase fw-bold'>Total Cost: $${result}</span>`;
  
      console.log('Result', result)
      // From Value
      if ($('.ranked-boost input[name="game_type"]').val() == 'D' && $('.ranked-boost input[name="ranked_type"]').val() == 2) {
        $('.ranked-boost input[name="current_rank"]').val(current_rank_2vs2);
        $('.ranked-boost input[name="current_division"]').val(current_division_2vs2);
        $('.ranked-boost input[name="desired_rank"]').val(desired_rank_2vs2);
        $('.ranked-boost input[name="desired_division"]').val(desired_division_2vs2);
        $('.ranked-boost input[name="price"]').val(result);
      }
    }

    // 1vs1
    function get1vs1RankedPrice() {
      const startRank = ((current_rank_1vs1 - 1) * 3) + current_division_1vs1;
      const endRank = ((desired_rank_1vs1 - 1) * 3) + desired_division_1vs1 - 1;
      const slicedArray = sliceArray(divisionPrices, startRank, endRank);
      let result = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
  
      // Apply extra charges to the result
      result += result * total_Percentage;
      result = parseFloat(result.toFixed(2)); 
  
      const pricee = document.querySelector('.price-data.ranked1vs1-boost');
      pricee.innerHTML = `<p class='fs-5 text-uppercase my-4 text-secondary'>Boosting <span class='fw-bold text-white'>From ${current_rank_name_1vs1} ${current_division_name_1vs1} to ${desired_rank_name_1vs1} ${desired_division_name_1vs1} </span></p>
      <span class='fs-5 text-uppercase fw-bold'>Total Cost: $${result}</span>`;
  
      console.log('Result', result)
      // From Value
      if ($('.ranked-boost input[name="game_type"]').val() == 'D' && $('.ranked-boost input[name="ranked_type"]').val() == 1) {
        $('.ranked-boost input[name="current_rank"]').val(current_rank_1vs1);
        $('.ranked-boost input[name="current_division"]').val(current_division_1vs1);
        $('.ranked-boost input[name="desired_rank"]').val(desired_rank_1vs1);
        $('.ranked-boost input[name="desired_division"]').val(desired_division_1vs1);
        $('.ranked-boost input[name="price"]').val(result);
      }
    }
  }

  // Get Result 
  get3vs3RankedPrice();
  get2vs2RankedPrice();
  get1vs1RankedPrice();

  // Current Rank 3vs3 Change
  radioButtons3vs3Current.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtons3vs3Current).indexOf(radio);
      current_rank_3vs3 = selectedIndex + 1;
      current_rank_name_3vs3 = ranksNames[current_rank_3vs3];
      get3vs3RankedPrice();
    });
  });

  // Current Rank 2vs2 Change
  radioButtons2vs2Current.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtons2vs2Current).indexOf(radio);
      current_rank_2vs2 = selectedIndex + 1;
      current_rank_name_2vs2 = ranksNames[current_rank_2vs2];
      get2vs2RankedPrice();
    });
  });

  // Current Rank 1vs1 Change
  radioButtons1vs1Current.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtons1vs1Current).indexOf(radio);
      current_rank_1vs1 = selectedIndex + 1;
      current_rank_name_1vs1 = ranksNames[current_rank_1vs1];
      get1vs1RankedPrice();
    });
  });

  // Desired Rank 3vs3 Change
  radioButtons3vs3Desired.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtons3vs3Desired).indexOf(radio);
      desired_rank_3vs3 = selectedIndex + 1;
      desired_rank_name_3vs3 = ranksNames[desired_rank_3vs3]
      
      get3vs3RankedPrice();
    });
  });

  // Desired Rank 2vs2 Change
  radioButtons2vs2Desired.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtons2vs2Desired).indexOf(radio);
      desired_rank_2vs2 = selectedIndex + 1;
      desired_rank_name_2vs2 = ranksNames[desired_rank_2vs2]
      
      get2vs2RankedPrice();
    });
  });

  // Desired Rank 1vs1 Change
  radioButtons1vs1Desired.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtons1vs1Desired).indexOf(radio);
      desired_rank_1vs1 = selectedIndex + 1;
      desired_rank_name_1vs1 = ranksNames[desired_rank_1vs1]
      
      get1vs1RankedPrice();
    });
  });

  // Current Division 3vs3 Change
  radioButtons3vs3CurrentDivision.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtons3vs3CurrentDivision).indexOf(radio);
      current_division_3vs3 = selectedIndex + 1;
      current_division_name_3vs3 = divisionNames[current_division_3vs3]
      get3vs3RankedPrice();
    });
  })

  // Current Division 2vs2 Change
  radioButtons2vs2CurrentDivision.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtons2vs2CurrentDivision).indexOf(radio);
      current_division_2vs2 = selectedIndex + 1;
      current_division_name_2vs2 = divisionNames[current_division_2vs2]
      get2vs2RankedPrice();
    });
  })

  // Current Division 1vs1 Change
  radioButtons1vs1CurrentDivision.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtons1vs1CurrentDivision).indexOf(radio);
      current_division_1vs1 = selectedIndex + 1;
      current_division_name_1vs1 = divisionNames[current_division_1vs1]
      get1vs1RankedPrice();
    });
  })

  // Desired Division 3vs3 Change
  radioButtons3vs3DesiredDivision.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtons3vs3DesiredDivision).indexOf(radio);
      desired_division_3vs3 = selectedIndex + 1;
      desired_division_name_3vs3 = divisionNames[desired_division_3vs3]
      get3vs3RankedPrice()
    });
  });

  // Desired Division 2vs2 Change
  radioButtons2vs2DesiredDivision.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtons2vs2DesiredDivision).indexOf(radio);
      desired_division_2vs2 = selectedIndex + 1;
      desired_division_name_2vs2 = divisionNames[desired_division_2vs2]
      get2vs2RankedPrice()
    });
  });

  // Desired Division 1vs1 Change
  radioButtons1vs1DesiredDivision.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtons1vs1DesiredDivision).indexOf(radio);
      desired_division_1vs1 = selectedIndex + 1;
      desired_division_name_1vs1 = divisionNames[desired_division_1vs1]
      get1vs1RankedPrice()
    });
  });

});

// ----------------------------- Placments Boost ---------------------------------
const placementRank = $('input[name="radio-group-placement-ranks"]');
const gameCountSlider = $("#game-count");
const gameCountValue = $(".game-count-value");
const gameCounterInitial = Number(gameCountSlider.val())
const initiallyPlacementCheckedIndexRank = $('input[name="radio-group-placement-ranks"]').index($('input[name="radio-group-placement-ranks"]:checked'));
const initiallyPlacementCheckedRank = $('input[name="radio-group-placement-ranks"]').eq(initiallyPlacementCheckedIndexRank);
const initiallyPlacementCheckedIndexRankPrice = initiallyPlacementCheckedRank.data('price');

let last_rank = initiallyPlacementCheckedIndexRank + 1
let placementRankPrice = initiallyPlacementCheckedIndexRankPrice
let gameCounter = gameCounterInitial

const getPlacementPrice = () => {
  let price = (placementRankPrice * gameCounter);
  price = parseFloat(price + (price * total_Percentage)).toFixed(2)
  const priceDiv = $('.price-data.placements-boost').eq(0);
  priceDiv.html(`
  <p class='fs-5 text-uppercase my-4 text-secondary'>Boosting of <span class='fw-bold text-white'>${gameCounter} Placement Games</span></p>
  <h4>$${price}</h4>
  `);

  if ($('.placements-boost input[name="game_type"]').val() == 'P') {
    $('.placements-boost input[name="last_rank"]').val(last_rank);
    $('.placements-boost input[name="number_of_match"]').val(gameCounter);
    $('.placements-boost input[name="price"]').val(price);
  }
}
getPlacementPrice()

placementRank.each(function (index, radio) {
  $(radio).on('change', function () {
    const selectedIndex = placementRank.index(radio) + 1;
    last_rank = selectedIndex;
    placementRankPrice = $(radio).data('price');
    getPlacementPrice()
  });
});

gameCountSlider.on("input", function (event) {
  gameCounter = Number(event.target.value);

  gameCountValue.text(gameCounter);

  const progress = (gameCounter / gameCountSlider.prop("max")) * 100;

  gameCountSlider.css("background", `linear-gradient(to right, var(--main-color) ${progress}%, #ccc ${progress}%)`);

  gameCountSlider.css("--thumb-rotate", `${(gameCounter / 100) * 2160}deg`);

  getPlacementPrice()
});

// ----------------------------- Seasonal Reward ---------------------------------
const seasonalRank = $('input[name="radio-group-seasonal-ranks"]');
const numberWinSlider = $("#num-win");
const numberWinValue = $(".number-win-value");
const numberWinInitial = Number(numberWinSlider.val())
const initiallySeasonalCheckedIndexRank = $('input[name="radio-group-seasonal-ranks"]').index($('input[name="radio-group-seasonal-ranks"]:checked'));
const initiallySeasonalCheckedRank = $('input[name="radio-group-seasonal-ranks"]').eq(initiallySeasonalCheckedIndexRank);
const initiallySeasonalCheckedIndexRankPrice = initiallySeasonalCheckedRank.data('price');

let current_rank = initiallySeasonalCheckedIndexRank + 1
let seasonalRankPrice = initiallySeasonalCheckedIndexRankPrice
let numberWin = numberWinInitial

const getSeasonalPrice = () => {
  let price = (seasonalRankPrice * numberWin);
  price = parseFloat(price + (price * total_Percentage)).toFixed(2)
  const priceDiv = $('.price-data.seasonal-reward').eq(0);
  priceDiv.html(`
  <p class='fs-5 text-uppercase my-4 text-secondary'>Seasonal Reward Boosting by <span class='fw-bold text-white'>${numberWin} Wins</span></p>
  <h4>$${price}</h4>
  `);

  if ($('.seasonal-reward input[name="game_type"]').val() == 'S') {
    $('.seasonal-reward input[name="current_rank"]').val(current_rank);
    $('.seasonal-reward input[name="number_of_wins"]').val(numberWin);
    $('.seasonal-reward input[name="price"]').val(price);
  }
}
getSeasonalPrice()

seasonalRank.each(function (index, radio) {
  $(radio).on('change', function () {
    const selectedIndex = seasonalRank.index(radio) + 1;
    current_rank = selectedIndex;
    seasonalRankPrice = $(radio).data('price');
    getSeasonalPrice()
  });
});

numberWinSlider.on("input", function (event) {
  numberWin = Number(event.target.value);

  numberWinValue.text(numberWin);

  const progress = (numberWin / numberWinSlider.prop("max")) * 100;

  numberWinSlider.css("background", `linear-gradient(to right, var(--main-color) ${progress}%, #ccc ${progress}%)`);

  numberWinSlider.css("--thumb-rotate", `${(numberWin / 100) * 2160}deg`);

  getSeasonalPrice()
});

// ----------------------------- Tournament Boost ---------------------------------
const tournamentRank = $('input[name="radio-group-tournament-ranks"]');
const initiallyTournamentCheckedIndexRank = $('input[name="radio-group-tournament-ranks"]').index($('input[name="radio-group-tournament-ranks"]:checked'));
const initiallyTournamentCheckedRank = $('input[name="radio-group-tournament-ranks"]').eq(initiallyTournamentCheckedIndexRank);
const initiallyTournamentCheckedIndexRankPrice = initiallyTournamentCheckedRank.data('price');

let current_league = initiallyTournamentCheckedIndexRank + 1
let tournamentRankPrice = initiallyTournamentCheckedIndexRankPrice

const getTournamentPrice = () => {
  let price = tournamentRankPrice;
  price = parseFloat(price + (price * total_Percentage)).toFixed(2)
  const priceDiv = $('.price-data.tournament-boost').eq(0);
  priceDiv.html(`
  <p class='fs-5 text-uppercase my-4 text-secondary'>${ranksNames[current_league]} League <span class='fw-bold text-white'>Tournament Win</span></p>
  <h4>$${price}</h4>
  `);

  if ($('.tournament-boost input[name="game_type"]').val() == 'T') {
    $('.tournament-boost input[name="current_league"]').val(current_league);
    $('.tournament-boost input[name="price"]').val(price);
  }
}
getTournamentPrice()

tournamentRank.each(function (index, radio) {
  $(radio).on('change', function () {
    const selectedIndex = tournamentRank.index(radio) + 1;
    current_league = selectedIndex;
    tournamentRankPrice = $(radio).data('price');
    getTournamentPrice()
  });
});
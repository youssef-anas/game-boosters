
// ----------------------------- Division Boost ---------------------------------

// Buttons
const radioButtonsCurrent = document.querySelectorAll('input[name="radio-group-current"]');
const radioButtonsDesired = document.querySelectorAll('input[name="radio-group-desired"]');
const radioButtonsCurrentDivision = document.querySelectorAll('input[name="radio-group-current-division"]');
const radioButtonsDesiredDivision = document.querySelectorAll('input[name="radio-group-desired-division"]');
const makrs_on_current_rank_selected = document.querySelector('.current-marks-select');
const makrs_on_current_rank = document.querySelectorAll('.current-marks');
const server_select_element = document.querySelector('.servers-select');

// Slice Function
function sliceArray(array, start, end) {
  return array.slice(start, end + 1);
}

// Initail Values
const initiallyCheckedIndexCurrent = Array.from(radioButtonsCurrent).findIndex(radio => radio.checked) + 1;
const initiallyCheckedIndexDesired = Array.from(radioButtonsDesired).findIndex(radio => radio.checked) + 1;

const initiallyCheckedIndexCurrentDivision = Array.from(radioButtonsCurrentDivision).findIndex(radio => radio.checked) + 1;
const initiallyCheckedIndexDesiredDivision = Array.from(radioButtonsDesiredDivision).findIndex(radio => radio.checked) + 1;
const initiallyCheckedIndexMark = makrs_on_current_rank_selected.value;

// Read Values From Json File
let divisionPrices = [0];
let marks_price = [[0, 0, 0, 0, 0, 0]];
Promise.all([
  new Promise(function (resolve, reject) {
    $.getJSON('/static/wildRift/data/divisions_data.json', function (data) {
      divisionPrices = divisionPrices.concat(...data);
      resolve();
    });
  }),
  new Promise(function (resolve, reject) {
    $.getJSON('/static/wildRift/data/marks_data.json', function (data) {
      marks_price = marks_price.concat(data.slice(0));
      resolve();
    });
  })
]).then(function () {
  // Array For Names 
  const divisionRanks = ['', 'iron', 'bronze', 'silver', 'gold', 'platinum', 'emerald', 'diamond', 'master'];

  const divisionNames = [0, 'IV', 'III', 'II', 'I']

  // Variable That I Use
  var current_rank = initiallyCheckedIndexCurrent;
  var desired_rank = initiallyCheckedIndexDesired;
  var current_division = initiallyCheckedIndexCurrentDivision;
  var desired_division = initiallyCheckedIndexDesiredDivision;
  var current_rank_name = divisionRanks[initiallyCheckedIndexCurrent];
  var desired_rank_name = divisionRanks[initiallyCheckedIndexDesired];
  var current_division_name = divisionNames[initiallyCheckedIndexCurrentDivision];
  var desired_division_name = divisionNames[initiallyCheckedIndexDesiredDivision];
  var number_of_mark = marks_price[current_rank][initiallyCheckedIndexMark];
  var mark = 0
  var selectedServer = server_select_element.value;

  // Look Here:- I Want Get The Current & Desired Element Not Index
  let currentElement = Array.from(radioButtonsCurrent).find(radio => radio.checked);
  let desiredElement = Array.from(radioButtonsDesired).find(radio => radio.checked);

  // Apply Extra Button
  function setupApplyButtonClickEvent(button, percentage) {
    Applybuttons[button].addEventListener('click', function () {
      updateTotalPercentage(percentage, !Applybuttons[button].classList.contains('cancelButton'), button);
      getResult();
      getPrices();
    });
  }

  // Setup click events for each button
  // for (const key in buttons) {
  //   setupButtonClickEvent(buttons[key], key);
  // }
  // setupApplyButtonClickEvent('duoBoosting', 0.65);
  // setupApplyButtonClickEvent('selectBooster', 0.05);
  // setupApplyButtonClickEvent('turboBoost', 0.20);
  // setupApplyButtonClickEvent('streaming', 0.15);

  // Read Marks
  $.getJSON('/static/wildRift/data/marks_data.json', function (data) {
    marks_price = marks_price.concat(data.slice(1));
    number_of_mark = marks_price[current_rank][initiallyCheckedIndexMark];
    getResult();
  });

  // if (extend_order) {
  //   let orderID = parseInt(extend_order, 10);
  //   document.getElementById('extendOrder').value = orderID; 

  //   // Set the checked state for each group of radio buttons using the specified order
  //   setRadioButtonStateWithDisable(radioButtonsCurrent, valuesToSet[0]-1);
  //   setRadioButtonStateWithDisable(radioButtonsCurrentDivision, valuesToSet[1]-1);
  //   setRadioButtonStateWithDisable(makrs_on_current_rank_selected, valuesToSet[2]);
  //   setRadioButtonState(radioButtonsDesired, valuesToSet[3]-1, true);
  //   setRadioButtonStateForDesiredDivision(radioButtonsDesiredDivision, valuesToSet[4]-1);
  //   current_rank = valuesToSet[0];
  //   current_division = valuesToSet[1];
  //   desired_rank = valuesToSet[3];
  //   desired_division = valuesToSet[4];
  //   var current_rank_name = divisionRanks[current_rank];
  //   var desired_rank_name = divisionRanks[desired_rank];
  //   var current_division_name = divisionNames[current_division];
  //   var desired_division_name = divisionNames[desired_division];

  //   let duoBoostingApply= document.getElementById('duoBoostingApplyButton')
  //   let turboBoostApply = document.getElementById('turboBoostApplyButton')
  //   let streamingApply = document.getElementById('streamingApplyButton')

  //   // Function to set checkbox state based on values
  //   function setCheckboxState(checkbox, value) {
  //     if (value === true){
  //       checkbox.click();
  //       console.log("hi")
  //     }
  //   }
  //   // Set the state of each checkbox based on the values list
  //   setCheckboxState(duoBoostingApply, valuesToSetAdditional[0]);
  //   setCheckboxState(autoSelectBooster, valuesToSetAdditional[1]);
  //   setCheckboxState(turboBoostApply, valuesToSetAdditional[2]);
  //   setCheckboxState(streamingApply, valuesToSetAdditional[3]);
  // }
    
  // if(extend_order) {
  //   function getResult() {
  //     const startt = ((valuesToSet[3] - 1) * 4) + valuesToSet[4];
  //     const endd = ((desired_rank - 1) * 4) + desired_division-1;
  //     const slicedArray = sliceArray(divisionPrices, startt, endd);
  //     const summ = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
  //     console.log(slicedArray)
  //     console.log(divisionPrices)

  //     let result_with_mark = summ

  //     if (summ !== 0) {
  //       result_with_mark = summ - number_of_mark;
  //     }

  //     // Apply extra charges to the result
  //     result_with_mark += result_with_mark * total_Percentage;
  //     result_with_mark = parseFloat(result_with_mark.toFixed(2)); 

  //     const pricee = document.querySelector('.price-data.division-boost');
  //     pricee.innerHTML = `
  //     <p class='fs-5 text-uppercase my-4'>Boosting <span class='fw-bold'>From ${current_rank_name} ${current_division_name} Marks ${valuesToSet[2]} to ${divisionRanks[valuesToSet[3]]} ${divisionNames[valuesToSet[4]] != 'master' ? divisionNames[valuesToSet[4]] : ''} </span></p>
  //     <p class='fs-5 text-uppercase my-4'>Extend <span class='fw-bold'>From ${divisionRanks[valuesToSet[3]]} ${divisionNames[valuesToSet[4]]} Marks ${mark} to ${desired_rank_name} ${desired_rank_name != 'master' ? desired_division_name : ''} </span></p>
  //     <span class='fs-5 text-uppercase fw-bold'>Extra Cost: $${result_with_mark}</span>
  //   `;

  //     // From Value
  //     $('input[name="current_rank"]').val(current_rank);
  //     $('input[name="current_division"]').val(current_division);
  //     $('input[name="marks"]').val(mark);
  //     $('input[name="desired_rank"]').val(desired_rank);
  //     $('input[name="desired_division"]').val(desired_division);
  //     $('input[name="price"]').val(result_with_mark);
  //   }
  // }
  // else{
    function getResult() {
      const startt = ((current_rank - 1) * 4) + current_division;
      const endd = 2;
      const slicedArray = sliceArray(divisionPrices, startt, endd);
      const summ = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

      let result_with_mark = summ

      if (summ !== 0) {
        result_with_mark = summ - number_of_mark;
      }

      // Apply extra charges to the result
      // result_with_mark += result_with_mark * total_Percentage;
      result_with_mark = parseFloat(result_with_mark.toFixed(2));
      
      // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
      $('#current-rank-selected-img').attr('src', $(currentElement).data('img'))
      $('#desired-rank-selected-img').attr('src', $(desiredElement).data('img'))

    //   const pricee = document.querySelector('.price-data.division-boost');
    //   pricee.innerHTML = `
    //   <p class='fs-5 text-uppercase my-4'>Boosting <span class='fw-bold'>From ${current_rank_name} ${current_division_name} Marks ${mark} to ${desired_rank_name} ${desired_rank_name != 'master' ? desired_division_name : ''} </span></p>
    //   <span class='fs-5 text-uppercase fw-bold'>Total Cost: $${result_with_mark}</span>
    // `;

      // From Value
      // $('input[name="current_rank"]').val(current_rank);
      // $('input[name="current_division"]').val(current_division);
      // $('input[name="marks"]').val(mark);
      // $('input[name="desired_rank"]').val(desired_rank);
      // $('input[name="desired_division"]').val(desired_division);
      // $('input[name="server"]').val(selectedServer);
      // $('input[name="price"]').val(result_with_mark);
      console.log(selectedServer)
    }
  // }

  // Get Result
  getResult();

  // Change Marks
  function setMarkNumber() {
    let number_of_marks = -1; // num of marks
    switch (current_rank) {
      case 1:
        number_of_marks = 2;
        break;
      case 2:
      case 3:
        number_of_marks = 3;
        break;
      case 4:
      case 5:
        number_of_marks = 4;
        break;
      case 6:
        number_of_marks = 5;
        break;
      case 7:
        number_of_marks = -1;
        break;
      default:
        number_of_marks = -1;
    }
    makrs_on_current_rank.forEach(function (element, index) {
      if (number_of_marks == -1) {
        $('.current-mark-container').css('visibility', 'hidden');
      }
      else {
        $('.current-mark-container').css('visibility', 'visible');
        if (index <= number_of_marks) {
          element.classList.remove('d-none');
        } else {
          element.classList.add('d-none');
        }
      }
    });

  }

  setMarkNumber();

  // Current Rank Change
  radioButtonsCurrent.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtonsCurrent).indexOf(radio);
      current_rank = selectedIndex + 1;
      current_rank_name = divisionRanks[current_rank];

      // Look Here:- When Current Rank Change Change Value So Image Changed 
      currentElement = Array.from(radioButtonsCurrent).find(radio => radio.checked);

      makrs_on_current_rank_selected.value = 0; // make 0 mark is check
      setMarkNumber();
      getResult();
    });
  });

  // Desired Rank Change
  radioButtonsDesired.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtonsDesired).indexOf(radio);
      desired_rank = selectedIndex + 1;
      desired_rank_name = divisionRanks[desired_rank]

      // Look Here:- When Desired Rank Change Change Value So Image Changed 
      desiredElement = Array.from(radioButtonsDesired).find(radio => radio.checked);

      const desired_division_to_hide = document.getElementById('desired-division');
      if (desired_rank == 8) {
        desired_division_to_hide.classList.add('d-none');
        let desired_division_IV = document.getElementById("desired-division0")
        desired_division_IV.checked = true;
      }
      else {
        desired_division_to_hide.classList.remove('d-none');
      }

      getResult();
    });
  });

  // Current Division Change
  radioButtonsCurrentDivision.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtonsCurrentDivision).indexOf(radio);
      current_division = selectedIndex + 1;
      current_division_name = divisionNames[current_division]
      getResult();
    });
  });

  // Desired Division Change
  radioButtonsDesiredDivision.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtonsDesiredDivision).indexOf(radio);
      desired_division = selectedIndex + 1;
      desired_division_name = divisionNames[desired_division]
      getResult()
    });
  });

  // Mark Changes
  makrs_on_current_rank_selected.addEventListener("change", function() {
    const selectedIndex = this.value;
    number_of_mark = marks_price[current_rank][selectedIndex];
    mark = selectedIndex
    getResult();
  });

  // Server Changes
  server_select_element.addEventListener("change", function() {
    selectedServer = this.value
    getResult();
  });
});
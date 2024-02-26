// --------- If Customer Come After Choose Booster or For Extend Order ---------
// Get Params
// Assume you have a reference to the HTML element
const orderContainer = document.getElementById('order-container');
const urlParams = new URLSearchParams(window.location.search);
const extend_order = urlParams.get('extend');
let discount_amount = 0

// Access the data attribute and convert it to a JavaScript variable
const orderValue = orderContainer.dataset.order;

const valuesAsList = orderValue.split(',')
const list1 = valuesAsList.slice(0, 5);
const list2 = valuesAsList.slice(5, 10);

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

// Additional Initial Percent
var total_Percentage = 0;

// ----------------------------- Division Boost ---------------------------------

// Buttons
const radioButtonsCurrent = document.querySelectorAll('input[name="radio-group-current"]');
const radioButtonsDesired = document.querySelectorAll('input[name="radio-group-desired"]');
const radioButtonsCurrentDivision = document.querySelectorAll('input[name="radio-group-current-division"]');
const radioButtonsDesiredDivision = document.querySelectorAll('input[name="radio-group-desired-division"]');
const makrs_on_current_rank_selected = document.querySelector('.current-marks-select');
const makrs_on_current_rank = document.querySelectorAll('.current-marks');
const server_select_element = document.querySelector('.servers-select');

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
const initiallyCheckedIndexCurrent = Array.from(radioButtonsCurrent).findIndex(radio => radio.checked) + 1;
const initiallyCheckedIndexDesired = Array.from(radioButtonsDesired).findIndex(radio => radio.checked) + 1;

const initiallyCheckedIndexCurrentDivision = Array.from(radioButtonsCurrentDivision).findIndex(radio => radio.checked) + 1;
const initiallyCheckedIndexDesiredDivision = Array.from(radioButtonsDesiredDivision).findIndex(radio => radio.checked) + 1;
const initiallyCheckedIndexMark = makrs_on_current_rank_selected.value;

// Read Values From Json File
let divisionPrices = [0];
let marks_price = [[0, 0, 0, 0, 0]];
Promise.all([
  new Promise(function (resolve, reject) {
    $.getJSON('/static/valorant/data/divisions_data.json', function (data) {
      divisionPrices = divisionPrices.concat(...data);
      resolve();
    });
  }),
  new Promise(function (resolve, reject) {
    $.getJSON('/static/valorant/data/marks_data.json', function (data) {
      marks_price = marks_price.concat(data.slice(0));
      resolve();
    });
  })
]).then(function () {
  // Array For Names 
  const divisionRanks = ['', 'iron', 'bronze', 'silver', 'gold', 'platinum', 'diamond', 'ascendant', 'immortal'];

  const divisionNames = [0, 'I', 'II', 'III']

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
  var mark = 0;
  var selectedServer = server_select_element.value;

  // Look Here:- I Want Get The Current & Desired Element Not Index
  let currentElement = Array.from(radioButtonsCurrent).find(radio => radio.checked);
  let desiredElement = Array.from(radioButtonsDesired).find(radio => radio.checked);

  // Extend
  if (extend_order) {
    let orderID = parseInt(extend_order, 10);
    document.getElementById('extendOrder').value = orderID; 

    // Set the checked state for each group of radio buttons using the specified order
    setRadioButtonStateWithDisable(radioButtonsCurrent, valuesToSet[0]-1);
    setRadioButtonStateWithDisable(radioButtonsCurrentDivision, valuesToSet[1]-1);
    setRadioButtonStateWithDisable(makrs_on_current_rank_checked, valuesToSet[2]);
    setRadioButtonState(radioButtonsDesired, valuesToSet[3]-1, true);
    setRadioButtonStateForDesiredDivision(radioButtonsDesiredDivision, valuesToSet[4]-1);
    current_rank = valuesToSet[0];
    current_division = valuesToSet[1];
    desired_rank = valuesToSet[3];
    desired_division = valuesToSet[4];
    var current_rank_name = divisionRanks[current_rank];
    var desired_rank_name = divisionRanks[desired_rank];
    var current_division_name = divisionNames[current_division];
    var desired_division_name = divisionNames[desired_division];

    // Checkbox
    let extraOptions = document.querySelectorAll('input[name="extra-checkbox"]');

    // Solo Or Duo Boosting Change
    if (valuesToSetAdditional[0]) {
      document.querySelector('input[name="switch-between-solo-duo"][value="duo"]').checked = true;
      $('input#duoBoosting').val(true)
      document.querySelector('input[name="switch-between-solo-duo"][value="duo"]').disabled = true;
      document.querySelector('input[name="switch-between-solo-duo"][value="solo"]').disabled = true;
    } else {
      document.querySelector('input[name="switch-between-solo-duo"][value="solo"]').checked = true;
      $('input#duoBoosting').val(false)
    }

    // Extra Buttons
    extraOptions.forEach(function (checkbox, index) {
      if (checkbox.value === "selectBooster" && valuesToSetAdditional[1]) {
        checkbox.checked = true
        $(`input#${checkbox.value}`).val(true)
        $(checkbox).prop('disabled', true)
      } else if (checkbox.value === "turboBoost" && valuesToSetAdditional[2]) {
        checkbox.checked = true
        $(`input#${checkbox.value}`).val(true)
        $(checkbox).prop('disabled', true)
      } else if (checkbox.value === "streaming" && valuesToSetAdditional[3]) {
        checkbox.checked = true
        $(`input#${checkbox.value}`).val(true)
        $(checkbox).prop('disabled', true)
      } else if (checkbox.value === "boosterChampions" && valuesToSetAdditional[4]) {
        checkbox.checked = true
        $(`input#${checkbox.value}`).val(true)
        $(checkbox).prop('disabled', true)
      } else {
        checkbox.checked = false
        $(`input#${checkbox.value}`).val(false)
      } 
    })

  }

  if(extend_order) {
    function getDivisionPrice() {
      const startRank = ((valuesToSet[3] - 1) * 3) + valuesToSet[4];
      const endRank = ((desired_rank - 1) * 3) + desired_division-1;
      const slicedArray = sliceArray(divisionPrices, startRank, endRank);
      const sum = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
      console.log(slicedArray)
      console.log(divisionPrices)

      let result_with_mark = sum

      if (sum !== 0) {
        result_with_mark = sum - number_of_mark;
      }

      // Apply extra charges to the result
      result_with_mark += result_with_mark * total_Percentage;
      // Apply promo code 
      result_with_mark -= result_with_mark * (discount_amount/100 )

      result_with_mark = parseFloat(result_with_mark.toFixed(2)); 

      let currentElement = Array.from(radioButtonsCurrent).find(radio => (radio.getAttribute('data-name')).toLowerCase() === (divisionRanks[valuesToSet[3]]).toLowerCase());

      // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
      $('.current-rank-selected-img').attr('src', $(currentElement).data('img'))
      $('.desired-rank-selected-img').attr('src', $(desiredElement).data('img'))

      $('.current-selected-info').html(`${divisionRanks[valuesToSet[3]]} ${divisionNames[valuesToSet[4]]} ${mark == 0 ? '0-20' : mark == 1 ? '21-40' : mark == 2 ? '41-60' : mark == 3 ? '61-80' : '81-100'} RR`);
      $('.desired-selected-info').html(`${desired_rank_name} ${desired_division_name}`)

      $('.total-price #price').text(`$${result_with_mark}`)

      // From Value
      $('input[name="current_rank"]').val(current_rank);
      $('input[name="current_division"]').val(current_division);
      $('input[name="marks"]').val(mark);
      $('input[name="desired_rank"]').val(desired_rank);
      $('input[name="desired_division"]').val(desired_division);
      $('input[name="server"]').val(selectedServer);
      $('input[name="price"]').val(result_with_mark);
    }
  } else {
    // Get Result Function
    function getDivisionPrice() {
      const startRank = ((current_rank - 1) * 3) + current_division;
      const endRank = ((desired_rank - 1) * 3) + desired_division - 1;
      const slicedArray = sliceArray(divisionPrices, startRank, endRank);
      const result = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
  
      let result_with_mark = result
  
      if (result !== 0) {
        result_with_mark = result - number_of_mark;
      }
  
      // Apply extra charges to the result
      result_with_mark += result_with_mark * total_Percentage;
      // Apply promo code 
      result_with_mark -= result_with_mark * (discount_amount/100 )

      result_with_mark = parseFloat(result_with_mark.toFixed(2)); 

      // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
      $('.current-rank-selected-img').attr('src', $(currentElement).data('img'))
      $('.desired-rank-selected-img').attr('src', $(desiredElement).data('img'))

      $('.current-selected-info').html(`${current_rank_name} ${current_division_name} ${mark == 0 ? '0-20' : mark == 1 ? '21-40' : mark == 2 ? '41-60' : mark == 3 ? '61-80' : '81-100'} RR`);
      $('.desired-selected-info').html(`${desired_rank_name} ${desired_division_name}`)

      $('.current').removeClass().addClass(`current ${current_rank_name}`)
      $('.desired').removeClass().addClass(`desired ${desired_rank_name}`)

      $('.total-price #price').text(`$${result_with_mark}`)
  
      // From Value
      if ($('.division-boost input[name="game_type"]').val() == 'D') {
        $('.division-boost input[name="current_rank"]').val(current_rank);
        $('.division-boost input[name="current_division"]').val(current_division);
        $('.division-boost input[name="marks"]').val(mark);
        $('.division-boost input[name="desired_rank"]').val(desired_rank);
        $('.division-boost input[name="desired_division"]').val(desired_division);
        $('input[name="server"]').val(selectedServer);
        $('.division-boost input[name="price"]').val(result_with_mark);
      }
    }
  }

  // Get Result 
  getDivisionPrice();

  // Current Rank Change
  radioButtonsCurrent.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtonsCurrent).indexOf(radio);
      current_rank = selectedIndex + 1;
      current_rank_name = divisionRanks[current_rank];

      // Look Here:- When Current Rank Change Change Value So Image Changed 
      currentElement = Array.from(radioButtonsCurrent).find(radio => radio.checked);

      makrs_on_current_rank_selected.value = 0; // make 0 mark is check
      getDivisionPrice();
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
      
      getDivisionPrice();
    });
  });

  // Current Division Change
  radioButtonsCurrentDivision.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtonsCurrentDivision).indexOf(radio);
      current_division = selectedIndex + 1;
      current_division_name = divisionNames[current_division]
      getDivisionPrice();
    });
  })

  // Desired Division Change
  radioButtonsDesiredDivision.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtonsDesiredDivision).indexOf(radio);
      desired_division = selectedIndex + 1;
      desired_division_name = divisionNames[desired_division]
      getDivisionPrice()
    });
  });

  // Mark Changes
  makrs_on_current_rank_selected.addEventListener("change", function() {
    const selectedIndex = this.value;
    number_of_mark = marks_price[current_rank][selectedIndex];
    mark = selectedIndex
    getDivisionPrice();
  });

  // Server Changes
  server_select_element.addEventListener("change", function() {
    selectedServer = this.value
    getResult();
  });

  // Extra Charges Part
  // Additional Initial Percent
  let percentege = {
    duoBoosting: 0.65,
    selectBooster: 0.10,
    turboBoost: 0.20,
    streaming: 0.15,
    boosterAgents: 0.0
  }

  // Checkbox
  let soloOrDuoBoosting = document.querySelectorAll('input[name="switch-between-solo-duo"]');
  let extraOptions = document.querySelectorAll('input[name="extra-checkbox"]');

  // Solo Or Duo Boosting Change
  soloOrDuoBoosting.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      if (this.value === "duo") {
        total_Percentage += percentege.duoBoosting;
        $('input#duoBoosting').val(true)
      } else {
        total_Percentage -= percentege.duoBoosting;
        $('input#duoBoosting').val(false)
      }

      getDivisionPrice()
    }) 
  })

  // Extra Buttons
  extraOptions.forEach(function (checkbox, index) {
    checkbox.addEventListener('change', function () {
      if (this.checked) {
        total_Percentage += percentege[this.value];
        $(`input#${this.value}`).val(true)
      } else {
        total_Percentage -= percentege[this.value];
        $(`input#${this.value}`).val(false)
      }
    
      getDivisionPrice()
    })
  });
  
 
  const form = document.querySelector('.discount form');

  form.addEventListener('submit', function(event) {
    event.preventDefault();

    const discountInput = document.querySelector('input[name="discount"]');
    const discountCode = discountInput.value.trim();
    const promoDetails = $('#promo-details h6');
    $('input[id="promo_send"]').val(discountCode);

    if (discountCode) {
      const csrfToken = getCookie('csrftoken');
      $.ajax({
        url: '/accounts/promo-codes/',
        type: 'POST',
        headers: {
          'X-CSRFToken': csrfToken
        },
        contentType: 'application/json',
        data: JSON.stringify({ code: discountCode }),
        success: function(data) {
          promoDetails.css('visibility', 'visible');
          promoDetails.text(data.description);
          promoDetails.css('color', 'green');
          discount_amount = data.discount_amount;
          getDivisionPrice();
        },
        error: function(xhr, textStatus, errorThrown) {
          promoDetails.css('visibility', 'visible');
          promoDetails.text(xhr.responseJSON.error);
          promoDetails.css('color', 'red');
          discount_amount = 0;
          getDivisionPrice();
        }
      });
        
    } else {
      $('input[id="promo_send"]').val('null');
      promoDetails.css('visibility', 'visible');
      promoDetails.text('Please enter a discount code');
      promoDetails.css('color', 'red');
      discount_amount = 0;
      getDivisionPrice();
    }
  });

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Check if the cookie name matches the CSRF cookie name
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
});

// ----------------------------- Placments Boost ---------------------------------
const radioButtonsRank = $('input[name="radio-group-ranks"]');
const sliderEl = $("#game-count");
const sliderValue = $(".value");
const gameCounterInitial = Number(sliderEl.val())
const initiallyCheckedIndexRank = $('input[name="radio-group-ranks"]').index($('input[name="radio-group-ranks"]:checked'));
const initiallyCheckedRank = $('input[name="radio-group-ranks"]').eq(initiallyCheckedIndexRank);
const initiallyCheckedIndexRankPrice = initiallyCheckedRank.data('price');

let last_rank = initiallyCheckedIndexRank
let rank_price = initiallyCheckedIndexRankPrice
let gameCounter = gameCounterInitial


const getPlacementPrice = () => {
  let price = (rank_price * gameCounter);
  price = parseFloat(price + (price * total_Percentage)).toFixed(2)
  const pricee = $('.price-data.placements-boost').eq(0);
  pricee.html(`
  <p class='fs-5 text-uppercase my-4'>Boosting of <span class='fw-bold'>${gameCounter} Placement Games</span></p>
  <h4>$${price}</h4>
  `);

  if ($('.placements-boost input[name="game_type"]').val() == 'P') {
    $('.placements-boost input[name="last_rank"]').val(last_rank);
    $('.placements-boost input[name="number_of_match"]').val(gameCounter);
    $('.placements-boost input[name="price"]').val(price);
  }
}
getPlacementPrice()

radioButtonsRank.each(function (index, radio) {
  $(radio).on('change', function () {
    const selectedIndex = radioButtonsRank.index(radio);
    last_rank = selectedIndex;
    rank_price = $(radio).data('price');
    getPlacementPrice()
  });
});


sliderEl.on("input", function (event) {
gameCounter = Number(event.target.value);

sliderValue.text(gameCounter);

const progress = (gameCounter / sliderEl.prop("max")) * 100;

sliderEl.css("background", `linear-gradient(to right, var(--main-color) ${progress}%, #ccc ${progress}%)`);

sliderEl.css("--thumb-rotate", `${(gameCounter / 100) * 2160}deg`);

getPlacementPrice()
});
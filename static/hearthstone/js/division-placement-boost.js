// Array For Names 
const ranksNames = ['unrank', 'bronze', 'silver', 'gold', 'platinum', 'diamond', 'legend'];

const divisionNames = [0,'X','IX','VIII','VII','VI','V','IV','III','II','I']  

// ----------------------------- Division Boost ---------------------------------

// Read Values From Json File
let divisionPrices = [0];
let marks_price = [[0, 0, 0, 0]];
Promise.all([
  new Promise(function (resolve, reject) {
    $.getJSON('/hearthstone/divisions-data/', function (data) {
      divisionPrices = divisionPrices.concat(...data);
      resolve();
    });
  }),
  new Promise(function (resolve, reject) {
    $.getJSON('/hearthstone/marks-data/', function (data) {
      marks_price = marks_price.concat(data.slice(0));
      resolve();
    });
  })
]).then(function () {

  // Extend
  if (extend_order) {
    let orderID = parseInt(extend_order, 10);
    document.getElementById('extendOrder').value = orderID; 

    // Set the checked state for each group of radio buttons using the specified order
    setRadioButtonStateWithDisable(radioButtonsCurrent, valuesToSet[0]-1);
    setRadioButtonStateWithDisable(radioButtonsCurrentDivision, valuesToSet[1]-1);
    setRadioButtonState(radioButtonsDesired, valuesToSet[3]-1, true);
    setRadioButtonStateForDesiredDivision(radioButtonsDesiredDivision, valuesToSet[4]-1);
    makrs_on_current_rank_selected.disabled = true
    division_server_select_element.disabled = true

    // Solo Or Duo Boosting Change
    if (valuesToSetAdditional[0]) {
      duoBoosting.checked = true;
      total_Percentage += percentege.duoBoosting;
      $('input#duoBoosting').val(true)
    } else {
      soloBoosting.checked = true;
      $('input#duoBoosting').val(false)
    }
    duoBoosting.disabled = true;
    soloBoosting.disabled = true;


    // Extra Buttons
    extraOptions.forEach(function (checkbox, index) {
      if (checkbox.value === "selectBooster" && valuesToSetAdditional[1]) {
        total_Percentage += percentege[checkbox.value];
        checkbox.checked = true
        $(`input#${checkbox.value}`).val(true)
        
      } else if (checkbox.value === "turboBoost" && valuesToSetAdditional[2]) {
        total_Percentage += percentege[checkbox.value];
        checkbox.checked = true
        $(`input#${checkbox.value}`).val(true)

      } else if (checkbox.value === "streaming" && valuesToSetAdditional[3]) {
        total_Percentage += percentege[checkbox.value];
        checkbox.checked = true
        $(`input#${checkbox.value}`).val(true)

      } else if (checkbox.value === "boosterChampions" && valuesToSetAdditional[4]) {
        total_Percentage += percentege[checkbox.value];
        checkbox.checked = true
        $(`input#${checkbox.value}`).val(true)

      } else {
        checkbox.checked = false
        $(`input#${checkbox.value}`).val(false)
      }
      // Disable Extra
      $(checkbox).prop('disabled', true)
    })
 
    function getResult() {
      const desired_rank = getSelectedValueForRadio(radioButtonsDesired)
      const desired_division = getSelectedValueForRadio(radioButtonsDesiredDivision)

      const current_rank = valuesToSet[0];
      const current_division = valuesToSet[1];
      const mark_index = valuesToSet[2];
      
      const current_rank_name = ranksNames[current_rank];
      const desired_rank_name = ranksNames[desired_rank];
      const desired_division_name = divisionNames[desired_division];

      const selectedDivsionServer = server;

      makrs_on_current_rank_selected.value = mark_index
      division_server_select_element.value = server

      const startRank = ((valuesToSet[3] - 1) * 10) + valuesToSet[4];
      const endRank = ((desired_rank - 1) * 10) + desired_division-1;
      const slicedArray = sliceArray(divisionPrices, startRank, endRank);
      const sum = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

      let result_with_mark = sum

      // Apply extra charges to the result
      result_with_mark += result_with_mark * total_Percentage;
      // Apply promo code 
      result_with_mark -= result_with_mark * (discountAmount/100)

      result_with_mark = parseFloat(result_with_mark.toFixed(2));

      // To Make Current Image Be Old Desired
      const oldDeiredElement = Array.from(radioButtonsCurrent).find(radio => (radio.getAttribute('data-name')).toLowerCase() === (ranksNames[valuesToSet[3]]).toLowerCase());
  
      const currentElement = getSelectedElement(radioButtonsCurrent)
      const desiredElement = getSelectedElement(radioButtonsDesired)

      // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
      $('.current-rank-selected-img:not(.checkout-img)').attr('src', $(currentElement).data('img'))
      $('.current-rank-selected-img.checkout-img').attr('src', $(oldDeiredElement).data('img'))

      $('.desired-rank-selected-img').attr('src', $(desiredElement).data('img'))

      $('.current-selected-info').html(`${ranksNames[valuesToSet[3]]} ${divisionNames[valuesToSet[4]]}`);
      $('.desired-selected-info').html(`${desired_rank_name} ${desired_division_name}`)

      $('.current').removeClass().addClass(`current ${current_rank_name}`)
      $('.desired').removeClass().addClass(`desired ${desired_rank_name}`)

      $('.total-price #division-boost-price').text(`$${result_with_mark}`)

      // From Value
      $('input[name="current_rank"]').val(current_rank);
      $('input[name="current_division"]').val(current_division);
      $('input[name="marks"]').val(mark_index);
      $('input[name="desired_rank"]').val(desired_rank);
      $('input[name="desired_division"]').val(desired_division);
      $('input[name="server"]').val(selectedDivsionServer);
      $('input[name="division-boost-price"]').val(result_with_mark);

      // SET PROMO CODE IN FORM
      $('input[name="promo_code"]').val(extendPromoCode);
    }
  } else {
    // Get Result Function
    function getResult() {
      const current_rank = getSelectedValueForRadio(radioButtonsCurrent);
      const desired_rank = getSelectedValueForRadio(radioButtonsDesired)
      const current_division = getSelectedValueForRadio(radioButtonsCurrentDivision)
      const desired_division = getSelectedValueForRadio(radioButtonsDesiredDivision)
      const current_rank_name = ranksNames[current_rank];
      const desired_rank_name = ranksNames[desired_rank];
      const current_division_name = divisionNames[current_division];
      const desired_division_name = divisionNames[desired_division];

      let mark_index = -1
      let number_of_mark = 0
      try {
        mark_index = getSelectedValueForDropList(makrs_on_current_rank_selected)
        number_of_mark = marks_price[current_rank][mark_index];
      } catch (error) {
        console.log("ERROR: ", error)
      }

      const selectedDivsionServer = division_server_select_element.value;

      const startRank = ((current_rank - 1) * 10) + current_division;
      const endRank = ((desired_rank - 1) * 10) + desired_division - 1;
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
      const currentElement = getSelectedElement(radioButtonsCurrent)
      const desiredElement = getSelectedElement(radioButtonsDesired)

      $('.current-rank-selected-img').attr('src', $(currentElement).data('img'))
      $('.desired-rank-selected-img').attr('src', $(desiredElement).data('img'))

      $('.current-selected-info').html(`${current_rank_name} ${current_division_name} ${mark_index == 0 ? '0' : 4 - mark_index} Stars`);
      $('.desired-selected-info').html(`${desired_rank_name} ${desired_division_name}`)

      $('.current').removeClass().addClass(`current ${current_rank_name}`)
      $('.desired').removeClass().addClass(`desired ${desired_rank_name}`)

      $('.total-price #division-boost-price').text(`$${result_with_mark}`)

      // From Value
      $('#division-boost-form input[name="current_rank"]').val(current_rank);
      $('#division-boost-form input[name="current_division"]').val(current_division);
      $('#division-boost-form input[name="marks"]').val(mark_index);
      $('#division-boost-form input[name="desired_rank"]').val(desired_rank);
      $('#division-boost-form input[name="desired_division"]').val(desired_division);
      $('#division-boost-form input[name="server"]').val(selectedDivsionServer);
      $('#division-boost-form input[name="price"]').val(result_with_mark);
    }
  }

  // Get Result 
  getResult();

  // get element by class name battlegrounds-servers-select and get value from it selected option
  
  selectedBattlegroundsArenaServer = function() {
    const battleServer = $('.battlegrounds-servers-select').find(":selected").val();
    $('#battlegrounds-boost-form input[name="server"]').val(battleServer);
    return battleServer
  }
  $('.battlegrounds-servers-select').on('change', function() {
    selectedBattlegroundsArenaServer()
  })

  selectedBattlegroundsDivsionServer = function() {
    const battleServer = $('.division-servers-select').find(":selected").val();
    $('#division-boost-form input[name="server"]').val(battleServer);
    return battleServer
  }
  $('.division-servers-select').on('change', function() {
    selectedBattlegroundsDivsionServer()
  })



  let currentBattlegroundsValue = 0
  let desiredBattlegroundsValue = 0



  const currentRangeInput = document.getElementById('current-battlegrounds-range');
  const currentRangeDisplay = document.querySelector('.current-battlegrounds-rp h1');

  const desiredRangeInput = document.getElementById('desired-battlegrounds-range');
  const desiredRangeDisplay = document.querySelector('.desired-battlegrounds-rp h1');

  // Event listener for current range input
  currentRangeInput.addEventListener('input', (event) => {
      updateCurrentRangeValue(event.target.value);
  });

  // Event listener for desired range input
  desiredRangeInput.addEventListener('input', (event) => {
      updateDesiredRangeValue(event.target.value);
  });




MIN_DESIRED_VALUE = 20
price_of_3vs3 = 5

function getBattlegroundsPrice() {
  // Price
  let price = (desiredBattlegroundsValue - currentBattlegroundsValue) * (price_of_3vs3 / MIN_DESIRED_VALUE);

  // Apply extra charges to the result
  price += price * total_Percentage;

  // Apply promo code 
  price -= price * (discount_amount/100 )

  price = parseFloat(price.toFixed(2)); 

  // Current
  $('#current-3vs3 .current-3vs3-rp').html(currentBattlegroundsValue);
  $('.current').removeClass().addClass(`current gold`);
  $('.current-selected-mmr').html(`${currentBattlegroundsValue} MMR`)

  // Desired
  $('#desired-3vs3 .desired-3vs3-rp').html(desiredBattlegroundsValue);
  $('.desired').removeClass().addClass(`desired gold`);
  $('.desired-selected-mmr').html(`${desiredBattlegroundsValue} MMR`)

  // Price
  $('#battlegrounds-boost-price').html(`$${price}`)

  // Form
  $('#battlegrounds-boost-form input[name="current_mmr"]').val(currentBattlegroundsValue);
  $('#battlegrounds-boost-form input[name="desired_mmr"]').val(desiredBattlegroundsValue);
  $('#battlegrounds-boost-form input[name="server"]').val(selectedBattlegroundsArenaServer());
  $('#battlegrounds-boost-form input[name="price"]').val(price);
}






  // Update current range value display
  const updateCurrentRangeValue = (value) => {
      currentRangeDisplay.textContent = value;
      currentBattlegroundsValue = value

      $('#current-battlegrounds .current-battlegrounds-rp').html(currentBattlegroundsValue);
      getBattlegroundsPrice();
  };

  // Update desired range value display
  const updateDesiredRangeValue = (value) => {
      desiredRangeDisplay.textContent = value;
      desiredBattlegroundsValue = value

      $('#desired-battlegrounds .desired-battlegrounds-rp').html(desiredBattlegroundsValue);
      getBattlegroundsPrice();
  };



    // Initialize display with default values
    updateCurrentRangeValue(currentRangeInput.value);
    updateDesiredRangeValue(desiredRangeInput.value);






  // Current Rank Change
  radioButtonsCurrent.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      makrs_on_current_rank_selected.value = 0;
      getResult();
    });
  });

  // Desired Rank Change
  radioButtonsDesired.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtonsDesired).indexOf(radio);
      desired_rank = selectedIndex + 1;

      const desired_division_to_hide = document.getElementById('desired-division');
      if (desired_rank == 6) {
        desired_division_to_hide.style.visibility = 'hidden';
        let desired_division_I = document.getElementById("desired-division0")
        desired_division_I.checked = true;
      }
      else {
        desired_division_to_hide.style.visibility = 'visible';
      }
      getResult();
    });
  });

  // Current Division Change
  radioButtonsCurrentDivision.forEach(function (radio, index) {
    radio.addEventListener('change', getResult);
  });

  // Desired Division Change
  radioButtonsDesiredDivision.forEach(function (radio, index) {
    radio.addEventListener('change', getResult);
  });

  // Mark Changes
  makrs_on_current_rank_selected.addEventListener("change", getResult);

  // Server Changes
  // division_server_select_element.addEventListener("change", getResult);

  // ----------------------------- Others ---------------------------------

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

      getResult()
      getBattlegroundsPrice()
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
    
      getResult()
      getBattlegroundsPrice()
    })
  });
 
  promo_form.addEventListener('submit', async function(event) {
    event.preventDefault();
    if(!extend_order) {
      discount_amount = await fetch_promo(); 

      getResult()
      getBattlegroundsPrice()

    }
  });

});
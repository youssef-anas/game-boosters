// Array For Names 
const ranksNames = ['unrank', 'iron', 'bronze', 'silver', 'gold', 'platinum', 'emerald', 'diamond', 'master'];

const divisionNames = [0, 'IV', 'III', 'II', 'I']

// Function That Change UI Of Range
function changeUI(achivedValue, element, steps, miuns = 0) {
  const progress = ((achivedValue - miuns) / (element.prop("max") - miuns) ) * 100;

  element.css({
    "background": `linear-gradient(to right, #F36E3F ${progress}%, #251D16 ${progress}%)`
  });
  
  steps.each((step, index) => {
    
    if (parseInt(index.innerText) < achivedValue) {
      index.classList.add('selected')
    } else {
      index.classList.remove('selected');
    }
  });
}

// ----------------------------- Division Boost ---------------------------------

// Read Values From Json File
let divisionPrices = [0];
let marks_price = [[0, 0, 0, 0, 0, 0]];
Promise.all([
  new Promise(function (resolve, reject) {
    $.getJSON('/lol/divisions-data/', function (data) {
      divisionPrices = divisionPrices.concat(...data);
      resolve();
    });
  }),
  new Promise(function (resolve, reject) {
    $.getJSON('/lol/marks-data/', function (data) {
      marks_price = marks_price.concat(data.slice(0));
      resolve();
    });
  })
]).then(function () {

  // Extend
  if (extend_order) {
    $('input[type="radio"]#placements-boost').prop('disabled', true)

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

    function getDivisionPrice() {
      const desired_rank = getSelectedValueForRadio(radioButtonsDesired)
      const desired_division = getSelectedValueForRadio(radioButtonsDesiredDivision)

      const current_rank = valuesToSet[0];
      const current_division = valuesToSet[1];
      const mark_index = valuesToSet[2];
      
      const current_rank_name = ranksNames[current_rank];
      const desired_rank_name = ranksNames[desired_rank];
      const desired_division_name = divisionNames[desired_division];

      makrs_on_current_rank_selected.value = mark_index
      division_server_select_element.value = server

      const startRank = ((valuesToSet[3] - 1) * 4) + valuesToSet[4];
      const endRank = ((desired_rank - 1) * 4) + desired_division-1;
      const slicedArray = sliceArray(divisionPrices, startRank, endRank);
      const sum = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

      let result_with_mark = sum

      // Apply extra charges to the result
      result_with_mark += result_with_mark * total_Percentage;
      // Apply promo code 
      result_with_mark = setPromoAmount(result_with_mark, discountAmount)

      result_with_mark = parseFloat(result_with_mark.toFixed(2)); 
      
      // To Make Current Image Be Old Desired
      const oldDeiredElement = Array.from(radioButtonsCurrent).find(radio => (radio.getAttribute('data-name')).toLowerCase() === (ranksNames[valuesToSet[3]]).toLowerCase());
      const currentElement = getSelectedElement(radioButtonsCurrent)
      const desiredElement = getSelectedElement(radioButtonsDesired)

      // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
      $('.division-boost .current-rank-selected-img:not(.checkout-img)').attr('src', $(currentElement).data('img'))
      $('.division-boost .current-rank-selected-img.checkout-img').attr('src', $(oldDeiredElement).data('img'))
       
      $('.division-boost .desired-rank-selected-img').attr('src', $(desiredElement).data('img'))

      $('.division-boost .current-selected-info').html(`${ranksNames[valuesToSet[3]]} ${divisionNames[valuesToSet[4]]}`);
      $('.division-boost .desired-selected-info').html(`${desired_rank_name} ${desired_rank != 8 ? desired_division_name : ''}`)

      $('.current').removeClass().addClass(`current ${current_rank_name}`)
      $('.desired').removeClass().addClass(`desired ${desired_rank_name}`)

      $('.total-price #division-boost-price').text(`$${result_with_mark}`)

      // From Value
      $('.division-boost input[name="current_rank"]').val(current_rank);
      $('.division-boost input[name="current_division"]').val(current_division);
      $('.division-boost input[name="marks"]').val(mark_index);
      $('.division-boost input[name="desired_rank"]').val(desired_rank);
      $('.division-boost input[name="desired_division"]').val(desired_division);
      $('.division-boost input[name="server"]').val(server);
      $('.division-boost input[name="price"]').val(result_with_mark);

      // SET PROMO CODE IN FORM
      $('.division-boost input[name="promo_code"]').val(extendPromoCode);
    }
  } else {
    // Get Result Function
    function getDivisionPrice() {
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
        
      }
      const selectedDivsionServer = division_server_select_element.value;

      const startRank = ((current_rank - 1) * 4) + current_division;
      const endRank = ((desired_rank - 1) * 4) + desired_division - 1;
      const slicedArray = sliceArray(divisionPrices, startRank, endRank);
      const result = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
  
      let result_with_mark = result
  
      if (result !== 0) {
        result_with_mark = result - number_of_mark;
      }
  
      // Apply extra charges to the result
      result_with_mark += result_with_mark * total_Percentage;
  
      // Apply promo code 
      result_with_mark = setPromoAmount(result_with_mark, discount_amount)

      result_with_mark = parseFloat(result_with_mark.toFixed(2));

      // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
      const currentElement = getSelectedElement(radioButtonsCurrent)
      const desiredElement = getSelectedElement(radioButtonsDesired)

      $('.division-boost .current-rank-selected-img').attr('src', $(currentElement).data('img'))
      $('.division-boost .desired-rank-selected-img').attr('src', $(desiredElement).data('img'))

      $('.division-boost .current-selected-info').html(`${current_rank_name} ${current_division_name} ${mark_index == 0 ? '0-20' : mark_index == 1 ? '21-40' : mark_index == 2 ? '41-60' : mark_index == 3 ? '61-80' : mark_index == 3 ? '81-99' : 'SERIES'} LP`);
      $('.division-boost .desired-selected-info').html(`${desired_rank_name} ${desired_rank != 8 ? desired_division_name : ''}`)
  
      $('.current').removeClass().addClass(`current ${current_rank_name}`)
      $('.desired').removeClass().addClass(`desired ${desired_rank_name}`)

      $('.total-price #division-boost-price').text(`$${result_with_mark}`)

      // From Value
      if ($('.division-boost input[name="game_type"]').val() == 'D') {
        $('.division-boost input[name="current_rank"]').val(current_rank);
        $('.division-boost input[name="current_division"]').val(current_division);
        $('.division-boost input[name="marks"]').val(mark_index);
        $('.division-boost input[name="desired_rank"]').val(desired_rank);
        $('.division-boost input[name="desired_division"]').val(desired_division);
        if (desired_rank == 8){
          $('input[name=desired_division]').val(1)
        }
        $('.division-boost input[name="server"]').val(selectedDivsionServer);
        $('.division-boost input[name="price"]').val(result_with_mark);
      }

    }
  }

  // Get Result 
  getDivisionPrice();

  // Current Rank Change
  radioButtonsCurrent.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      makrs_on_current_rank_selected.value = 0; // make 0 mark is check
      getDivisionPrice();
    });
  });

  // Desired Rank Change
  radioButtonsDesired.forEach(function (radio, index) {
    radio.addEventListener('change', function () {

      const selectedIndex = Array.from(radioButtonsDesired).indexOf(radio);
      desired_rank = selectedIndex + 1;
    
      const desired_division_to_hide = document.getElementById('desired-division');
      if (desired_rank == 8) {
        desired_division_to_hide.style.visibility = "hidden";
        let desired_division_I = document.getElementById("desired-division0")
        desired_division_I.checked = true;
        desired_division_I.setAttribute("checked", "checked");
      }
      else {
        desired_division_to_hide.style.visibility = "visible";
      }
      getDivisionPrice();
    });
  });

  // Current Division Change
  radioButtonsCurrentDivision.forEach(function (radio, index) {
    radio.addEventListener('change', getDivisionPrice);
  });

   // Desired Division Change
   radioButtonsDesiredDivision.forEach(function (radio, index) {
    radio.addEventListener('change', getDivisionPrice);
  });

  // Mark Changes
  makrs_on_current_rank_selected.addEventListener("change", getDivisionPrice);
  // Server Changes
  division_server_select_element.addEventListener("change", getDivisionPrice);

  // ----------------------------- Placments Boost ---------------------------------
  // Pervious Varible
  const placementsRanks = $('input[name="placement-ranks"]');

  // Game Count
  const gameCount = $("#game-count");
  const gameCountSteps = $('.step-indicator .step');

  // Server
  const placement_server_select_element = $('.placement-servers-select');

  const getPlacementPrice = () => {
    const checkedIndexRank = placementsRanks.index($('input[name="placement-ranks"]:checked'));
    const perviousElementRank = placementsRanks.eq(checkedIndexRank);

    const perviousRank = checkedIndexRank;
  
    const perviousRankName = ranksNames[perviousRank]
    
    const gameCounterValue = Number(gameCount.val())
    
    const rankPrice = perviousElementRank.data('price');

    const selectedPlacementServer = placement_server_select_element.val()

    let price = (rankPrice * gameCounterValue);

    // Apply extra charges to the result
    price = price + (price * total_Percentage)

    // Apply promo code 
    price = setPromoAmount(price, discount_amount)

    price = parseFloat(price.toFixed(2))
  
    // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
    $('.placements-boost .pervious-rank-selected-img').attr('src', $(perviousElementRank).data('img'))
    $('.num-of-match').text(gameCounterValue);

    $('.placements-boost .pervious-selected-info').html(`${perviousRankName}`)
    $('.placements-boost .game-count-selected-info').html(`${gameCounterValue} Matches`)

    $('.pervious').removeClass().addClass(`pervious ${perviousRankName}`);
    $('.matches-amount').removeClass().addClass(`matches-amount ${perviousRankName}`);

    $('.total-price #placements-boost-price').text(`$${price}`)

    changeUI(gameCounterValue, gameCount, gameCountSteps, 1)

    if ($('.placements-boost input[name="game_type"]').val() == 'P') {
      $('.placements-boost input[name="last_rank"]').val(perviousRank);
      $('.placements-boost input[name="number_of_match"]').val(gameCounterValue);
      $('.placements-boost input[name="server"]').val(selectedPlacementServer);
      $('.placements-boost input[name="price"]').val(price);
    }
  }

  getPlacementPrice()

  placementsRanks.each(function (index, radio) {
    $(radio).on('change', getPlacementPrice);
  });
  
  gameCount.on("input", getPlacementPrice);

  // Server Changes
  placement_server_select_element.on("change", getPlacementPrice);

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

      getDivisionPrice()
      getPlacementPrice()
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
      getPlacementPrice()
    })
  });
 
  promo_form.addEventListener('submit', async function(event) {
    event.preventDefault();
    if(!extend_order) {
      discount_amount = await fetch_promo(); 
      getDivisionPrice(); 
      getPlacementPrice();
    }
  });
});
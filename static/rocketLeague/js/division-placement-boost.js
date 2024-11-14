// Array For Names 
const ranksNames = ['unrank', 'bronze', 'silver', 'gold', 'platinum', 'diamond', 'champion', 'grand champion', 'supersonic legend']

const divisionNames = [0, 'I', 'II', 'III']

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
Promise.all([
  new Promise(function (resolve, reject) {
    $.getJSON('/rocketLeague/divisions-data/', function (data) {
      divisionPrices = divisionPrices.concat(...data);
      resolve();
    });
  })
]).then(function () {

  const ranked_type_selected = document.querySelector('.queue-type-select');

  // Extend
  if (extend_order) {
    $('input[type="radio"]#placements-boost').prop('disabled', true)
    $('input[type="radio"]#seasonal-reward').prop('disabled', true)
    $('input[type="radio"]#tournament-boost').prop('disabled', true)

    let orderID = parseInt(extend_order, 10);
    document.getElementById('extendOrder').value = orderID;

    // Set the checked state for each group of radio buttons using the specified order
    setRadioButtonStateWithDisable(radioButtonsCurrent, valuesToSet[0]-1);
    setRadioButtonStateWithDisable(radioButtonsCurrentDivision, valuesToSet[1]-1);
    setRadioButtonState(radioButtonsDesired, valuesToSet[3]-1, true);
    setRadioButtonStateForDesiredDivision(radioButtonsDesiredDivision, valuesToSet[4]-1);
    ranked_type_selected.disabled = true
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
      const ranked_type = valuesToSet[2];
      
      const current_rank_name = ranksNames[current_rank];
      const desired_rank_name = ranksNames[desired_rank];
      const desired_division_name = divisionNames[desired_division];

      const selectedDivsionServer = server;

      ranked_type_selected.value = ranked_type
      division_server_select_element.value = server

      const startRank = ((valuesToSet[3] - 1) * 3) + valuesToSet[4];
      const endRank = ((desired_rank - 1) * 3) + desired_division-1;
      const slicedArray = sliceArray(divisionPrices, startRank, endRank);
      const sum = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

      let result = sum

      // Apply extra charges to the result
      result += result * total_Percentage;

      // Apply promo code 
      result = setPromoAmount(result, discountAmount)

      result = parseFloat(result.toFixed(2)); 

      // To Make Current Image Be Old Desired
      const oldDeiredElement = Array.from(radioButtonsCurrent).find(radio => (radio.getAttribute('data-name')).toLowerCase() === (ranksNames[valuesToSet[3]]).toLowerCase());
      const currentElement = getSelectedElement(radioButtonsCurrent)
      const desiredElement = getSelectedElement(radioButtonsDesired)

      // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
      $('.division-boost .current-rank-selected-img:not(.checkout-img)').attr('src', $(currentElement).data('img'))
      $('.division-boost .current-rank-selected-img.checkout-img').attr('src', $(oldDeiredElement).data('img'))

      $('.division-boost .desired-rank-selected-img').attr('src', $(desiredElement).data('img'))

      $('.division-boost .current-selected-info').html(`${ranksNames[valuesToSet[3]]} ${divisionNames[valuesToSet[4]]}`);
      $('.division-boost .desired-selected-info').html(`${desired_rank_name} ${desired_division_name}`)
     
      $('.current').removeClass().addClass(`current ${current_rank_name.replace(/\s+/g, '-')}`)
      $('.desired').removeClass().addClass(`desired ${desired_rank_name.replace(/\s+/g, '-')}`)

      $('.total-price #division-boost-price').text(`$${result}`)

      // From Value
      $('.division-boost input[name="current_rank"]').val(current_rank);
      $('.division-boost input[name="current_division"]').val(current_division);
      $('.division-boost input[name="ranked_type"]').val(ranked_type);
      $('.division-boost input[name="desired_rank"]').val(desired_rank);
      $('.division-boost input[name="desired_division"]').val(desired_division);
      $('.division-boost input[name="server"]').val(selectedDivsionServer);
      $('.division-boost input[name="price"]').val(result);

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

      const ranked_type = ranked_type_selected.value

      const selectedDivsionServer = division_server_select_element.value;

      const startRank = ((current_rank - 1) * 3) + current_division;
      const endRank = ((desired_rank - 1) * 3) + desired_division - 1;
      const slicedArray = sliceArray(divisionPrices, startRank, endRank);
      const sum = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
  
      let result = sum
  
      // Apply extra charges to the result
      result += result * total_Percentage;
      // Apply promo code 
      result = setPromoAmount(result, discount_amount)

      result = parseFloat(result.toFixed(2)); 

      // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
      const currentElement = getSelectedElement(radioButtonsCurrent)
      const desiredElement = getSelectedElement(radioButtonsDesired)

      $('.division-boost .current-rank-selected-img').attr('src', $(currentElement).data('img'))
      $('.division-boost .desired-rank-selected-img').attr('src', $(desiredElement).data('img'))

      $('.division-boost .current-selected-info').html(`${current_rank_name} ${current_division_name}`);
      $('.division-boost .desired-selected-info').html(`${desired_rank_name} ${desired_division_name}`)

      $('.current').removeClass().addClass(`current ${current_rank_name.replace(/\s+/g, '-')}`)
      $('.desired').removeClass().addClass(`desired ${desired_rank_name.replace(/\s+/g, '-')}`)

      $('.total-price #division-boost-price').text(`$${result}`)
  
      // From Value
      if ($('.division-boost input[name="game_type"]').val() == 'D') {
        $('.division-boost input[name="current_rank"]').val(current_rank);
        $('.division-boost input[name="current_division"]').val(current_division);
        $('.division-boost input[name="ranked_type"]').val(ranked_type);
        $('.division-boost input[name="desired_rank"]').val(desired_rank);
        $('.division-boost input[name="desired_division"]').val(desired_division);
        $('.division-boost input[name="server"]').val(selectedDivsionServer);
        $('.division-boost input[name="price"]').val(result);
      }
    }
  }

  // Get Result 
  getDivisionPrice();

  // Current Rank Change
  radioButtonsCurrent.forEach(function (radio, index) {
    radio.addEventListener('change', getDivisionPrice)
  });

  // Desired Rank Change
  radioButtonsDesired.forEach(function (radio, index) {
    radio.addEventListener('change', getDivisionPrice);
  });

  // Current Division Change
  radioButtonsCurrentDivision.forEach(function (radio, index) {
    radio.addEventListener('change', getDivisionPrice);
  })

  // Desired Division  Change
  radioButtonsDesiredDivision.forEach(function (radio, index) {
    radio.addEventListener('change', getDivisionPrice);
  });

  // Mark Changes
  ranked_type_selected.addEventListener("change", getDivisionPrice);

  // Server Changes
  division_server_select_element.addEventListener("change", getDivisionPrice);

  // ----------------------------- Placments Boost ---------------------------------

  // Pervious Varible
  const placementsRanks = $('input[name="placement-ranks"]');

  // Game Count
  const gameCount = $("#game-count");
  const gameCountSteps = $('.game-count-step.step-indicator .step');

  // Server
  const placement_server_select_element = $('.placement-servers-select');

  const getPlacementPrice = () => {
    const checkedIndexRank = placementsRanks.index($('input[name="placement-ranks"]:checked'));
    const perviousElementRank = placementsRanks.eq(checkedIndexRank);

    const perviousRank = checkedIndexRank + 1;
  
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

  // ----------------------------- Seasonal Reward ---------------------------------
  // Current Seasonal Varible
  const seasonalRanks = $('input[name="seasonal-ranks"]');

  // Number Of Win
  const numOfWin = $("#num-win");
  const numOfWinSteps = $('.num-win-step.step-indicator .step');

  // Server
  const seasonal_server_select_element = $('.seasonal-servers-select');

  const getSeasonalPrice = () => {
    const checkedIndexRank = seasonalRanks.index($('input[name="seasonal-ranks"]:checked'));
    const currentSeasonalElementRank = seasonalRanks.eq(checkedIndexRank);
    const currentSeasonalRank = checkedIndexRank + 1;
  
    const currentSeasonalRankName = ranksNames[currentSeasonalRank]
    
    const numOfWinValue = Number(numOfWin.val())
    
    const rankPrice = currentSeasonalElementRank.data('price');

    const selectedSeasonalServer = seasonal_server_select_element.val()

    let price = (rankPrice * numOfWinValue);

    // Apply extra charges to the result
    price = price + (price * total_Percentage)

    // Apply promo code 
    price = setPromoAmount(price, discount_amount)

    price = parseFloat(price.toFixed(2))

    // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
    $('.seasonal-reward .current-seasonal-rank-selected-img').attr('src', $(currentSeasonalElementRank).data('img'))
    $('.num-of-wins').text(numOfWinValue);

    $('.seasonal-reward .current-seasonal-selected-info').html(`${currentSeasonalRankName}`)
    $('.seasonal-reward .num-win-selected-info').html(`${numOfWinValue} Matches`)

    $('.current-seasonal').removeClass().addClass(`current-seasonal ${currentSeasonalRankName}`);
    $('.matches-amount').removeClass().addClass(`matches-amount ${currentSeasonalRankName}`);

    $('.total-price #seasonal-reward-price').text(`$${price}`)

    changeUI(numOfWinValue, numOfWin, numOfWinSteps, 1)
  

    if ($('.seasonal-reward input[name="game_type"]').val() == 'S') {
      $('.seasonal-reward input[name="current_rank"]').val(currentSeasonalRank);
      $('.seasonal-reward input[name="number_of_wins"]').val(numOfWinValue);
      $('.seasonal-reward input[name="server"]').val(selectedSeasonalServer);
      $('.seasonal-reward input[name="price"]').val(price);
    }
  }
  getSeasonalPrice()

  seasonalRanks.each(function (index, radio) {
    $(radio).on('change', getSeasonalPrice);
  });

  numOfWin.on("input", getSeasonalPrice);

  // Server Changes
  seasonal_server_select_element.on("change", getSeasonalPrice);

  // ----------------------------- Tournament Boost ---------------------------------
  // Current League Varible
  const tournamentRanks = $('input[name="tournament-ranks"]');

  // Server
  const tournament_server_select_element = $('.tournament-servers-select');

  const getTournamentPrice = () => {
    const checkedIndexRank = tournamentRanks.index($('input[name="tournament-ranks"]:checked'));
    const currentTournamentElementRank = tournamentRanks.eq(checkedIndexRank);
    const currentTournamentRank = checkedIndexRank + 1;
  
    const currentTournamentRankName = ranksNames[currentTournamentRank]
    
    const rankPrice = currentTournamentElementRank.data('price');

    const selectedTournamentServer = tournament_server_select_element.val()

    let price = rankPrice;

    // Apply extra charges to the result
    price = price + (price * total_Percentage)

    // Apply promo code 
    price = setPromoAmount(price, discount_amount)

    price = parseFloat(price.toFixed(2))

    // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
    $('.tournament-boost .current-league-rank-selected-img').attr('src', $(currentTournamentElementRank).data('img'))

    $('.tournament-boost .current-league-selected-info').html(`${currentTournamentRankName}`)

    $('.current-league').removeClass().addClass(`current-league ${currentTournamentRankName}`);

    $('.total-price #tournament-boost-price').text(`$${price}`)

    if ($('.tournament-boost input[name="game_type"]').val() == 'T') {
      $('.tournament-boost input[name="current_league"]').val(currentTournamentRank);
      $('.tournament-boost input[name="server"]').val(selectedTournamentServer);
      $('.tournament-boost input[name="price"]').val(price);
    }
  }
  getTournamentPrice()

  tournamentRanks.each(function (index, radio) {
    $(radio).on('change', getTournamentPrice);
  });

  // Server Changes
  tournament_server_select_element.on("change", getTournamentPrice);

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

      getDivisionPrice();
      getPlacementPrice();
      getSeasonalPrice();
      getTournamentPrice();
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
    
      getDivisionPrice();
      getPlacementPrice();
      getSeasonalPrice();
      getTournamentPrice();
    })
  });
 
  promo_form.addEventListener('submit', async function(event) {
    event.preventDefault();
    if(!extend_order) {
      discount_amount = await fetch_promo(); 
      getDivisionPrice(); 
      getPlacementPrice();
      getSeasonalPrice();
      getTournamentPrice();
    }
  });
});

// Array For Names 
const ranksNames = ['unrank', 'bronze', 'silver', 'gold', 'platinum', 'diamond', 'champion', 'grand champion', 'supersonic legend']

const divisionNames = [0, 'I', 'II', 'III']
// ----------------------------- Division Boost ---------------------------------

// Read Values From Json File
let divisionPrices = [0];
Promise.all([
  new Promise(function (resolve, reject) {
    $.getJSON('/static/rocketLeague/data/divisions_data.json', function (data) {
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
      result -= result * (discountAmount/100 )

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
      result -= result * (discount_amount/100 )

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
      // getPlacementPrice()
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
      // getPlacementPrice()
    })
  });
 
  promo_form.addEventListener('submit', async function(event) {
    event.preventDefault();
    if(!extend_order) {
      discount_amount = await fetch_promo(); 
      getDivisionPrice(); 
      // getPlacementPrice();
    }
  });
});

// ----------------------------- Placments Boost ---------------------------------
// const placementRank = $('input[name="radio-group-placement-ranks"]');
// const gameCountSlider = $("#game-count");
// const gameCountValue = $(".game-count-value");
// const gameCounterInitial = Number(gameCountSlider.val())
// const initiallyPlacementCheckedIndexRank = $('input[name="radio-group-placement-ranks"]').index($('input[name="radio-group-placement-ranks"]:checked'));
// const initiallyPlacementCheckedRank = $('input[name="radio-group-placement-ranks"]').eq(initiallyPlacementCheckedIndexRank);
// const initiallyPlacementCheckedIndexRankPrice = initiallyPlacementCheckedRank.data('price');

// let last_rank = initiallyPlacementCheckedIndexRank + 1
// let placementRankPrice = initiallyPlacementCheckedIndexRankPrice
// let gameCounter = gameCounterInitial

// const getPlacementPrice = () => {
//   let price = (placementRankPrice * gameCounter);
//   price = parseFloat(price + (price * total_Percentage)).toFixed(2)
//   const priceDiv = $('.price-data.placements-boost').eq(0);
//   priceDiv.html(`
//   <p class='fs-5 text-uppercase my-4 text-secondary'>Boosting of <span class='fw-bold text-white'>${gameCounter} Placement Games</span></p>
//   <h4>$${price}</h4>
//   `);

//   if ($('.placements-boost input[name="game_type"]').val() == 'P') {
//     $('.placements-boost input[name="last_rank"]').val(last_rank);
//     $('.placements-boost input[name="number_of_match"]').val(gameCounter);
//     $('.placements-boost input[name="price"]').val(price);
//   }
// }
// getPlacementPrice()

// placementRank.each(function (index, radio) {
//   $(radio).on('change', function () {
//     const selectedIndex = placementRank.index(radio) + 1;
//     last_rank = selectedIndex;
//     placementRankPrice = $(radio).data('price');
//     getPlacementPrice()
//   });
// });

// gameCountSlider.on("input", function (event) {
//   gameCounter = Number(event.target.value);

//   gameCountValue.text(gameCounter);

//   const progress = (gameCounter / gameCountSlider.prop("max")) * 100;

//   gameCountSlider.css("background", `linear-gradient(to right, var(--main-color) ${progress}%, #ccc ${progress}%)`);

//   gameCountSlider.css("--thumb-rotate", `${(gameCounter / 100) * 2160}deg`);

//   getPlacementPrice()
// });

// // ----------------------------- Seasonal Reward ---------------------------------
// const seasonalRank = $('input[name="radio-group-seasonal-ranks"]');
// const numberWinSlider = $("#num-win");
// const numberWinValue = $(".number-win-value");
// const numberWinInitial = Number(numberWinSlider.val())
// const initiallySeasonalCheckedIndexRank = $('input[name="radio-group-seasonal-ranks"]').index($('input[name="radio-group-seasonal-ranks"]:checked'));
// const initiallySeasonalCheckedRank = $('input[name="radio-group-seasonal-ranks"]').eq(initiallySeasonalCheckedIndexRank);
// const initiallySeasonalCheckedIndexRankPrice = initiallySeasonalCheckedRank.data('price');

// let current_rank = initiallySeasonalCheckedIndexRank + 1
// let seasonalRankPrice = initiallySeasonalCheckedIndexRankPrice
// let numberWin = numberWinInitial

// const getSeasonalPrice = () => {
//   let price = (seasonalRankPrice * numberWin);
//   price = parseFloat(price + (price * total_Percentage)).toFixed(2)
//   const priceDiv = $('.price-data.seasonal-reward').eq(0);
//   priceDiv.html(`
//   <p class='fs-5 text-uppercase my-4 text-secondary'>Seasonal Reward Boosting by <span class='fw-bold text-white'>${numberWin} Wins</span></p>
//   <h4>$${price}</h4>
//   `);

//   if ($('.seasonal-reward input[name="game_type"]').val() == 'S') {
//     $('.seasonal-reward input[name="current_rank"]').val(current_rank);
//     $('.seasonal-reward input[name="number_of_wins"]').val(numberWin);
//     $('.seasonal-reward input[name="price"]').val(price);
//   }
// }
// getSeasonalPrice()

// seasonalRank.each(function (index, radio) {
//   $(radio).on('change', function () {
//     const selectedIndex = seasonalRank.index(radio) + 1;
//     current_rank = selectedIndex;
//     seasonalRankPrice = $(radio).data('price');
//     getSeasonalPrice()
//   });
// });

// numberWinSlider.on("input", function (event) {
//   numberWin = Number(event.target.value);

//   numberWinValue.text(numberWin);

//   const progress = (numberWin / numberWinSlider.prop("max")) * 100;

//   numberWinSlider.css("background", `linear-gradient(to right, var(--main-color) ${progress}%, #ccc ${progress}%)`);

//   numberWinSlider.css("--thumb-rotate", `${(numberWin / 100) * 2160}deg`);

//   getSeasonalPrice()
// });

// // ----------------------------- Tournament Boost ---------------------------------
// const tournamentRank = $('input[name="radio-group-tournament-ranks"]');
// const initiallyTournamentCheckedIndexRank = $('input[name="radio-group-tournament-ranks"]').index($('input[name="radio-group-tournament-ranks"]:checked'));
// const initiallyTournamentCheckedRank = $('input[name="radio-group-tournament-ranks"]').eq(initiallyTournamentCheckedIndexRank);
// const initiallyTournamentCheckedIndexRankPrice = initiallyTournamentCheckedRank.data('price');

// let current_league = initiallyTournamentCheckedIndexRank + 1
// let tournamentRankPrice = initiallyTournamentCheckedIndexRankPrice

// const getTournamentPrice = () => {
//   let price = tournamentRankPrice;
//   price = parseFloat(price + (price * total_Percentage)).toFixed(2)
//   const priceDiv = $('.price-data.tournament-boost').eq(0);
//   priceDiv.html(`
//   <p class='fs-5 text-uppercase my-4 text-secondary'>${ranksNames[current_league]} League <span class='fw-bold text-white'>Tournament Win</span></p>
//   <h4>$${price}</h4>
//   `);

//   if ($('.tournament-boost input[name="game_type"]').val() == 'T') {
//     $('.tournament-boost input[name="current_league"]').val(current_league);
//     $('.tournament-boost input[name="price"]').val(price);
//   }
// }
// getTournamentPrice()

// tournamentRank.each(function (index, radio) {
//   $(radio).on('change', function () {
//     const selectedIndex = tournamentRank.index(radio) + 1;
//     current_league = selectedIndex;
//     tournamentRankPrice = $(radio).data('price');
//     getTournamentPrice()
//   });
// });
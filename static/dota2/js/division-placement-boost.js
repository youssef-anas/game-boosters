// ----------------------------- Prices ---------------------------------
let dota2Data = $('#dota2Data');
const MMR_PRICES  = [0].concat(dota2Data.data('divsion'));
const PLACEMENT_PRICES =  [0].concat(dota2Data.data('placement'));
const RANKS_IMAGES = [0].concat(dota2Data.data('images'));
const ROLE_PRICES = [0, 0, 0.30]

// ----------------------------- Division Boost ---------------------------------
const ranks = ["unrank", "herald", "guardian", "crusader", "archon", "legend", "ancient", "divine", "immortal"]
const MIN_DESIRED_VALUE = 50

function getRank(mmr)  {
  if (mmr <= 700) {
    return [ranks[1], 1]
  } 

  if (mmr <= 1540) {
    return [ranks[2], 2]
  }

  if (mmr <= 2380) {
    return [ranks[3], 3]
  }

  if (mmr <= 3220) {
    return [ranks[4], 4]
  }

  if (mmr <= 4060) {
    return [ranks[5], 5]
  }

  if (mmr <= 4900) {
    return [ranks[6], 6]
  }

  if (mmr <= 5500) {
    return [ranks[7], 7]
  }

  if (mmr > 5500) {
    return [ranks[8], 8]
  }
}


function getPrice(currentMmr, desiredMmr) {
  function getRange(mmr) {
    if (mmr <= 2000) return MMR_PRICES[1]
    if (mmr <= 3000) return MMR_PRICES[2]
    if (mmr <= 4000) return MMR_PRICES[3]
    if (mmr <= 5000) return MMR_PRICES[4]
    if (mmr <= 5500) return MMR_PRICES[5]
    if (mmr <= 6000) return MMR_PRICES[6]
    if (mmr > 6000) return MMR_PRICES[7]
  }

  const currentRange = getRange(currentMmr);
  const desiredRange = getRange(desiredMmr);

  if(currentRange === desiredRange) return currentRange
  else return (desiredRange + currentRange) / 2
}

function changeUI(achivedValue, arena, steps) {
  const progress = ((achivedValue) / (arena.prop("max"))) * 100;

  arena.css({
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

// Current Varible
const currentMmr = $('#current-mmr');
const currentSteps = $('.current-step.step-indicator .step');
let currentMmrValue = Number(currentMmr.val())
let currentRank = getRank(currentMmrValue)[0]

// Desired Varible
const desiredMmr = $('#desired-mmr');
const desiredSteps = $('.desired-step.step-indicator .step');
let desiredMmrValue = Number(desiredMmr.val())
let desiredRank = getRank(desiredMmrValue)[0]


if(extend_order) {
  $('input[type="radio"]#placements-boost').prop('disabled', true)

  let orderID = parseInt(extend_order, 10);
  document.getElementById('extendOrder').value = orderID; 

  division_server_select_element.disabled = true
  role_selected.disabled = true

  division_server_select_element.value = server
  role_selected.value = roleValue

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
      checkbox.checked = true
      total_Percentage += percentege[checkbox.value];
      $(`input#${checkbox.value}`).val(true)

    } else if (checkbox.value === "turboBoost" && valuesToSetAdditional[2]) {
      checkbox.checked = true
      total_Percentage += percentege[checkbox.value];
      $(`input#${checkbox.value}`).val(true)

    } else if (checkbox.value === "streaming" && valuesToSetAdditional[3]) {
      checkbox.checked = true
      total_Percentage += percentege[checkbox.value];
      $(`input#${checkbox.value}`).val(true)

    } else if (checkbox.value === "boosterChampions" && valuesToSetAdditional[4]) {
      checkbox.checked = true
      total_Percentage += percentege[checkbox.value];
      $(`input#${checkbox.value}`).val(true)

    } else {
      checkbox.checked = false
      $(`input#${checkbox.value}`).val(false)
    } 
    
    $(checkbox).prop('disabled', true)
  }) 
  
  // Change Values
  currentRank = getRank(valuesToSet[1])[0]
  desiredRank = getRank(valuesToSet[4])[0]
  currentMmrValue = valuesToSet[1]
  desiredMmrValue = valuesToSet[4]

  // Change Range Value
  currentMmr.val(currentMmrValue) 
  desiredMmr.val(desiredMmrValue) 

  // Change Range UI
  changeUI(currentMmrValue, currentMmr, currentSteps)
  changeUI(desiredMmrValue, desiredMmr, desiredSteps)

  // Disable Current
  currentMmr.prop('disabled', true)

  function getDivisionPrice() {
    const MMR_PRICE = getPrice(valuesToSet[4], desiredMmrValue)
    // Price
    let price = ((desiredMmrValue - valuesToSet[4]) * (MMR_PRICE / MIN_DESIRED_VALUE));

    // Apply role extra value
    const total_Percentage_with_role_result = total_Percentage + ROLE_PRICES[roleValue]

    // Apply extra charges to the result
    price += price * total_Percentage_with_role_result;
  
    // Apply promo code 
    price -= price * (discountAmount / 100 )
  
    price = parseFloat(price.toFixed(2));
  
    // Current
    $('#current .current-rp').html(currentMmrValue);
    $('.current-rank-selected-img:not(.checkout-img)').attr('src', RANKS_IMAGES[getRank(currentMmrValue)[1]]);
    $('.current-rank-selected-img.checkout-img').attr('src', RANKS_IMAGES[getRank(valuesToSet[4])[1]])
    $('.current').removeClass().addClass(`current ${getRank(currentMmrValue)[0]}`);
    $('.current-selected-info').html(`${valuesToSet[4]} MMR`)
  
    // Desired
    $('#desired .desired-rp').html(desiredMmrValue);
    $('.desired-selected-img').attr('src', RANKS_IMAGES[desiredRank]);
    $('.desired').removeClass().addClass(`desired ${desiredRank}`);
    $('.desired-selected-info').html(`${desiredMmrValue} MMR`)
  
    // Price
    $('.total-price #division-boost-price').html(`$${price}`)
  
    // Form
    $('.division-boost input[name="current_rank"]').val(getRank(currentMmrValue)[1]);
    $('.division-boost input[name="current_division"]').val(currentMmrValue);
    $('.division-boost input[name="role"]').val(roleValue);
    $('.division-boost input[name="desired_rank"]').val(getRank(desiredMmrValue)[1]);
    $('.division-boost input[name="desired_division"]').val(desiredMmrValue);
    $('.division-boost input[name="server"]').val(server);
    $('.division-boost input[name="price"]').val(price);

    // SET PROMO CODE IN FORM
    $('#division-boost input[name="promo_code"]').val(extendPromoCode);
    
  }

} else {

  function getDivisionPrice() {
    const selectedDivsionServer = division_server_select_element.value;
    const role = role_selected.value;

    const MMR_PRICE = getPrice(currentMmrValue, desiredMmrValue)

    // Price
    let price = (desiredMmrValue - currentMmrValue) * (MMR_PRICE / MIN_DESIRED_VALUE);

    // Apply role extra value
    const total_Percentage_with_role_result = total_Percentage + ROLE_PRICES[role]

    // Apply extra charges to the result
    price += price * total_Percentage_with_role_result;
  
    // Apply promo code 
    price -= price * (discount_amount / 100 )
  
    price = parseFloat(price.toFixed(2));
  
    // Current
    $('#current .current-rp').html(currentMmrValue);
    $('.current-selected-img').attr('src', RANKS_IMAGES[getRank(currentMmrValue)[1]]);
    $('.current').removeClass().addClass(`current ${currentRank}`);
    $('.current-selected-info').html(`${currentMmrValue} MMR`)
  
    // Desired
    $('#desired .desired-rp').html(desiredMmrValue);
    $('.desired-selected-img').attr('src', RANKS_IMAGES[getRank(desiredMmrValue)[1]]);
    $('.desired').removeClass().addClass(`desired ${desiredRank}`);
    $('.desired-selected-info').html(`${desiredMmrValue} MMR`)
  
    // Price
    $('.total-price #division-boost-price').html(`$${price}`)
  
    // Form
    $('.division-boost input[name="current_rank"]').val(getRank(currentMmrValue)[1]);
    $('.division-boost input[name="current_division"]').val(currentMmrValue);
    $('.division-boost input[name="role"]').val(role);
    $('.division-boost input[name="desired_rank"]').val(getRank(desiredMmrValue)[1]);
    $('.division-boost input[name="desired_division"]').val(desiredMmrValue);
    $('.division-boost input[name="server"]').val(selectedDivsionServer);
    $('.division-boost input[name="price"]').val(price);
    
  }

}

getDivisionPrice();

currentMmr.on("input", function (event) {
  currentMmrValue = Number(event.target.value);
  currentRank = getRank(currentMmrValue)[0];

  if((desiredMmrValue - currentMmrValue) < MIN_DESIRED_VALUE) {
    desiredMmr.val(currentMmrValue + MIN_DESIRED_VALUE);
    desiredMmrValue = currentMmrValue + MIN_DESIRED_VALUE;
    desiredRank = getRank(desiredMmrValue)[0];

    changeUI(desiredMmrValue, desiredMmr, desiredSteps);
  }
  
  changeUI(currentMmrValue, currentMmr, currentSteps)

  getDivisionPrice()

})

desiredMmr.on("input", function (event) {
  desiredMmrValue = Number(event.target.value);
  desiredRank = getRank(desiredMmrValue)[0];

  if((desiredMmrValue - currentMmrValue) < MIN_DESIRED_VALUE) {
    desiredMmr.val(currentMmrValue + MIN_DESIRED_VALUE);
    desiredMmrValue = currentMmrValue + MIN_DESIRED_VALUE;
    desiredRank = getRank(desiredMmrValue)[0];

    changeUI(desiredMmrValue, desiredMmr, desiredSteps);
  }
  
  if (extend_order && desiredMmrValue < valuesToSet[4]) {
    desiredMmr.val(valuesToSet[4])
    desiredMmrValue = valuesToSet[4];
    desiredRank = getRank(desiredMmrValue)[0];
    changeUI(desiredMmrValue, desiredMmr, desiredSteps);
  }

  changeUI(desiredMmrValue, desiredMmr, desiredSteps);

  getDivisionPrice()

})

// Server Changes
division_server_select_element.addEventListener("change", getDivisionPrice);
role_selected.addEventListener("change", getDivisionPrice)
  
// ----------------------------- Placments Boost ---------------------------------
// const placementsRanks = $('input[name="placement-ranks"]');
// const gameCountInput = $("#game-count");
// const steps = $('.step-indicator .step');
// const gameCounterInitial = Number(gameCountInput.val())
// const initiallyCheckedIndexRank = $('input[name="placement-ranks"]').index($('input[name="placement-ranks"]:checked'));
// const initiallyCheckedRank = $('input[name="placement-ranks"]').eq(initiallyCheckedIndexRank);
// const initiallyCheckedIndexRankPrice = initiallyCheckedRank.data('price');
// const placement_server_select_element = $('.placement-servers-select');

// let perviousElement = Array.from(placementsRanks).find(radio => radio.checked);

// let pervious_rank = initiallyCheckedIndexRank
// let pervious_rank_name = ranksNames[pervious_rank]
// let rank_price = initiallyCheckedIndexRankPrice
// let gameCounter = gameCounterInitial
// let selectedPlacementServer = placement_server_select_element.val()

// const getPlacementPrice = () => {
//   let price = (rank_price * gameCounter);
//   // Apply extra charges to the result
//   price = price + (price * total_Percentage)
//   // Apply promo code 
//   price -= price * (discount_amount / 100 )

//   price = parseFloat(price.toFixed(2))

//   // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
//   $('.placements-boost .pervious-rank-selected-img').attr('src', $(perviousElement).data('img'))
//   $('.num-of-match').text(gameCounter);

//   $('.placements-boost .pervious-selected-info').html(`${pervious_rank_name}`)
//   $('.placements-boost .game_count-selected-info').html(`${gameCounter} Matches`)

//   $('.pervious').removeClass().addClass(`pervious ${pervious_rank_name}`);

//   $('.total-price #placements-boost-price').text(`$${price}`)

//   const pricee = $('.price-data.placements-boost').eq(0);
//   pricee.html(`
//   <p class='fs-5 text-uppercase my-4'>Boosting of <span class='fw-bold'>${gameCounter} Placement Games</span></p>
//   <h4>$${price}</h4>
//   `);

//   if ($('.placements-boost input[name="game_type"]').val() == 'P') {
//     $('.placements-boost input[name="last_rank"]').val(pervious_rank);
//     $('.placements-boost input[name="number_of_match"]').val(gameCounter);
//     $('.placements-boost input[name="server"]').val(selectedPlacementServer);
//     $('.placements-boost input[name="price"]').val(price);
//   }
// }

// getPlacementPrice()

// placementsRanks.each(function (index, radio) {
//   $(radio).on('change', function () {
//     const selectedIndex = placementsRanks.index(radio);
//     pervious_rank = selectedIndex;
//     pervious_rank_name = ranksNames[pervious_rank]
//     rank_price = $(radio).data('price');

//     // Look Here:- When Desired Rank Change Change Value So Image Changed 
//     perviousElement = Array.from(placementsRanks).find(radio => radio.checked);

//     getPlacementPrice()
//   });
// });

// gameCountInput.on("input", function (event) {
//   gameCounter = Number(event.target.value);
  
//   const progress = ((gameCounter - 1) / (gameCountInput.prop("max") - 1)) * 100;

//   gameCountInput.css({
//     "background": `linear-gradient(to right, #F36E3F ${progress}%, #251D16 ${progress}%)`
//   });

//   steps.each((step, index) => {
//     var $step = $(step);
//     if (index < gameCounter) {
//       $step.addClass('selected');
//     } else {
//       $step.removeClass('selected');
//     }
//   });

//   getPlacementPrice()

// })

// // Server Changes
// placement_server_select_element.on("change", function() {

//   selectedPlacementServer = $(this).val();
//   getPlacementPrice();
// });

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
// ----------------------------- Prices ---------------------------------
let dota2Data = $('#dota2Data');
const MMR_PRICES  = [0].concat(dota2Data.data('divsion'));
const PLACEMENT_PRICES =  [0].concat(dota2Data.data('placement'));
const RANKS_IMAGES = [0].concat(dota2Data.data('images'));
const ROLE_PRICES = [0, 0, 0.30]

// ----------------------------- Division Boost ---------------------------------
const ranks = ["unrank", "herald", "guardian", "crusader", "archon", "legend", "ancient", "divine", "immortal"]
const MIN_DESIRED_VALUE = 50

function getRangeCurrent(mmr) {
  const MAX_LISTS = [0, 2000, 3000, 4000, 5000, 5500, 6000, 8000];
  for (let idx = 1; idx < MAX_LISTS.length; idx++) {
      const max_val = MAX_LISTS[idx];
      if (mmr <= max_val) {
          const val = max_val - mmr;
          return [Math.floor(val / 50), idx];
      }
  }
  console.log('out_of_range');
  return [null, null];
}

function getRangeDesired(mmr) {
  const MAX_LISTS = [0, 2000, 3000, 4000, 5000, 5500, 6000, 8000];
  for (let idx = 1; idx < MAX_LISTS.length; idx++) {
      const max_val = MAX_LISTS[idx];
      if (mmr <= max_val) {
          const val = mmr - MAX_LISTS[idx-1];
          return [Math.floor(val / 50), idx];
      }
  }
  console.log('out_of_range');
  return [null, null];
}
const price1 = Math.round(MMR_PRICES[1] * 40 * 10) / 10;
const price2 = Math.round(MMR_PRICES[2] * 20 * 10) / 10;
const price3 = Math.round(MMR_PRICES[3] * 20 * 10) / 10;
const price4 = Math.round(MMR_PRICES[4] * 20 * 10) / 10;
const price5 = Math.round(MMR_PRICES[5] * 10 * 10) / 10;
const price6 = Math.round(MMR_PRICES[6] * 10 * 10) / 10;
const price7 = Math.round(MMR_PRICES[7] * 40 * 10) / 10;

const full_price_val = [price1, price2, price3, price4, price5, price6, price7];

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


// function getPrice(currentMmr, desiredMmr) {
//   function getRange(mmr) {
//     if (mmr <= 2000) return MMR_PRICES[1]
//     if (mmr <= 3000) return MMR_PRICES[2]
//     if (mmr <= 4000) return MMR_PRICES[3]
//     if (mmr <= 5000) return MMR_PRICES[4]
//     if (mmr <= 5500) return MMR_PRICES[5]
//     if (mmr <= 6000) return MMR_PRICES[6]
//     if (mmr > 6000) return MMR_PRICES[7]
//   }

//   const currentRange = getRange(currentMmr);
//   const desiredRange = getRange(desiredMmr);

//   if(currentRange === desiredRange) return currentRange
//   else return (desiredRange + currentRange) / 2
// }

function changeUI(achivedValue, arena, steps, miuns = 0) {
  const progress = ((achivedValue - miuns) / (arena.prop("max") - miuns) ) * 100;

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
    // const MMR_PRICE = getPrice(valuesToSet[1], valuesToSet[4])

    // Price
    // let price = ((desiredMmrValue - valuesToSet[4]) * (MMR_PRICE / MIN_DESIRED_VALUE));

    let [current_mmr_in_c_range, current_range] = getRangeCurrent(valuesToSet[4]);
    let [desired_mmr_in_d_range, desired_range] = getRangeDesired(desiredMmrValue);
    let sliced_prices = full_price_val.slice(current_range, desired_range - 1);
    let sum_current = current_mmr_in_c_range * MMR_PRICES[current_range];
    let sum_desired = desired_mmr_in_d_range * MMR_PRICES[desired_range];
    let clear_res = sliced_prices.reduce((acc, val) => acc + val, 0);
    let price = 0
    if(current_range==desired_range){
      let range_value = Math.floor((desiredMmrValue - valuesToSet[4])/50)
      price = range_value * MMR_PRICES[current_range]
    }else{
      price = sum_current + sum_desired + clear_res
    }


    // Apply role extra value
    const total_Percentage_with_role_result = total_Percentage + ROLE_PRICES[roleValue]

    // Apply extra charges to the result
    price += price * total_Percentage_with_role_result;
  
    // Apply promo code 
    price = setPromoAmount(price, discountAmount)
  
    price = parseFloat(price.toFixed(2));
  
    // Current
    $('#current .current-rp').html(currentMmrValue);

    $('.current-selected-img:not(.checkout-img)').attr('src', RANKS_IMAGES[getRank(currentMmrValue)[1]]);
    $('.current-selected-img.checkout-img').attr('src', RANKS_IMAGES[getRank(valuesToSet[4])[1]])

    $('.current').removeClass().addClass(`current ${currentRank}`);
    $('.current-selected-info').html(`${valuesToSet[4]} MMR`)
  
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
    $('.division-boost input[name="role"]').val(roleValue);
    $('.division-boost input[name="desired_rank"]').val(getRank(desiredMmrValue)[1]);
    $('.division-boost input[name="desired_division"]').val(desiredMmrValue);
    $('.division-boost input[name="server"]').val(server);
    $('.division-boost input[name="price"]').val(price);

    // SET PROMO CODE IN FORM
    $('.division-boost input[name="promo_code"]').val(extendPromoCode);
    
  }

} else {

  function getDivisionPrice() {
    const selectedDivsionServer = division_server_select_element.value;
    const role = role_selected.value;

    // const MMR_PRICE = getPrice(currentMmrValue, desiredMmrValue)


    let [current_mmr_in_c_range, current_range] = getRangeCurrent(currentMmrValue);
    let [desired_mmr_in_d_range, desired_range] = getRangeDesired(desiredMmrValue);
    let sliced_prices = full_price_val.slice(current_range, desired_range - 1);
    let sum_current = current_mmr_in_c_range * MMR_PRICES[current_range];
    let sum_desired = desired_mmr_in_d_range * MMR_PRICES[desired_range];
    let clear_res = sliced_prices.reduce((acc, val) => acc + val, 0);
    let price = 0
    if(current_range==desired_range){
      let range_value = Math.floor((desiredMmrValue - currentMmrValue)/50)
      price = range_value * MMR_PRICES[current_range]
    }else{
      price = sum_current + sum_desired + clear_res
    }
    
    // Price
    // let price = (desiredMmrValue - currentMmrValue) * (MMR_PRICE / MIN_DESIRED_VALUE);


    // Apply role extra value
    const total_Percentage_with_role_result = total_Percentage + ROLE_PRICES[role]

    // Apply extra charges to the result
    price += price * total_Percentage_with_role_result;
  
    // Apply promo code 
    price = setPromoAmount(price, discount_amount)
  
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
    let newValue = currentMmrValue + MIN_DESIRED_VALUE;

    if(newValue > 8000) {
      newValue = 8000;
      currentMmr.val(newValue - MIN_DESIRED_VALUE);
      currentMmrValue = newValue - MIN_DESIRED_VALUE;
      currentRank = getRank(currentMmrValue)[0];
    }
    desiredMmr.val(newValue);
    desiredMmrValue = newValue;
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
    let newValue = currentMmrValue + MIN_DESIRED_VALUE;

    if(newValue > 8000) {
      newValue = 8000;
      currentMmr.val(newValue - MIN_DESIRED_VALUE);
      currentMmrValue = newValue - MIN_DESIRED_VALUE;
      currentRank = getRank(currentMmrValue)[0];
    }
    desiredMmr.val(newValue);
    desiredMmrValue = newValue;
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
// Pervious Varible
const perviousMmr = $('#pervious-mmr');
const perviousSteps = $('.pervious-step.step-indicator .step');

// Game Count
const gameCount = $("#game-count");
const gameCountSteps = $('.game-count-step.step-indicator .step');

// Server
const placement_server_select_element = $('.placement-servers-select');
// Role
const placement_role_select = $('.placement-role-select');

const getPlacementPrice = () => {

  let perviousMmrValue = Number(perviousMmr.val())
  let perviousRank = getRank(perviousMmrValue)[0]

  let gameCounterValue = Number(gameCount.val())

  const selectedPlacementServer = placement_server_select_element.val();
  const role = placement_role_select.val();

  const RANK_PRICE = PLACEMENT_PRICES[getRank(perviousMmrValue)[1]]

  let price = (RANK_PRICE * gameCounterValue);
  // Apply role extra value
  const total_Percentage_with_role_result = total_Percentage + ROLE_PRICES[role]

  // Apply extra charges to the result
  price += price * total_Percentage_with_role_result;

  // Apply promo code 
  price = setPromoAmount(price, discount_amount)

  price = parseFloat(price.toFixed(2));

  // Pervious
  $('#pervious .pervious-rp').html(perviousMmrValue);
  $('.pervious-selected-img').attr('src', RANKS_IMAGES[getRank(perviousMmrValue)[1]]);
  $('.pervious').removeClass().addClass(`pervious ${perviousRank}`);
  $('.pervious-selected-info').html(`${perviousMmrValue} MMR`);
  changeUI(perviousMmrValue, perviousMmr, perviousSteps);

  // Counter
  $('#matches-amount .num-of-match').html(gameCounterValue);
  $('.matches-amount').removeClass().addClass(`matches-amount ${perviousRank}`);
  $('.game_count-selected-info').html(`${gameCounterValue} Matches`)
  changeUI(gameCounterValue, gameCount, gameCountSteps, 1);

  // Price
  $('.total-price #placements-boost-price').text(`$${price}`)

  // Form
  $('.placements-boost input[name="last_rank"]').val(getRank(perviousMmrValue)[1]);
  $('.placements-boost input[name="last_division"]').val(perviousMmrValue);
  $('.placements-boost input[name="role"]').val(role);
  $('.placements-boost input[name="number_of_match"]').val(gameCounterValue);
  $('.placements-boost input[name="server"]').val(selectedPlacementServer);
  $('.placements-boost input[name="price"]').val(price);
  
}

getPlacementPrice()

perviousMmr.on("input", getPlacementPrice)
gameCount.on("input", getPlacementPrice)

// Server Changes
placement_server_select_element.on("change", getPlacementPrice);
// Role
placement_role_select.on("change", getPlacementPrice);

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
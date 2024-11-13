// Function UI
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

// Read Values From Json File
let divisionPrices = [0];
let marks_price = [[0, 0, 0, 0, 0]];
let role_price = 0
let premierPrices = [0]
let faceitPrices = []
Promise.all([
  new Promise(function (resolve, reject) {
    $.getJSON('/csgo2/division-prices/', function (data) {
      divisionPrices = divisionPrices.concat(...data);
      resolve();
    });
  }),

  new Promise(function (resolve, reject) {
    $.getJSON('/csgo2/premier-prices/', function (data) {
      premierPrices = premierPrices.concat(...data);
      resolve();
    });
  }),

  new Promise(function (resolve, reject) {
    $.getJSON('/csgo2/faceit-prices/', function (data) {
      faceitPrices = data;
      resolve();
    });
  }),
]).then(function () {
  // Array For Names 
  const divisionRanks = [
    "","SilverI", "SilverII", "SilverIII", "SilverIV", "SilverElite", "SEMstr", "GoldNVI", "GoldNVII", "GoldNVIII", "GoldNVMstr",
    "MstrGrdI", "MstrGrdII", "MstrGrdElite", "DMasterGrd", "LegEagle", "LegEagleMstr", "SupreMstrFC", "GlobalElite"
    ]

  // ----------------------------- Premier Funtion ---------------------------------

  const premierRanksNames = ['', 'silver', 'grey', 'blue', 'purple', 'pink', 'red']

  function getRangeCurrent(amount) {
    const MAX_LISTS = [4999, 7999, 11999, 18999, 20999, 24999, 30000];
    for (let idx = 0; idx < MAX_LISTS.length; idx++) {
        const max_val = MAX_LISTS[idx];
        if (amount <= max_val) {
          const val = max_val - amount;
          return [parseFloat((val / 500).toFixed(2)), idx + 1];
        }
    }
    console.log('out_of_range');
    return [null, null];
  }

  function getRangeDesired(amount) {
    const MAX_LISTS = [4999, 7999, 11999, 18999, 20999, 24999, 30000];
    for (let idx = 0; idx < MAX_LISTS.length; idx++) {
        const max_val = MAX_LISTS[idx];
        if (amount <= max_val) {
            const val = amount - MAX_LISTS[idx-1];
            return [parseFloat((val / 500).toFixed(2)), idx + 1];
        }
    }
    console.log('out_of_range');
    return [null, null];
  }
  const price1 = Math.round(premierPrices[1] * 10 * 100) / 100;
  const price2 = Math.round(premierPrices[2] * 6 * 100) / 100;
  const price3 = Math.round(premierPrices[3] * 8 * 100) / 100;
  const price4 = Math.round(premierPrices[4] * 14 * 100) / 100;
  const price5 = Math.round(premierPrices[5] * 4 * 100) / 100;
  const price6 = Math.round(premierPrices[6] * 8 * 100) / 100;
  const price7 = Math.round(premierPrices[7] * 10.002 * 100) / 100;

  const full_price_val = [price1, price2, price3, price4, price5, price6, price7];

  function getRank(division)  {
    if (division < 5000) {
      return [premierRanksNames[1], 1]
    } 

    if (division < 10000) {
      return [premierRanksNames[2], 2]
    }

    if (division < 15000) {
      return [premierRanksNames[3], 3]
    }

    if (division < 20000) {
      return [premierRanksNames[4], 4]
    }

    if (division < 25000) {
      return [premierRanksNames[5], 5]
    }

    if (division >= 25000) {
      return [premierRanksNames[6], 6]
    }

  }

  // ----------------------------- Premier Element Select ---------------------------------
  // Current Varible
  const currentPremierRank = $('#current-premier-rank');
  const currentPremierSteps = $('.current-premier-step.step-indicator .step');
  let currentDivision = Number(currentPremierRank.val())
  let currentRank = getRank(currentDivision)[1]
  let currentRankName = getRank(currentDivision)[0]

  // Desired Varible
  const desiredPremierRank = $("#desired-premier-rank");
  const desiredPremierSteps = $('.desired-premier-step.step-indicator .step');
  let desiredDivision = Number(desiredPremierRank.val())
  let desiredRank = getRank(desiredDivision)[1]
  let desiredRankName = getRank(desiredDivision)[0]

  // Server
  const premier_server_select_element = $('.premier-servers-select');

  // ----------------------------- Faceit Element Select ---------------------------------
  // Current Varible
  const currentFaceitLevel = $('#current-faceit-level');
  const currentFaceitSteps = $('.current-faceit-step.step-indicator .step');

  // Desired Varible
  const desiredFaceitLevel = $("#desired-faceit-level");
  const desiredFaceitSteps = $('.desired-faceit-step.step-indicator .step');

  // Server
  const faceit_server_select_element = $('.faceit-servers-select');

  // -------------------------------------------------------------------------------------
  if(extend_order) {
    const extends_from_divison = valuesToSetExtra[0]
    $('input[type="radio"]#faceit-boost').prop('disabled', true)

    let orderID = parseInt(extend_order, 10);

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
        $(`input#${checkbox.value}`).val(true)
        total_Percentage += percentege[checkbox.value];

      } else if (checkbox.value === "turboBoost" && valuesToSetAdditional[2]) {
        checkbox.checked = true
        $(`input#${checkbox.value}`).val(true)
        total_Percentage += percentege[checkbox.value];

      } else if (checkbox.value === "streaming" && valuesToSetAdditional[3]) {
        checkbox.checked = true
        $(`input#${checkbox.value}`).val(true)
        total_Percentage += percentege[checkbox.value];

      } else if (checkbox.value === "selectChampion" && valuesToSetAdditional[4]) {
        checkbox.checked = true
        $(`input#${checkbox.value}`).val(true)
        total_Percentage += percentege[checkbox.value];

      } else {
        checkbox.checked = false
        $(`input#${checkbox.value}`).val(false)
      } 
      $(checkbox).prop('disabled', true)
    })

    if (extends_from_divison) {
      divisionBoostRadio.checked = true
      divisionBoostChecked()

      $('input[type="radio"]#premier-boost').prop('disabled', true)

      $('.division-boost input[name="extend_order"]').val(orderID); 
      // SET PROMO CODE IN FORM
      $('.division-boost input[name="promo_code"]').val(extendPromoCode);

      // Set the checked state for each group of radio buttons using the specified order
      setRadioButtonStateWithDisable(radioButtonsCurrent, valuesToSet[0]-1);
      setRadioButtonStateWithDisable(radioButtonsCurrentDivision, valuesToSet[1]-1);
      setRadioButtonState(radioButtonsDesired, valuesToSet[3]-1, true);
      setRadioButtonStateForDesiredDivision(radioButtonsDesiredDivision, valuesToSet[4]-1);
      makrs_on_current_rank_selected.disabled = true
      division_server_select_element.disabled = true

      function getDivisionPrice() {
        const desired_rank = getSelectedValueForRadio(radioButtonsDesired)
        const desired_division = getSelectedValueForRadio(radioButtonsDesiredDivision)
  
        const current_rank = valuesToSet[0];
        const current_division = valuesToSet[1];
        const mark_index = valuesToSet[2];
        console.log(current_rank)
        
        const current_rank_name = divisionRanks[current_rank];
        const desired_rank_name = divisionRanks[desired_rank];
  
        makrs_on_current_rank_selected.value = mark_index
        division_server_select_element.value = server
        
        const startRank = ((valuesToSet[3] - 1) * 1) + 1; // 1 = current division
        const endRank = ((desired_rank - 1) * 1) ;
        const slicedArr = sliceArray(divisionPrices, startRank, endRank);
        
        const sum = slicedArr.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
  
        let result_with_mark = sum
        
        // Apply role extra value
        const total_Percentage_with_role_result = total_Percentage + role_price
  
        // Apply extra charges to the result
        result_with_mark += result_with_mark * total_Percentage_with_role_result;
        // Apply promo code 
        result_with_mark = setPromoAmount(result_with_mark, discountAmount)
        
        result_with_mark = parseFloat(result_with_mark.toFixed(2)); 
  
        const currentElement = getSelectedElement(radioButtonsCurrent)
        const desiredElement = getSelectedElement(radioButtonsDesired)
  
        // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
        $('.division-boost .current-rank-selected-img').attr('src', $(currentElement).data('img'))
        $('.division-boost .desired-rank-selected-img').attr('src', $(desiredElement).data('img'))
  
        $('.division-boost .desired-selected-info').html(`${desired_rank_name}`)
        $('.division-boost .current-selected-info').html(`${current_rank_name}`)
  
        $('.current').removeClass().addClass(`current ${current_rank_name}`)
        $('.desired').removeClass().addClass(`desired ${desired_rank_name}`)
  
        $('.total-price #division-boost-price').text(`$${result_with_mark}`)
  
        // From Value
        $('.division-boost input[name="current_rank"]').val(current_rank);
        $('.division-boost input[name="marks"]').val(mark_index);
        $('.division-boost input[name="desired_rank"]').val(desired_rank);
        $('.division-boost input[name="price"]').val(result_with_mark);
      }

      // Get Result 
      getDivisionPrice();

    } else {
      // Premier
      premierBoostRadio.checked = true
      premierBoostChecked() 

      $('input[type="radio"]#division-boost').prop('disabled', true)

      $('.premier-boost input[name="extend_order"]').val(orderID); 
      // SET PROMO CODE IN FORM
      $('.premier-boost input[name="promo_code"]').val(extendPromoCode);

      // Current Varible
      currentDivision = valuesToSet[1]
      currentRank = getRank(valuesToSet[1])[1]
      currentRankName = getRank(valuesToSet[1])[0]

      // Desired Varible
      desiredDivision = valuesToSet[4]
      desiredRank = getRank(valuesToSet[4])[1]
      desiredRankName = getRank(valuesToSet[4])[0]

      // Change Range Value
      currentPremierRank.val(currentDivision)
      desiredPremierRank.val(desiredDivision)

      // Disable Current
      currentPremierRank.prop('disabled', true)

      changeUI(currentDivision, currentPremierRank, currentPremierSteps);
      changeUI(desiredDivision, desiredPremierRank, desiredPremierSteps);

      premier_server_select_element.prop("disabled", true)

      function getPremierPrice() {
        // Server
        premier_server_select_element.val(server);

        desiredRankName = getRank(desiredDivision)[0]

        let [current_mmr_in_c_range, current_range] = getRangeCurrent(valuesToSet[4]);
        let [desired_mmr_in_d_range, desired_range] = getRangeDesired(desiredDivision);
        let sliced_prices = full_price_val.slice(current_range, desired_range - 1);
        let sum_current = current_mmr_in_c_range * premierPrices[current_range];
        let sum_desired = desired_mmr_in_d_range * premierPrices[desired_range];
        let clear_res = sliced_prices.reduce((acc, val) => acc + val, 0);
        let price = 0
        if (current_range==desired_range) {
          let range_value = Math.floor((desiredDivision - valuesToSet[4]) / 500)
          price = range_value * premierPrices[current_range]
        } else {
          price = sum_current + sum_desired + clear_res
        }

        // Apply extra charges to the result
        price += price * total_Percentage;
      
        // Apply promo code 
        price = setPromoAmount(price, discountAmount)
      
        price = parseFloat(price.toFixed(2));

        // Current Premier
        $('#current-premier .current-premier-number').html(currentDivision);
        $('.current-premier-selected-info').html(`${valuesToSet[4]} Premier Rank`);
        $('.current-premier').removeClass().addClass(`current-premier ${currentRankName}`);
        
        // Desired Premier
        $('#desired-premier .desired-premier-number').html(desiredDivision);
        $('.desired-premier-selected-info').html(`${desiredDivision} Premier Rank`);
        $('.desired-premier').removeClass().addClass(`desired-premier ${desiredRankName}`);
        
        // Price
        $('.total-price #premier-boost-price').text(`$${price}`)

        // Form
        if($('.premier-boost input[name="game_type"]').val() == 'A') {
          $('.premier-boost input[name="current_rank"]').val(currentRank);
          $('.premier-boost input[name="current_division"]').val(currentDivision);
          $('.premier-boost input[name="desired_rank"]').val(desiredRank);
          $('.premier-boost input[name="desired_division"]').val(desiredDivision);
          $('.premier-boost input[name="server"]').val(server);
          $('.premier-boost input[name="price"]').val(price);
        }
      }

      // Get Result 
      getPremierPrice();
    }
  
  } else {
    // ----------------------------- Division Boost ---------------------------------
    function getDivisionPrice() {

      const current_rank = getSelectedValueForRadio(radioButtonsCurrent);
      const desired_rank = getSelectedValueForRadio(radioButtonsDesired)
      const current_rank_name = divisionRanks[current_rank];
      const desired_rank_name = divisionRanks[desired_rank];

      const startRank = ((current_rank - 1) * 1) + 1;
      const endRank = ((desired_rank - 1) * 1);
      const slicedArray = sliceArray(divisionPrices, startRank, endRank);
      let result = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
      let result_with_mark = result
      
      //Apply role percent
      const total_Percentage_with_role_result = total_Percentage + role_price

      // Apply extra charges to the result
      result_with_mark += result_with_mark * total_Percentage_with_role_result;
      // Apply promo code 
      result_with_mark = setPromoAmount(result_with_mark, discount_amount)

      result_with_mark = parseFloat(result_with_mark.toFixed(2)); 

      // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
      const currentElement = getSelectedElement(radioButtonsCurrent)
      const desiredElement = getSelectedElement(radioButtonsDesired)

      // Look Here:- We Change Everything Should Change Depend On Current & Desired Element

      $('.division-boost .current-rank-selected-img').attr('src', $(currentElement).data('img'))
      $('.division-boost .desired-rank-selected-img').attr('src', $(desiredElement).data('img'))

      $('.division-boost .current-selected-info').html(`${current_rank_name}`);
      $('.division-boost .desired-selected-info').html(`${desired_rank_name}`);


      $('.current').removeClass().addClass(`current ${current_rank_name}`);
      $('.desired').removeClass().addClass(`desired ${desired_rank_name}`);

      $('.total-price #division-boost-price').text(`$${result_with_mark}`);
  
      // From Value
      if ($('.division-boost input[name="game_type"]').val() == 'D') {
        $('.division-boost input[name="current_rank"]').val(current_rank);
        $('.division-boost input[name="desired_rank"]').val(desired_rank);
        $('.division-boost input[name="price"]').val(result_with_mark);
      }
    }
    // Get Result 
    getDivisionPrice();

    // ----------------------------- Premier Boost ---------------------------------
    function getPremierPrice() {
      currentRankName = getRank(currentDivision)[0]
      desiredRankName = getRank(desiredDivision)[0]

      // Server
      const selectedPremierServer = premier_server_select_element.val();

      let [current_mmr_in_c_range, current_range] = getRangeCurrent(currentDivision);
      let [desired_mmr_in_d_range, desired_range] = getRangeDesired(desiredDivision);
      let sliced_prices = full_price_val.slice(current_range, desired_range - 1);
      let sum_current = current_mmr_in_c_range * premierPrices[current_range];
      let sum_desired = desired_mmr_in_d_range * premierPrices[desired_range];
      let clear_res = sliced_prices.reduce((acc, val) => acc + val, 0);
      let price = 0
      if (current_range==desired_range) {
        let range_value = Math.floor((desiredDivision - currentDivision) / 500)
        price = range_value * premierPrices[current_range]
      } else {
        price = sum_current + sum_desired + clear_res
      }

      // Apply extra charges to the result
      price += price * total_Percentage;
    
      // Apply promo code 
      price = setPromoAmount(price, discount_amount)
    
      price = parseFloat(price.toFixed(2));

      // Current Paceit
      $('#current-premier .current-premier-number').html(currentDivision);
      $('.current-premier-selected-info').html(`${currentDivision} Premier Rank`);
      $('.current-premier').removeClass().addClass(`current-premier ${currentRankName}`);
      
      // Desired Premier
      $('#desired-premier .desired-premier-number').html(desiredDivision);
      $('.desired-premier-selected-info').html(`${desiredDivision} Premier Rank`);
      $('.desired-premier').removeClass().addClass(`desired-premier ${desiredRankName}`);
      
      // Price
      $('.total-price #premier-boost-price').text(`$${price}`)

      // Form
      if($('.premier-boost input[name="game_type"]').val() == 'A') {
        $('.premier-boost input[name="current_rank"]').val(currentRank);
        $('.premier-boost input[name="current_division"]').val(currentDivision);
        $('.premier-boost input[name="desired_rank"]').val(desiredRank);
        $('.premier-boost input[name="desired_division"]').val(desiredDivision);
        $('.premier-boost input[name="server"]').val(selectedPremierServer);
        $('.premier-boost input[name="price"]').val(price);
      }
    }
    // Get Result 
    getPremierPrice();
  }

  // Current Rank Change
  radioButtonsCurrent.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      getDivisionPrice();
    });
  });

  // Desired Rank Change
  radioButtonsDesired.forEach(function (radio, index) {
    radio.addEventListener('change', function(){
      getDivisionPrice()
    });
  });

  // Server Changes
  division_server_select_element.addEventListener("change", function(){
    const selectedDivsionServer = division_server_select_element.value;
    $('.division-boost input[name="server"]').val(selectedDivsionServer);
  }); 

  // ----------------------------- Premier Boost ---------------------------------
  // Current Change
  currentPremierRank.on("input", function(event) {
    currentDivision = Number(event.target.value)
    currentRank = getRank(currentDivision)[1]

    // Check Difference
    if((desiredDivision - currentDivision) < 500) {
      let newValue = currentDivision + 500

      if(newValue > 30000){
        newValue = 30000
        currentPremierRank.val(newValue - 500)
        currentDivision = newValue - 500
        currentRank = getRank(currentDivision)[1]
      }

      desiredPremierRank.val(newValue);
      desiredDivision = newValue;
      desiredRank = getRank(desiredDivision)[0];
  
      changeUI(desiredDivision, desiredPremierRank, desiredPremierSteps);
    }

    changeUI(currentDivision, currentPremierRank, currentPremierSteps);

    getPremierPrice()
  })
  
  // Desired Change
  desiredPremierRank.on("input", function(event) {
    desiredDivision = Number(event.target.value);
    desiredRank = getRank(desiredDivision)[1]

    // Check Difference
    if((desiredDivision - currentDivision) < 500) {
      let newValue = currentDivision + 500

      if(newValue > 30000){
        newValue = 30000
        currentPremierRank.val(newValue - 500)
        currentDivision = newValue - 500
        currentRank = getRank(currentDivision)[1]
      }

      desiredPremierRank.val(newValue);
      desiredDivision = newValue;
      desiredRank = getRank(desiredDivision)[0];
  
      changeUI(desiredDivision, desiredPremierRank, desiredPremierSteps);
    }

    if (extend_order && desiredDivision < valuesToSet[4]) {
      desiredPremierRank.val(valuesToSet[4])
      desiredDivision = valuesToSet[4];
      desiredRank = getRank(desiredDivision)[0];
      changeUI(desiredDivision, desiredPremierRank, desiredPremierSteps);
    }

    changeUI(desiredDivision, desiredPremierRank, desiredPremierSteps);

    getPremierPrice()
  })
  
  // Server Changes
  premier_server_select_element.on("change", getPremierPrice);

  // ----------------------------- Faceit Boost ---------------------------------

  const getFaceitPrice = () => {

    let currentLevel = Number(currentFaceitLevel.val())

    let desiredLevel = Number(desiredFaceitLevel.val())

    const selectedFaceitServer = faceit_server_select_element.val();

    const slicedArray = faceitPrices.slice(currentLevel, desiredLevel);
    let price = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

    // Apply extra charges to the result
    price += price * total_Percentage;

    // Apply promo code 
    price = setPromoAmount(price, discount_amount)

    price = parseFloat(price.toFixed(2));

    // Current Faceit
    $('#current-faceit .current-faceit-number').html(currentLevel);
    $('.current-faceit-selected-info').html(`${currentLevel} FACEIT Rank`);
    changeUI(currentLevel, currentFaceitLevel, currentFaceitSteps, 1);

    // Desired Faceit
    $('#desired-faceit .desired-faceit-number').html(desiredLevel);
    $('.desired-faceit-selected-info').html(`${desiredLevel} FACEIT Rank`);
    changeUI(desiredLevel, desiredFaceitLevel, desiredFaceitSteps, 1);

    // Price
    $('.total-price #faceit-boost-price').text(`$${price}`)

    // Form
    if($('.faceit-boost input[name="game_type"]').val() == 'F') {
      $('.faceit-boost input[name="current_level"]').val(currentLevel);
      $('.faceit-boost input[name="desired_level"]').val(desiredLevel);
      $('.faceit-boost input[name="server"]').val(selectedFaceitServer);
      $('.faceit-boost input[name="price"]').val(price);
    }
    
  }

  getFaceitPrice()

  currentFaceitLevel.on("input", getFaceitPrice)
  desiredFaceitLevel.on("input", getFaceitPrice)

  // Server Changes
  faceit_server_select_element.on("change", getFaceitPrice);

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
      getPremierPrice();
      getFaceitPrice();
    }) 
  })

  // Extra Buttons
  extraOptions.forEach(function (checkbox, index) {
    checkbox.addEventListener('change', function () {
      if (this.checked) {
        console.log(this.value)
        console.log(percentege[this.value])
        total_Percentage += percentege[this.value];
        
        $(`input#${this.value}`).val(true)
      } else {
        total_Percentage -= percentege[this.value];
        $(`input#${this.value}`).val(false)
      }
      getDivisionPrice();
      getPremierPrice();
      getFaceitPrice();
    })
  });
  
  promo_form.addEventListener('submit', async function(event) {
    event.preventDefault();
    if(!extend_order) {
      discount_amount = await fetch_promo(); 
      getDivisionPrice();
      getPremierPrice();
      getFaceitPrice();
    }
  });
});
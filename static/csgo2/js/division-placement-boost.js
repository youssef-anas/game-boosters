// Read Values From Json File

let divisionPrices = [0];
let marks_price = [[0, 0, 0, 0, 0]];
let role_price = 0
Promise.all([
  new Promise(function (resolve, reject) {
    $.getJSON('/static/csgo2/data/divisions_data.json', function (data) {
      divisionPrices = divisionPrices.concat(...data);
      resolve();
    });
  }),
]).then(function () {
  // Array For Names 
  const divisionRanks = [
    "Silver I", "Silver II", "Silver III", "Silver IV", "Silver Elite", "SE Master", "Gold NV I", "Gold NV II", "Gold NV III", "Gold NV Master",
    "Master Grd I", "Master Grd II", "Master Grd Elite", "D Master Grd", "Leg Eagle", "Leg Eagle Master", "Supre Master FC", "Global Elite"
    ]


  if(extend_order) {
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
  
    function getDivisionPrice() {
      const desired_rank = getSelectedValueForRadio(radioButtonsDesired)
      const desired_division = getSelectedValueForRadio(radioButtonsDesiredDivision)

      const current_rank = valuesToSet[0];
      const current_division = valuesToSet[1];
      const mark_index = valuesToSet[2];
      
      const current_rank_name = divisionRanks[current_rank];
      const desired_rank_name = divisionRanks[desired_rank];

      makrs_on_current_rank_selected.value = mark_index
      division_server_select_element.value = server
      
      const startRank = ((valuesToSet[3] - 1) * 1) + 1; // 1 = current division
      const endRank = ((desired_rank - 1) * 1) + desired_division-1;
      const slicedArr = sliceArray(divisionPrices, startRank, endRank);
      
      const sum = slicedArr.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

      let result_with_mark = sum
      
      // Apply role extra value
      const total_Percentage_with_role_result = total_Percentage + role_price

      // Apply extra charges to the result
      result_with_mark += result_with_mark * total_Percentage_with_role_result;
      // Apply promo code 
      result_with_mark -= result_with_mark * (discountAmount/100 )
      
      result_with_mark = parseFloat(result_with_mark.toFixed(2)); 

      const currentElement = getSelectedElement(radioButtonsCurrent)
      const desiredElement = getSelectedElement(radioButtonsDesired)

      // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
      $('.division-boost .current-rank-selected-img').attr('src', $(currentElement).data('img'))
      $('.division-boost .desired-rank-selected-img').attr('src', $(desiredElement).data('img'))

      $('.division-boost .desired-selected-info').html(`${desired_rank_name}`)

      $('.current').removeClass().addClass(`current ${current_rank_name}`)
      $('.desired').removeClass().addClass(`desired ${desired_rank_name}`)

      $('.total-price #division-boost-price').text(`$${result_with_mark}`)

      // From Value
      $('.division-boost input[name="current_rank"]').val(current_rank);
      $('.division-boost input[name="marks"]').val(mark_index);
      $('.division-boost input[name="desired_rank"]').val(desired_rank);
      $('.division-boost input[name="price"]').val(result_with_mark);

      // SET PROMO CODE IN FORM
      $('.division-boost input[name="promo_code"]').val(extendPromoCode);
    }
  } else {
    // Get Result Function
    function getDivisionPrice() {

      const current_rank = getSelectedValueForRadio(radioButtonsCurrent);
      const desired_rank = getSelectedValueForRadio(radioButtonsDesired)
      const current_rank_name = divisionRanks[current_rank];
      const desired_rank_name = divisionRanks[desired_rank];

      const startRank = ((current_rank - 1) * 1) + 1;
      const endRank = ((desired_rank - 1) * 1) + 1 - 1;
      const slicedArray = sliceArray(divisionPrices, startRank, endRank);
      let result = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
      let result_with_mark = result
      
      //Apply role percent
      const total_Percentage_with_role_result = total_Percentage + role_price

      // Apply extra charges to the result
      result_with_mark += result_with_mark * total_Percentage_with_role_result;
      // Apply promo code 
      result_with_mark -= result_with_mark * (discount_amount/100 )

      result_with_mark = parseFloat(result_with_mark.toFixed(2)); 
''
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

  // Current Division Change
//   radioButtonsCurrentDivision.forEach(function (radio, index) {
//     radio.addEventListener('change', ()=>{
//       getDivisionPrice()
//     });
//   })

  // Desired Division Change
//   radioButtonsDesiredDivision.forEach(function (radio, index) {
//     radio.addEventListener('change', function(){
//       getDivisionPrice()
//     });
//   });

  // Mark Changes
//   makrs_on_current_rank_selected.addEventListener("change", function(){
//     getDivisionPrice()
//   });

  // Server Changes
  division_server_select_element.addEventListener("change", function(){
    const selectedDivsionServer = division_server_select_element.value;
    $('.division-boost input[name="server"]').val(selectedDivsionServer);
  }); 


  // Get Result 
  getDivisionPrice();
  
  // ----------------------------- Placments Boost ---------------------------------
  const placementsRanks = $('input[name="placement-ranks"]');
  const gameCountInput = $("#game-count");
  const steps = $('.step-indicator .step');
  const gameCounterInitial = Number(gameCountInput.val())
  const initiallyCheckedIndexRank = $('input[name="placement-ranks"]').index($('input[name="placement-ranks"]:checked'));
  const initiallyCheckedRank = $('input[name="placement-ranks"]').eq(initiallyCheckedIndexRank);
  const initiallyCheckedIndexRankPrice = initiallyCheckedRank.data('price');
  const placement_server_select_element = $('.placement-servers-select');
  
  let perviousElement = Array.from(placementsRanks).find(radio => radio.checked);
  
  let pervious_rank = initiallyCheckedIndexRank
  let pervious_rank_name = divisionRanks[pervious_rank]
  let rank_price = initiallyCheckedIndexRankPrice
  let gameCounter = gameCounterInitial
  let selectedPlacementServer = placement_server_select_element.val()
  
  const getPlacementPrice = () => {
    let price = (rank_price * gameCounter);
    // Apply extra charges to the result
    price = price + (price * total_Percentage)
    // Apply promo code 
    price -= price * (discount_amount / 100 )
  
    price = parseFloat(price.toFixed(2))
  
    // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
    $('.placements-boost .pervious-rank-selected-img').attr('src', $(perviousElement).data('img'))
    $('.num-of-match').text(gameCounter);

    $('.placements-boost .pervious-selected-info').html(`${pervious_rank_name}`)
    $('.placements-boost .game_count-selected-info').html(`${gameCounter} Matches`)
  
    $('.pervious').removeClass().addClass(`pervious ${pervious_rank_name}`);

    $('.total-price #placements-boost-price').text(`$${price}`)
  
    const pricee = $('.price-data.placements-boost').eq(0);
    pricee.html(`
    <p class='fs-5 text-uppercase my-4'>Boosting of <span class='fw-bold'>${gameCounter} Placement Games</span></p>
    <h4>$${price}</h4>
    `);
  
    if ($('.placements-boost input[name="game_type"]').val() == 'P') {
      $('.placements-boost input[name="last_rank"]').val(pervious_rank);
      $('.placements-boost input[name="number_of_match"]').val(gameCounter);
      $('.placements-boost input[name="server"]').val(selectedPlacementServer);
      $('.placements-boost input[name="price"]').val(price);
    }
  }

//   getPlacementPrice()
  
  placementsRanks.each(function (index, radio) {
    $(radio).on('change', function () {
      const selectedIndex = placementsRanks.index(radio);
      pervious_rank = selectedIndex;
      pervious_rank_name = divisionRanks[pervious_rank]
      rank_price = $(radio).data('price');

      // Look Here:- When Desired Rank Change Change Value So Image Changed 
      perviousElement = Array.from(placementsRanks).find(radio => radio.checked);

    //   getPlacementPrice()
    });
  });
  
  gameCountInput.on("input", function (event) {
    gameCounter = Number(event.target.value);
    
    const progress = ((gameCounter - 1) / (gameCountInput.prop("max") - 1)) * 100;
  
    gameCountInput.css({
      "background": `linear-gradient(to right, #F36E3F ${progress}%, #251D16 ${progress}%)`
    });
  
    steps.each((step, index) => {
      var $step = $(step);
      if (index < gameCounter) {
        $step.addClass('selected');
      } else {
        $step.removeClass('selected');
      }
    });
  
    // getPlacementPrice()
  
  })

  // Server Changes
  placement_server_select_element.on("change", function() {
    selectedPlacementServer = $(this).val();
    // getPlacementPrice();
  });

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
      getDivisionPrice()
    })
  });
  
  promo_form.addEventListener('submit', async function(event) {
    event.preventDefault();
    if(!extend_order) {
      discount_amount = await fetch_promo(); 
      getDivisionPrice(); 
    }
  });
});
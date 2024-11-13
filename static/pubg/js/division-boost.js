// Read Values From Json File
let divisionPrices = [0];
let marks_price = [[0, 0, 0, 0, 0, 0]];
Promise.all([
  new Promise(function (resolve, reject) {
    $.getJSON('/pubg/get-divisions-data/', function (data) {
      divisionPrices = divisionPrices.concat(...data);
      resolve();
    }).fail(function() {
      reject("Error loading divisions data");
    });
  }),
  new Promise(function (resolve, reject) {
    $.getJSON('/pubg/get-marks-data/', function (data) {
      marks_price = marks_price.concat(data.slice(0));
      resolve();
    }).fail(function() {
      reject("Error loading marks data");
    });
  })
]).then(function () {
  // Array For Names 
  const divisionRanks = ['','bronze', 'silver', 'gold', 'platinum', 'diamond', 'crown', 'ace', 'ace master', 'ace domenater'];
  const divisionNames = [0, 'V', 'IV', 'III', 'II', 'I']


  if(extend_order) {
    $('input[type="radio"]#placements-boost').prop('disabled', true)

    let orderID = parseInt(extend_order, 10);
    document.getElementById('extendOrder').value = orderID; 

    // Set the checked state for each group of radio buttons using the specified order
    setRadioButtonStateWithDisable(radioButtonsCurrent, valuesToSet[0]-1);
    setRadioButtonStateWithDisable(radioButtonsCurrentDivision, valuesToSet[1]-1);
    setRadioButtonState(radioButtonsDesired, valuesToSet[3]-1, true);
    setRadioButtonStateForDesiredDivision(radioButtonsDesiredDivision, valuesToSet[4]-1);
    console.log(valuesToSet)
    selectNthRadioButton(radioButtonsCurrent,valuesToSet[3]-1)
    selectNthRadioButton(radioButtonsCurrentDivision,valuesToSet[4]-1)

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
      const desired_division_name = divisionNames[desired_division];

      makrs_on_current_rank_selected.value = mark_index
      division_server_select_element.value = server
      
      const startRank = ((valuesToSet[3] - 1) * 5) + valuesToSet[4];
      const endRank = ((desired_rank - 1) * 5) + desired_division-1;
      const slicedArr = sliceArray(divisionPrices, startRank, endRank);
      
      const sum = slicedArr.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

      let result_with_mark = sum

      // Apply extra charges to the result
      result_with_mark += result_with_mark * total_Percentage;
      // Apply promo code 
      result_with_mark = setPromoAmount(result_with_mark, discountAmount)
      
      result_with_mark = parseFloat(result_with_mark.toFixed(2)); 

      const currentElement = getSelectedElement(radioButtonsCurrent)
      const desiredElement = getSelectedElement(radioButtonsDesired)

      // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
      $('.division-boost .current-rank-selected-img').attr('src', $(currentElement).data('img'))
      $('.division-boost .desired-rank-selected-img').attr('src', $(desiredElement).data('img'))

      $('.division-boost .current-selected-info').html(`${divisionRanks[valuesToSet[3]]} ${divisionNames[valuesToSet[4]]}`);
      $('.division-boost .desired-selected-info').html(`${desired_rank_name} ${desired_division_name}`)

      $('.current').removeClass().addClass(`current ${current_rank_name}`)
      $('.desired').removeClass().addClass(`desired ${desired_rank_name}`)

      $('.total-price #division-boost-price').text(`$${result_with_mark}`)

      // From Value
      $('.division-boost input[name="current_rank"]').val(current_rank);
      $('.division-boost input[name="current_division"]').val(current_division);
      $('.division-boost input[name="marks"]').val(mark_index);
      $('.division-boost input[name="desired_rank"]').val(desired_rank);
      $('.division-boost input[name="desired_division"]').val(desired_division);
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
      const current_rank_name = divisionRanks[current_rank];
      const desired_rank_name = divisionRanks[desired_rank];
      const current_division_name = divisionNames[current_division];
      const desired_division_name = divisionNames[desired_division];
      let mark_index = -1
      let number_of_mark = 0
      try {
        mark_index = getSelectedValueForDropList(makrs_on_current_rank_selected)
        number_of_mark = marks_price[current_rank][mark_index];
      } catch (error) {
        
      }
            
      const startRank = ((current_rank - 1) * 5) + current_division;
      const endRank = ((desired_rank - 1) * 5) + desired_division - 1;
      const slicedArray = sliceArray(divisionPrices, startRank, endRank);
      let result = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
      let result_with_mark = result
  
      if (result > 0) {
        result_with_mark = result - number_of_mark;
      }
      
      // Apply extra charges to the result
      result_with_mark += result_with_mark * total_Percentage;
      // Apply promo code 
      result_with_mark = setPromoAmount(result_with_mark, discount_amount)

      result_with_mark = parseFloat(result_with_mark.toFixed(2)); 
''
      // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
      const currentElement = getSelectedElement(radioButtonsCurrent)
      const desiredElement = getSelectedElement(radioButtonsDesired)

      // Look Here:- We Change Everything Should Change Depend On Current & Desired Element

      $('.division-boost .current-rank-selected-img').attr('src', $(currentElement).data('img'))
      $('.division-boost .desired-rank-selected-img').attr('src', $(desiredElement).data('img'))

      $('.division-boost .current-selected-info').html(`${current_rank_name} ${current_division_name} ${mark_index == 0 ? '0-20 Points' : mark_index == 1 ? '21-40 Points' : mark_index == 2 ? '41-60 Points' : mark_index == 3 ? '61-80 Points' : mark_index == 4 ? '81-99 Points' : ''}`);
      $('.division-boost .desired-selected-info').html(`${desired_rank_name} ${desired_division_name}`)

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
    radioButtonsCurrentDivision.forEach(function (radio, index) {
      radio.addEventListener('change', ()=>{
        getDivisionPrice()
      });
    })
  
    // Desired Division Change
    radioButtonsDesiredDivision.forEach(function (radio, index) {
      radio.addEventListener('change', function(){
        getDivisionPrice()
      });
    });
  
    // Mark Changes
    makrs_on_current_rank_selected.addEventListener("change", function(){
      getDivisionPrice()
    });
    // Server Changes
    division_server_select_element.addEventListener("change", function(){
      const selectedDivsionServer = division_server_select_element.value;
      $('.division-boost input[name="server"]').val(selectedDivsionServer);
    }); 
  
  
    // Get Result 
    getDivisionPrice();

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
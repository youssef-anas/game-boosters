// Array For Names 
const ranksNames = ['', 'iron', 'bronze', 'silver', 'gold', 'platinum', 'emerald', 'diamond', 'master'];

const divisionNames = [0, 'IV', 'III', 'II', 'I']
// ----------------------------- Division Boost ---------------------------------
// Read Values From Json File
let divisionPrices = [0];
let marks_price = [[0, 0, 0, 0, 0, 0, 0]];
Promise.all([
  new Promise(function (resolve, reject) {
    $.getJSON('/wildRift/divisions-data/', function (data) {
      divisionPrices = divisionPrices.concat(...data);
      resolve();
    });
  }),
  new Promise(function (resolve, reject) {
    $.getJSON('/wildRift/marks-data/', function (data) {
      marks_price = marks_price.concat(data.slice(0));
      resolve();
    });
  })
]).then(function () {

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

      const startt = ((valuesToSet[3] - 1) * 4) + valuesToSet[4];
      const endd = ((desired_rank - 1) * 4) + desired_division-1;
      const slicedArray = sliceArray(divisionPrices, startt, endd);
      const summ = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

      let result_with_mark = summ

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
      $('.current-rank-selected-img:not(.checkout-img)').attr('src', $(currentElement).data('img'))
      $('.current-rank-selected-img.checkout-img').attr('src', $(oldDeiredElement).data('img'))

      $('.desired-rank-selected-img').attr('src', $(desiredElement).data('img'))

      $('.current-selected-info').html(`${ranksNames[valuesToSet[3]]} ${divisionNames[valuesToSet[4]]}`);
      $('.desired-selected-info').html(`${desired_rank_name} ${desired_rank == 8 ? desired_division_name : ''}`)

      $('.current').removeClass().addClass(`current ${current_rank_name}`)
      $('.desired').removeClass().addClass(`desired ${desired_rank_name}`)

      $('.total-price #price').text(`$${result_with_mark}`)

      // From Value
      $('input[name="current_rank"]').val(current_rank);
      $('input[name="current_division"]').val(current_division);
      $('input[name="marks"]').val(mark_index);
      $('input[name="desired_rank"]').val(desired_rank);
      $('input[name="desired_division"]').val(desired_division);
      $('input[name="server"]').val(selectedDivsionServer);
      $('input[name="price"]').val(result_with_mark);

      // SET PROMO CODE IN FORM
      $('input[name="promo_code"]').val(extendPromoCode);
    }
  }
  else {
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

      setMarkNumber(current_rank)

      const selectedDivsionServer = division_server_select_element.value;

      const startt = ((current_rank - 1) * 4) + current_division;
      const endd = ((desired_rank - 1) * 4) + desired_division-1;
      const slicedArray = sliceArray(divisionPrices, startt, endd);
      const summ = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

      let result_with_mark = summ

      if (summ !== 0) {
        result_with_mark = summ - number_of_mark;
      }

      // Apply extra charges to the result
      result_with_mark += result_with_mark * total_Percentage;
      // Apply promo code 
      result_with_mark = setPromoAmount(result_with_mark, discount_amount)
      
      result_with_mark = parseFloat(result_with_mark.toFixed(2));

      // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
      const currentElement = getSelectedElement(radioButtonsCurrent)
      const desiredElement = getSelectedElement(radioButtonsDesired)
      
      $('.current-rank-selected-img').attr('src', $(currentElement).data('img'))
      $('.desired-rank-selected-img').attr('src', $(desiredElement).data('img'))

      $('.current-selected-info').html(`${current_rank_name} ${current_division_name} ${mark_index} Marks`);
      $('.desired-selected-info').html(`${desired_rank_name} ${desired_rank != 8 ? desired_division_name : ''}`)

      $('.current').removeClass().addClass(`current ${current_rank_name}`)
      $('.desired').removeClass().addClass(`desired ${desired_rank_name}`)

      $('.total-price #price').text(`$${result_with_mark}`)

      // From Value
      $('input[name="current_rank"]').val(current_rank);
      $('input[name="current_division"]').val(current_division);
      $('input[name="marks"]').val(mark_index);
      $('input[name="desired_rank"]').val(desired_rank);
      $('input[name="desired_division"]').val(desired_division);
      if (desired_rank == 8){
        $('input[name=desired_division]').val(1)
      }
      $('input[name="server"]').val(selectedDivsionServer);
      $('input[name="price"]').val(result_with_mark);
    }
  }

  // Get Result
  getResult();

  // Change Marks
  function setMarkNumber(current_rank) {
    let number_of_marks = -1; // num of marks
    switch (current_rank) {
      case 1:
        number_of_marks = 2;
        break;
      case 2:
      case 3:
        number_of_marks = 3;
        break;
      case 4:
      case 5:
        number_of_marks = 4;
        break;
      case 6:
        number_of_marks = 5;
        break;
      case 7:
        number_of_marks = -1;
        break;
      default:
        number_of_marks = -1;
    }
    makrs_on_current_rank.forEach(function (element, index) {
      if (number_of_marks == -1) {
        $('.current-mark-container').addClass('d-none')
      }
      else {
        $('.current-mark-container').removeClass('d-none')
        if (index <= number_of_marks) {
          element.classList.remove('d-none');
        } else {
          element.classList.add('d-none');
        }
      }
    });

  }

  // Current Rank Change
  radioButtonsCurrent.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      makrs_on_current_rank_selected.value = 0; // make 0 mark is check
      getResult();
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
        let desired_division_IV = document.getElementById("desired-division0")
        desired_division_IV.checked = true; 
        desired_division_IV.setAttribute("checked", "checked");
      }
      else {
        desired_division_to_hide.style.visibility = "visible";
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
  division_server_select_element.addEventListener("change", getResult);

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
    })
  });
 
  promo_form.addEventListener('submit', async function(event) {
    event.preventDefault();
    if(!extend_order) {
      discount_amount = await fetch_promo(); 
      getResult();
    }
  });

});
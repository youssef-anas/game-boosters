// Disable Functions
function setRadioButtonStateWithDisable(radioButtons, values) {
radioButtons.forEach((radio, index) => {
    // Assuming values in the specified order correspond to radio button indices
    radio.checked = (index === values);
    radio.disabled = true;
});
}

function selectNthRadioButton(radioButtons, number) {
    if (number >= 0 && number < radioButtons.length) {
        radioButtons[number].checked = true;
    } else {
        console.error("Invalid number provided or radio button does not exist.");
    }
}


function setRadioButtonState(radioButtons, values) {
radioButtons.forEach((radio, index) => {
    radio.checked = (index === values);
    if (index<values){
    radio.disabled = true;
    }
});
}
function setRadioButtonStateForDesiredDivision(radioButtons, values) {
radioButtons.forEach((radio, index) => {
    radio.checked = (index === values);
});
}

// Slice Function
function sliceArray(array, start, end) {
    return array.slice(start, end + 1);
}
  

function getSelectedValueForRadio(radioButton) {
    value = Array.from(radioButton).findIndex(radio => radio.checked);
    return value +1;
}

function getSelectedValueForDropList(selectElement) {
    let selectedOption = selectElement.options[selectElement.selectedIndex];
    let selectedIndex = Array.from(selectElement.options).indexOf(selectedOption);
    return selectedIndex;
}

function getSelectedElement(radioButton) {
    element = Array.from(radioButton).find(radio => radio.checked);
    return element;
}


function getDivisionIconsMobilLegends(rank) {
    let rank_icons = 5;
    switch (rank) {
      case 1:
        rank_icons = 3;
        break;
      case 2:
      case 3:
        rank_icons = 4;
        break;
      default:
        rank_icons = 5;
    }
    return rank_icons;
  }

  function getMarksIconsMobilLegends(rank) {
    let rank_icons = 5;
    switch (rank) {
      case 1:
      case 2:  
        rank_icons = 3;
        break;
      case 3:
        rank_icons = 4;
        break;
      case 4:
      case 5:
      case 6:
        rank_icons = 5;
        break;
      case 7:
      case 8:
      case 9:
        rank_icons = 0;
        break;
      default:
        rank_icons = 5;
    }
    return rank_icons;
    
  }

function refreshDivisionBasedRankMobileLegends(selectedRank, currentDivison){
    let labels
    let divisionIconsNumber
    divisionIconsNumber = getDivisionIconsMobilLegends(selectedRank);
    if (currentDivison){
        const divisionContainer = document.querySelector('.current-dcontainer');
        labels = divisionContainer.querySelectorAll('label');
        const current_divisionIII = document.getElementById('current-division2');
        const current_divisionII = document.getElementById('current-division1');
        if (selectedRank === 1){
            current_divisionIII.checked = true;
        }
        if (selectedRank === 2 || selectedRank === 3){
            current_divisionII.checked = true;
        }
    }
    else{
        const divisionContainer = document.querySelector('.desired-dcontainer');
        labels = divisionContainer.querySelectorAll('label');
        const desired_divisionIII = document.getElementById('desired-division2');
        const desired_divisionII = document.getElementById('desired-division1');
        if (selectedRank === 1){
            desired_divisionIII.checked = true;
        }
        if (selectedRank === 2 || selectedRank === 3){
              desired_divisionII.checked = true;
        }
    }
    labels.forEach((label, index) => {
        if (index < 5-divisionIconsNumber) {
        label.classList.add('d-none');
        } else {
        label.classList.remove('d-none');
        }
    });
}
function refreshMarksBasedRankMobileLegends(current_rank){
    const markContainer = document.querySelector('.current-marks-select');
    const containerOfmarkContainer = document.querySelector('.current-mark-container')
    markContainer.innerHTML = '';
    const numberOfMarks = getMarksIconsMobilLegends(current_rank)
    for (let i = 1; i <= numberOfMarks; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = `${i} Star`;
        markContainer.appendChild(option);
        if (i === 1) {
            option.setAttribute('selected', 'selected');
        }
    };
    if ([7, 8, 9].includes(current_rank)) {
        containerOfmarkContainer.classList.add('d-none');
    } else {
        containerOfmarkContainer.classList.remove('d-none');
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Check if the cookie name matches the CSRF cookie name
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
}


// Function to fetch promo data
async function fetch_promo() {
  return new Promise((resolve, reject) => {
    const promo_form = document.querySelector('.discount #promo-form');
    const discountInput = document.querySelector('input[name="discount"]');
    const discountCode = discountInput.value.trim();
    const promoDetails = $('#promo-details');
    const applyFormInput = document.getElementById('promo-form-submit')
    applyFormInput.disabled = true;
    $('input[id="promo_send"]').val(discountCode);
    if (discountCode) {
      applyFormInput.value = 'Please Wait...';
      const csrfToken = getCookie('csrftoken');
      $.ajax({
          url: '/accounts/promo-codes/',
          type: 'POST',
          headers: {
            'X-CSRFToken': csrfToken
          },
          contentType: 'application/json',
          data: JSON.stringify({ code: discountCode }),
          success: function(data) {
            promo_form.classList.add('d-none');
            promoDetails.css('visibility', 'visible');
            promoDetails.text(`%${data.discount_amount} Discount applied successfully \uD83C\uDF89`);
            promoDetails.addClass('success-message');
            promoDetails.removeClass('error-message');
            applyFormInput.value = 'Apply';
            applyFormInput.disabled = false;
            if (data.is_percent){
              resolve(data.discount_amount / 100);
            }else{
              resolve(data.discount_amount);
            }

          },
          error: function(xhr, textStatus, errorThrown) {
            promoDetails.css('visibility', 'visible');
            promoDetails.text(`${xhr.responseJSON.error} \uD83D\uDE1E`);
            promoDetails.removeClass('success-message');
            promoDetails.addClass('error-message');
            applyFormInput.value = 'Apply';
            applyFormInput.disabled = false;
            resolve(0); // Reject the promise when there's an error
          }
      });
    } else {
      $('input[id="promo_send"]').val('null');
      promoDetails.css('visibility', 'visible');
      promoDetails.text('Please enter a discount code \uD83D\uDE1E');
      promoDetails.removeClass('success-message');
      promoDetails.addClass('error-message');
      applyFormInput.value = 'Apply';
      applyFormInput.disabled = false;
      resolve(0); // Resolve the promise with null if there's no discount code
    }
  });
}


const setPromoAmount = (price, amount)=> {
  if (amount > 0 && amount < 1){
    return price -= price * amount
  }else if (amount > 1){
    return price - amount
  }else{
    return price
  }
}

const MadBoostInputAndRange = (input_div, range_div, action) => {
  if (!input_div){
      console.error(`error in the Number input Not found `);
  }

  if (!range_div){
      console.error(`error in the Range input Not found `);
  }

  const max_value = parseInt(input_div.getAttribute('max'), 10);
  const min_value = parseInt(input_div.getAttribute('min'), 10);

  const changer = (strValue) => {
      let value = parseInt(strValue, 10);
      if (isNaN(value)) {
          value = min_value;
      }
      if  ((value) > max_value){
          value = max_value;
      }
      else if ((value) < min_value) {
          value = min_value;
      }
      input_div.value = value;
      range_div.value = value;
      action();
  };

  input_div.addEventListener('input', ()=> {
      changer(input_div.value);
  });

  range_div.addEventListener('input', ()=> {
      changer(range_div.value);
  });
  action();
}


function getFirstTwoWords(name) {
  const words = name.split('-');
  return words.length >= 3 ? `${words[0]}-${words[1]}` : words[0];
}

// wow game set post method
const setBoostMethod = (method, action) => {

  const method_name = `boost-method-${method}`
  const boostMetods = document.getElementsByName(method_name);
  boostMetods.forEach(function (radio) {
    radio.addEventListener('change', function () {
      const boost_val = getFirstTwoWords(radio.id);
      const inputs = document.querySelectorAll(`input[class^="${method_name}"]`);
      // Set the value for each matching input element
      inputs.forEach(input => {
        input.value = boost_val;
      });
      action();

      const method_info = document.getElementById(`${method}-method-info`);
      if (method_info){
        method_info.innerHTML = getFirstTwoWords(radio.id);
      }
    })
  }) 
}

// wow
// Function to find and check the first checkbox in a container
function checkFirstCheckbox(container) {
  // Find all checkboxes within the container
  const checkboxes = container.querySelectorAll('input[type="checkbox"]');
  
  // Iterate through checkboxes to find the first one and check it
  for (let i = 0; i < checkboxes.length; i++) {
      if (i === 0) {
          checkboxes[i].checked = true;
      }
  }
}

// wow
const getImgPathFromUrl=(backgroundImage)=> {
  // extract path from backgroundImage
  const path = backgroundImage.match(/url\((.*)\)/)[1];
  // replace &quot; with "
  const newPath = path.replace(/&quot;/g, '"');
  // replace url(" with ""
  const newPath2 = newPath.replace(/url\((.*)\)/, '$1');
  // replace " with ""
  const newPath3 = newPath2.replace(/"/g, '');
  // replace ' with ""
  const newPath4 = newPath3.replace(/'/g, '');
  return newPath4
}

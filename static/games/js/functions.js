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
            resolve(data.discount_amount); // Resolve the promise with data when the request is successful
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
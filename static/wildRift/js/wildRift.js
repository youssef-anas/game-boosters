document.addEventListener("DOMContentLoaded", function () {
  const radioButtonsCurrent = document.querySelectorAll('input[name="radio-group-current"]');
  const radioButtonsDesired = document.querySelectorAll('input[name="radio-group-desired"]');
  const radioButtonsCurrentDivision = document.querySelectorAll('input[name="radio-group-current-division"]');
  const radioButtonsDesiredDivision = document.querySelectorAll('input[name="radio-group-desired-division"]');

  // Find the initially checked radio button and log its index
  // Changesss -------- Check It Shehhhhhhhhhhabbbbbbbbbbb
  const initiallyCheckedElementCurrent = Array.from(radioButtonsCurrent).find(radio => radio.checked);
  const initiallyCheckedElementDesired = Array.from(radioButtonsDesired).find(radio => radio.checked);

  let initiallyCheckedNameCurrent = null;
  let initiallyCheckedNameDesired = null;
  let initiallyCheckedIndexCurrent = -1;
  let initiallyCheckedIndexDesired = -1;

  if (initiallyCheckedElementCurrent) {
    initiallyCheckedNameCurrent = initiallyCheckedElementCurrent.getAttribute('data-name');
    initiallyCheckedIndexCurrent = initiallyCheckedElementCurrent.getAttribute('data-id');
  }
  if (initiallyCheckedElementDesired) {
    initiallyCheckedNameDesired = initiallyCheckedElementDesired.getAttribute('data-name');
    initiallyCheckedIndexDesired = initiallyCheckedElementDesired.getAttribute('data-id');
  }

  // -----------------------------------------------
  const initiallyCheckedElementCurrentDivision = Array.from(radioButtonsCurrentDivision).find(radio => radio.checked);
  const initiallyCheckedElementDesiredDivision = Array.from(radioButtonsDesiredDivision).find(radio => radio.checked);

  let initiallyCheckedNameCurrentDivision = null;
  let initiallyCheckedNameDesiredDivision = null;
  let initiallyCheckedIndexCurrentDivision = -1;
  let initiallyCheckedIndexDesiredDivision = -1;

  if (initiallyCheckedElementCurrentDivision) {
    initiallyCheckedNameCurrentDivision = initiallyCheckedElementCurrentDivision.getAttribute('data-name');
    console.log(initiallyCheckedNameCurrentDivision)
    initiallyCheckedIndexCurrentDivision = initiallyCheckedElementCurrentDivision.getAttribute('data-id');
  }
  if (initiallyCheckedElementDesiredDivision) {
    initiallyCheckedNameDesiredDivision = initiallyCheckedElementDesiredDivision.getAttribute('data-name');
    initiallyCheckedIndexDesiredDivision = initiallyCheckedElementDesiredDivision.getAttribute('data-id');
  }

  // End Change Here

  if (initiallyCheckedIndexCurrent !== -1 && initiallyCheckedIndexDesired !== -1 && initiallyCheckedIndexCurrentDivision !== -1
    && initiallyCheckedIndexDesiredDivision !== -1) {
    console.log('Initially checked index For Current:', initiallyCheckedIndexCurrent);
    console.log('Initially checked index For Desired:', initiallyCheckedIndexDesired);
    console.log('Initially checked index For CurrentDivision :', initiallyCheckedIndexCurrentDivision);
    console.log('Initially checked index For CurrentDivision:', initiallyCheckedIndexDesiredDivision);
  } else {
    console.log('No radio buttons is initially checked.');
  }

  function sliceArray(array, start, end) {
    return array.slice(start, end + 1);
  }


  // --------------------->  Sarah Mohamed  (:
  // --------> 
  // -------->
  // pls add real price here in this list , but dont remove 0 number 
  // const divisionPrices [0, listed list of price from iron IV to master  -- listed listed listed **** listed and try (: ]
  // const divisionPrices = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29];
  // const prices = [0];
  let divisionPrices = [0];
  $.getJSON('/static/wildRift/data/divisions_data.json', function (data) {
    console.log(data)
    divisionPrices = divisionPrices.concat(...data);

    console.log("data", divisionPrices);

    getResult();
  });


  var current_rank = initiallyCheckedIndexCurrent;
  var desired_rank = initiallyCheckedIndexDesired;
  var current_division = initiallyCheckedIndexCurrentDivision;
  var desired_division = initiallyCheckedIndexDesiredDivision;
  var current_division_name = initiallyCheckedNameCurrentDivision;
  var desired_division_name = initiallyCheckedNameDesiredDivision;
  var current_rank_name = initiallyCheckedNameCurrent
  var desired_rank_name = initiallyCheckedNameDesired


  // Here Simple Change --- Shehhhhhhhhhab
  function getResult() {
    const startt = ((Number(current_rank) - 1) * 4) + 1 + Number(current_division);
    const endd = ((Number(desired_rank) - 1) * 4) + Number(desired_division);
    const slicedArray = sliceArray(divisionPrices, startt, endd);
    console.log('Start', startt)
    console.log('End', endd)
    console.log('divisionPrices', divisionPrices)
    console.log('slicedArray', slicedArray);
    const summ = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
    const pricee = document.getElementsByClassName('price-data')[0];
    console.log(pricee)
    // !Imporrrrrrtant ---- Here I Want You Add Make Number That Choices Instead Of 0 (Mark 0)
    pricee.innerHTML = `
      <p class='fs-5 text-uppercase my-4'>Boosting <span class='fw-bold'>From ${current_rank_name} ${current_division_name} Marks 0 to ${desired_rank_name} ${desired_division_name} </span></p>
      <h4>$${summ}</h4>
    `;
    console.log(summ);
  }
  getResult();

  // Add change event listener to log the index when a radio button is changed
  // Changesss -------- Check It Shehhhhhhhhhhabbbbbbbbbbb to End
  radioButtonsCurrent.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedElement = Array.from(radioButtonsCurrent).find(radio => radio.checked);
      if (selectedElement) {
        const dataIdValue = selectedElement.getAttribute('data-id');
        const dataNameValue = selectedElement.getAttribute('data-name');
        console.log('Selected data-id value:', dataIdValue);

        current_rank = dataIdValue;
        current_rank_name = dataNameValue
        getResult();
      } else {
        console.log('No radio button is selected.');
      }
      console.log('current_rank', current_rank)
      console.log('current_rank_name', current_rank_name)

      const currentMarks = $(this).data("mark");
      $('.current-marks').empty();
      if (currentMarks) {
        for (let i = 0; i <= currentMarks; i++) {
          $(".current-marks").append(`
          <input type="radio" id="current-mark${i}" name="radio-group-current-mark" class="current-mark px-3 py-2 mb-3 border border-1 bg-light text-dark me-2 rounded-3 text-decoration-none" data-mark="${i}">
          <label for="current-mark${i}" class="me-2 mt-3 py-2 px-4">${i} Mark</label>
        `);
        }
      }

      getResult()
    });
  });

  radioButtonsDesired.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedElement = Array.from(radioButtonsDesired).find(radio => radio.checked);
      if (selectedElement) {
        const dataIdValue = selectedElement.getAttribute('data-id');
        const dataNameValue = selectedElement.getAttribute('data-name');
        console.log('Selected data-id value:', dataIdValue);

        desired_rank = dataIdValue;
        desired_rank_name = dataNameValue
        getResult();
      } else {
        console.log('No radio button is selected.');
      }
      console.log('desired_rank', desired_rank)
      console.log('desired_rank_name', desired_rank_name)
      const desired_division_to_hide = document.getElementById('desired-division');
      if (desired_rank == 8) {
        desired_division_to_hide.classList.add('d-none');
      }
      else {
        desired_division_to_hide.classList.remove('d-none');
      }
      getResult();
    });
  });

  radioButtonsCurrentDivision.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedElement = Array.from(radioButtonsCurrentDivision).find(radio => radio.checked);

      if (selectedElement) {
        const dataIdValue = selectedElement.getAttribute('data-id');
        const dataNameValue = selectedElement.getAttribute('data-name');
        console.log('Selected data-id value for Current Division:', dataIdValue);

        current_division = dataIdValue;
        current_division_name = dataNameValue
        getResult();
      } else {
        console.log('No radio button for Current Division is selected.');
      }

      getResult();
    });
  });

  radioButtonsDesiredDivision.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedElement = Array.from(radioButtonsDesiredDivision).find(radio => radio.checked);

      if (selectedElement) {
        const dataIdValue = selectedElement.getAttribute('data-id');
        const dataNameValue = selectedElement.getAttribute('data-name');
        console.log('Selected data-id value for Current Division:', dataIdValue);

        desired_division = dataIdValue;
        desired_division_name = dataNameValue
        getResult();
      } else {
        console.log('No radio button for Current Division is selected.');
      }
      getResult()
    });
  });
});

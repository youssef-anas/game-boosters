document.addEventListener("DOMContentLoaded", function () {
  const radioButtonsCurrent = document.querySelectorAll('input[name="radio-group-current"]');
  const radioButtonsDesired = document.querySelectorAll('input[name="radio-group-desired"]');
  const radioButtonsCurrentDivision = document.querySelectorAll('input[name="radio-group-current-division"]');
  const radioButtonsDesiredDivision = document.querySelectorAll('input[name="radio-group-desired-division"]');

  const initiallyCheckedIndexCurrent = Array.from(radioButtonsCurrent).findIndex(radio => radio.checked)+1;
  const initiallyCheckedIndexDesired  = Array.from(radioButtonsDesired).findIndex(radio => radio.checked)+1;

  const initiallyCheckedIndexCurrentDivision  = Array.from(radioButtonsCurrentDivision).findIndex(radio => radio.checked)+1;
  const initiallyCheckedIndexDesiredDivision  = Array.from(radioButtonsDesiredDivision).findIndex(radio => radio.checked)+1;

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
  const divisionRanks = [null,'iron','bronze','silver','gold','platinum','emerald','diamond','master'];

  const divisionNames = [0, 'IV', 'III', 'II', 'I']


  var current_rank = initiallyCheckedIndexCurrent;
  console.log('hi',initiallyCheckedIndexCurrent)
  var desired_rank = initiallyCheckedIndexDesired;
  var current_division = initiallyCheckedIndexCurrentDivision;
  var desired_division = initiallyCheckedIndexDesiredDivision;
  var current_rank_name = divisionRanks[initiallyCheckedIndexCurrent];
  var desired_rank_name = divisionRanks[initiallyCheckedIndexDesired];
  var current_division_name = divisionNames[initiallyCheckedIndexCurrentDivision];
  var desired_division_name = divisionNames[initiallyCheckedIndexDesiredDivision];


  function getResult() {
    const startt = ((current_rank-1)*4)+1 + current_division;
    const endd = ((desired_rank-1)*4) + desired_division;
    const slicedArray = sliceArray(divisionPrices, startt, endd);
    console.log('Start', startt)
    console.log('End', endd)
    console.log('divisionPrices', divisionPrices)
    console.log('slicedArray', slicedArray);
    const summ = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
    const pricee = document.getElementsByClassName('price-data')[0];
    console.log(pricee)
    pricee.innerHTML = `
      <p class='fs-5 text-uppercase my-4'>Boosting <span class='fw-bold'>From ${current_rank_name} ${current_division_name} Marks 0 to ${desired_rank_name} ${desired_rank_name != 'master' ? desired_division_name : ''} </span></p>
      <h4>$${summ}</h4>
    `;
    console.log(summ);
  }
  getResult();
  radioButtonsCurrent.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtonsCurrent).indexOf(radio);
      console.log('Selected index:', selectedIndex+1);
      current_rank = selectedIndex+1;
      current_rank_name = divisionRanks[current_rank]
      console.log('current_rank', current_rank)

      const currentMarks = this.getAttribute('data-mark');
      console.log('cu',currentMarks)
      const current_marks_to_hide =  document.querySelectorAll('div.current-mark-container');
      console.log('current_marks_to_hide',current_marks_to_hide)
      current_marks_to_hide.forEach(function (currentMark, index) {
        if(currentMarks) {
          if (Number(currentMark.getAttribute('data-mark')) > Number(currentMarks)) {
            currentMark.classList.add('d-none');
          } else {
            currentMark.classList.remove('d-none');
          }
        } else {
          currentMark.classList.add('d-none');
        }
      })
      // $('.current-marks').empty();
      // if (currentMarks) {
      //   for (let i = 0; i <= currentMarks; i++) {
      //     $(".current-marks").append(`
      //     <input type="radio" id="current-mark${i}" name="radio-group-current-mark" class="current-mark px-3 py-2 mb-3 border border-1 bg-light text-dark me-2 rounded-3 text-decoration-none" data-mark="${i}">
      //     <label for="current-mark${i}" class="me-2 mt-3 py-2 px-4">${i} Mark</label>
      //   `);
      //   }
      // }

      getResult()
    });
  });

  radioButtonsDesired.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtonsDesired).indexOf(radio);
      console.log('Selected index:', selectedIndex+1);
      desired_rank = selectedIndex+1;
      desired_rank_name = divisionRanks[desired_rank]
      const desired_division_to_hide =  document.getElementById('desired-division');
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
      const selectedIndex = Array.from(radioButtonsCurrentDivision).indexOf(radio);
      console.log('Selected Division index:', selectedIndex+1);
      current_division = selectedIndex+1;
      current_division_name = divisionNames[current_division]
      getResult();
    });
  });

  radioButtonsDesiredDivision.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtonsDesiredDivision).indexOf(radio);
      console.log('Selected Division index:', selectedIndex+1);
      desired_division = selectedIndex+1;
      desired_division_name = divisionNames[desired_division]
      getResult()
    });
  });
});

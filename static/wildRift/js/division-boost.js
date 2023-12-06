document.addEventListener("DOMContentLoaded", function () {
  const radioButtonsCurrent = document.querySelectorAll('input[name="radio-group-current"]');
  const radioButtonsDesired = document.querySelectorAll('input[name="radio-group-desired"]');
  const radioButtonsCurrentDivision = document.querySelectorAll('input[name="radio-group-current-division"]');
  const radioButtonsDesiredDivision = document.querySelectorAll('input[name="radio-group-desired-division"]');
  const makrs_on_current_rank = document.querySelectorAll('.current-mark-container');
  const makrs_on_current_rank_checked = document.querySelectorAll('input[name="radio-group-current-mark"]');

  const initiallyCheckedIndexCurrent = Array.from(radioButtonsCurrent).findIndex(radio => radio.checked) + 1;
  const initiallyCheckedIndexDesired = Array.from(radioButtonsDesired).findIndex(radio => radio.checked) + 1;

  const initiallyCheckedIndexCurrentDivision = Array.from(radioButtonsCurrentDivision).findIndex(radio => radio.checked) + 1;
  const initiallyCheckedIndexDesiredDivision = Array.from(radioButtonsDesiredDivision).findIndex(radio => radio.checked) + 1;
  const initiallyCheckedIndexMark = Array.from(makrs_on_current_rank_checked).findIndex(radio => radio.checked);

  // if (initiallyCheckedIndexCurrent !== -1 && initiallyCheckedIndexDesired !== -1 && initiallyCheckedIndexCurrentDivision !== -1
  //   && initiallyCheckedIndexDesiredDivision !== -1) {
  //   console.log('Initially checked index For Current:', initiallyCheckedIndexCurrent);
  //   console.log('Initially checked index For Desired:', initiallyCheckedIndexDesired);
  //   console.log('Initially checked index For CurrentDivision :', initiallyCheckedIndexCurrentDivision);
  //   console.log('Initially checked index For CurrentDivision:', initiallyCheckedIndexDesiredDivision);
  // } else {
  //   console.log('No radio buttons is initially checked.');
  // }

  function sliceArray(array, start, end) {
    return array.slice(start, end + 1);
  }

  let divisionPrices = [0];
  let marks_price = [[0, 0, 0, 0, 0, 0]];
  Promise.all([
    new Promise(function (resolve, reject) {
      $.getJSON('/static/wildRift/data/divisions_data.json', function (data) {
        divisionPrices = divisionPrices.concat(...data);
        resolve();
        console.log('List',divisionPrices)
      });
    }),
    new Promise(function (resolve, reject) {
      $.getJSON('/static/wildRift/data/marks_data.json', function (data) {
        marks_price = marks_price.concat(data.slice(0));
        console.log('mark price', marks_price);
        resolve();
      });
    })
  ]).then(function () {
console.log('sara is hereeeeeeeeeeeeeeeeeeeee')
    const divisionRanks = ['', 'iron', 'bronze', 'silver', 'gold', 'platinum', 'emerald', 'diamond', 'master'];

    const divisionNames = [0, 'IV', 'III', 'II', 'I']

    var current_rank = initiallyCheckedIndexCurrent;
    var desired_rank = initiallyCheckedIndexDesired;
    var current_division = initiallyCheckedIndexCurrentDivision;
    var desired_division = initiallyCheckedIndexDesiredDivision;
    var current_rank_name = divisionRanks[initiallyCheckedIndexCurrent];
    var desired_rank_name = divisionRanks[initiallyCheckedIndexDesired];
    var current_division_name = divisionNames[initiallyCheckedIndexCurrentDivision];
    var desired_division_name = divisionNames[initiallyCheckedIndexDesiredDivision];
    var number_of_mark = marks_price[current_rank][initiallyCheckedIndexMark];

    $.getJSON('/static/wildRift/data/marks_data.json', function (data) {
      marks_price = marks_price.concat(data.slice(1));
      console.log('hi', marks_price)
      number_of_mark = marks_price[current_rank][initiallyCheckedIndexMark];
      getResult();
    });

console.log("initail mark price = ", number_of_mark)


    let total_Percentage = 0;

    // ################################ Extra Charges Part #################################################
    const buttons = {
      duoBoosting: document.querySelector('#duoBoostingButton'),
      selectBooster: document.querySelector('#selectBoosterButton'),
      turboBoost: document.querySelector('#turboBoostButton'),
      streaming: document.querySelector('#streamingButton'),
    };

    const contents = {
      duoBoosting: document.querySelector('.duoBoostingContent'),
      selectBooster: document.querySelector('.selectBoosterContent'),
      turboBoost: document.querySelector('.turboBoostContent'),
      streaming: document.querySelector('.streamingContent'),
    };

    const Applybuttons = {
      duoBoosting: document.querySelector('#duoBoostingApplyButton'),
      selectBooster: document.querySelector('#selectBoosterApplyButton'),
      turboBoost: document.querySelector('#turboBoostApplyButton'),
      streaming: document.querySelector('#streamingApplyButton'),
    };

    // Toggle Function
    function toggleContent(content) {
      for (const key in contents) {
        contents[key].style.display = key === content && contents[key].style.display !== 'block' ? 'block' : 'none';
      }
    }

    // Toggle click event
    function setupButtonClickEvent(button, content) {
      button.addEventListener('click', function () {
        toggleContent(content);
      });
    }

    function updateTotalPercentage(percentage, add = true, button) {
      buttonOldName = buttons[button].innerHTML
      if (add) {
        total_Percentage += percentage;
        buttons[button].innerHTML = '<i class="fa-solid fa-check"></i>' + buttonOldName;
        Applybuttons[button].innerHTML = 'Cancel'
        Applybuttons[button].classList.remove('applyButton');
        Applybuttons[button].classList.add('cancelButton');
      } else {
        total_Percentage -= percentage;
        buttons[button].innerHTML = buttonOldName.replace('<i class="fa-solid fa-check"></i>', '');
        Applybuttons[button].innerHTML = 'Apply'
        Applybuttons[button].classList.remove('cancelButton');
        Applybuttons[button].classList.add('applyButton');
      }

      console.log(total_Percentage)
    }

    // Apply Button
    function setupApplyButtonClickEvent(button, percentage) {
      Applybuttons[button].addEventListener('click', function () {
        updateTotalPercentage(percentage, !Applybuttons[button].classList.contains('cancelButton'), button);
        getResult();
      });
    }

    // Setup click events for each button
    for (const key in buttons) {
      setupButtonClickEvent(buttons[key], key);
    }
    setupApplyButtonClickEvent('duoBoosting', 0.65);
    setupApplyButtonClickEvent('selectBooster', 0.05);
    setupApplyButtonClickEvent('turboBoost', 0.20);
    setupApplyButtonClickEvent('streaming', 0.15);

    function getResult() {
      const startt = ((current_rank - 1) * 4) + current_division;
      const endd = ((desired_rank - 1) * 4) + desired_division-1;
      const slicedArray = sliceArray(divisionPrices, startt, endd);
      console.log('Start', startt)
      console.log('End', endd)
      // console.log('divisionPrices', divisionPrices)
      console.log('slicedArray', slicedArray);
      const summ = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

      let result_with_mark = summ

      if (summ !== 0) {
        result_with_mark = summ - number_of_mark;
      }

      // Apply extra charges to the result
      result_with_mark += result_with_mark * total_Percentage;
      result_with_mark = parseFloat(result_with_mark.toFixed(2)); 

      const pricee = document.querySelector('.price-data.division-boost');
      console.log('priceeeeeeeeeeeeee', pricee)
      pricee.innerHTML = `
      <p class='fs-5 text-uppercase my-4'>Boosting <span class='fw-bold'>From ${current_rank_name} ${current_division_name} Marks 0 to ${desired_rank_name} ${desired_rank_name != 'master' ? desired_division_name : ''} </span></p>
      <span class='fs-5 text-uppercase fw-bold'>Total Cost: $${result_with_mark}</span>
    `;
    }
    getResult();


    function setMarkNumber() {
      let number_of_marks = -1; // num of marks
      makrs_on_current_rank_checked[0].checked = true; // make 0 mark is check
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
        if (index <= number_of_marks) {
          element.classList.remove('d-none');
        } else {
          element.classList.add('d-none');
        }
      });

    }
    setMarkNumber();

    radioButtonsCurrent.forEach(function (radio, index) {
      radio.addEventListener('change', function () {
        const selectedIndex = Array.from(radioButtonsCurrent).indexOf(radio);
        console.log('Selected index:', selectedIndex + 1);
        current_rank = selectedIndex + 1;
        current_rank_name = divisionRanks[current_rank];
        console.log('current_rank', current_rank, current_rank_name);

        setMarkNumber();
        getResult();
      });
    });



    radioButtonsDesired.forEach(function (radio, index) {
      radio.addEventListener('change', function () {
        const selectedIndex = Array.from(radioButtonsDesired).indexOf(radio);
        console.log('Selected index:', selectedIndex + 1);
        desired_rank = selectedIndex + 1;
        desired_rank_name = divisionRanks[desired_rank]
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
        const selectedIndex = Array.from(radioButtonsCurrentDivision).indexOf(radio);
        console.log('Selected Division index:', selectedIndex + 1);
        current_division = selectedIndex + 1;
        current_division_name = divisionNames[current_division]
        getResult();
      });
    });



    radioButtonsDesiredDivision.forEach(function (radio, index) {
      radio.addEventListener('change', function () {
        const selectedIndex = Array.from(radioButtonsDesiredDivision).indexOf(radio);
        console.log('Selected Division index:', selectedIndex + 1);
        desired_division = selectedIndex + 1;
        desired_division_name = divisionNames[desired_division]
        getResult()
      });
    });

    makrs_on_current_rank_checked.forEach(function (radio, index) {
      radio.addEventListener('change', function () {
        const selectedIndex = Array.from(makrs_on_current_rank_checked).indexOf(radio);
        console.log('Selected Mark index:', selectedIndex);
        number_of_mark = marks_price[current_rank][selectedIndex];
        getResult();
      });
    });
  });






});

$(document).ready(function () {
  let divisionsData;
  let marksData;
  let currentId;
  let currentName;
  let currentDision;
  let currentDisionNumber;
  let currentMarks;
  let currentMark;
  let currentRank;

  let desiredId;
  let desiredName;
  let desiredDivision;
  let desiredDivisionNumber;
  let desiredRank;

  let completedRanks;

  let price = 0

  $.getJSON('/static/wildRift/data/divisions_data.json', function (data) {
    console.log(data)
    divisionsData = data
  });

  console.log(currentRank)

  $(".current").click(function () {
    currentId = $(this).data("id");
    currentName = $(this).data("name");
    currentMarks =currentMarks = $(this).data("mark");
    $(".current").removeClass("clicked");
    $(this).addClass("clicked");

    $(".current-dcontainer ").find("a").remove();
    $(".current-dcontainer").append(`
    <a id="current-division4" class="current-divison px-3 py-2 mb-3 border border-1 bg-light text-dark me-2 rounded-3 text-decoration-none" data-division="IV">IV</a>
    <a id="current-division3" class="current-divison px-3 py-2 mb-3 border border-1 bg-light text-dark me-2 rounded-3 text-decoration-none" data-division="III">III</a>
    <a id="current-division2" class="current-divison px-3 py-2 mb-3 border border-1 bg-light text-dark me-2 rounded-3 text-decoration-none" data-division="II">II</a>
    <a id="current-division1" class="current-divison px-3 py-2 mb-3 border border-1 bg-light text-dark me-2 rounded-3 text-decoration-none" data-division="I">I</a>
    `)

    currentRank = divisionsData.filter(item => item.name === currentName)[0];
    console.log(currentRank)
    $.getJSON('/static/wildRift/data/marks_data.json', function (data) {
      // console.log(data)
      marksData = data.filter(item => item.rank == currentName)[0]
      console.log(marksData)
    });
  });

  $(".desired").click(function () {
    desiredId = $(this).data("id");
    desiredName = $(this).data("name");
    desiredMarks = $(this).data("mark");
    $(this).css("background-color", "lightblue");
    $(".desired").removeClass("clicked");
    $(this).addClass("clicked");

    $(".desired-division").find("a").remove();
    if (desiredName != 'master') {
      $(".desired-dcontainer ").find("a").remove();
      $(".desired-dcontainer").append(`
      <a id="desired-division4" class="desired-divison px-3 py-2 mb-3 border border-1 bg-light text-dark me-2 rounded-3 text-decoration-none" data-division="IV">IV</a>
      <a id="desired-division3" class="desired-divison px-3 py-2 mb-3 border border-1 bg-light text-dark me-2 rounded-3 text-decoration-none" data-division="III">III</a>
      <a id="desired-division2" class="desired-divison px-3 py-2 mb-3 border border-1 bg-light text-dark me-2 rounded-3 text-decoration-none" data-division="II">II</a>
      <a id="desired-division1" class="desired-divison px-3 py-2 mb-3 border border-1 bg-light text-dark me-2 rounded-3 text-decoration-none" data-division="I">I</a>
      `)
    }
    desiredRank = divisionsData.filter(item => item.name === desiredName)[0];
    completedRanks = divisionsData.filter(item => item.id > currentRank.id && item.id < desiredRank.id);
    console.log(desiredRank)
    console.log(completedRanks)
  });

  $('.current-dcontainer').on('click', '.current-divison', function () {
    currentDision = $(this).data("division")
    if (currentDision == 'I') {
      currentDisionNumber = 1
    } else if (currentDision == 'II') {
      currentDisionNumber = 2
    } else if (currentDision == 'III') {
      currentDisionNumber = 3
    } else if (currentDision == 'IV') {
      currentDisionNumber = 4
    }
    $(".current-divison").removeClass("clicked");
    $(this).addClass("clicked");
    $(".current-marks").find("a").remove();
    for (let i = 0; i <= currentMarks; i++) {
      if (currentMarks !== 0) {
        $(".current-marks").append(`
          <a id="current-mark${i}" class="current-mark px-3 py-2 mb-3 border border-1 bg-light text-dark me-2 rounded-3 text-decoration-none" data-mark="${i}">${i} Mark</a>
        `);
      }
    }
  })
  $('.desired-dcontainer').on('click', '.desired-divison', function () {
    desiredDivision = $(this).data("division")
    if (desiredDivision == 'I') {
      desiredDivisionNumber = 1
    } else if (desiredDivision == 'II') {
      desiredDivisionNumber = 2
    } else if (desiredDivision == 'III') {
      desiredDivisionNumber = 3
    } else if (desiredDivision == 'IV') {
      desiredDivisionNumber = 4
    }
    $(".desired-divison").removeClass("clicked");
    $(this).addClass("clicked");
    console.log(desiredDivision)
  })


  $('.current-marks').on('click', '.current-mark', function () {
    $(".current-mark").removeClass("clicked");
    $(this).addClass("clicked");
    currentMark = $(this).data("mark")
    console.log('mark', currentMark)
    console.log(currentDisionNumber)
    console.log(desiredDivisionNumber)
    if (currentDisionNumber > desiredDivisionNumber && currentRank == desiredRank) {
      price = 0
      for (let i = desiredDivisionNumber; i < currentDisionNumber; i++) {
        console.log(i)
        if (i == 1) {
          price += desiredRank.I
        } else if (i == 2) {
          price += desiredRank.II
        } else if (i == 3) {
          price += desiredRank.III
        } else if (i == 4) {
          price += desiredRank.IV
        }
      }
    } else {
      price = 0
      for (let j = currentDisionNumber - 1; j >= 1; j--) {
        if (j == 1) {
          price += currentRank.I
        } else if (j == 2) {
          price += currentRank.II
        } else if (j == 3) {
          price += currentRank.III
        } else if (j == 4) {
          price += currentRank.IV
        }
      }

      for (let k = desiredDivisionNumber + 1; k <= 4; k++) {
        console.log(desiredDivisionNumber)
        if (k == 1) {
          price += desiredRank.I
        } else if (k == 2) {
          price += desiredRank.II
        } else if (k == 3) {
          price += desiredRank.III
        } else if (k == 4) {

          price += desiredRank.IV
        }
      }
      console.log(completedRanks)
      for (let i = 0; i < completedRanks.length; i++) {
        price += completedRanks[i].I + completedRanks[i].II + completedRanks[i].III + completedRanks[i].IV
      }
    }
    console.log(marksData)
    if (currentMark == 1) {
      console.log('m', marksData.mark_1)
      price -= marksData.mark_1
    } else if (currentMark == 2) {
      console.log('m', marksData.mark_2)
      price -= marksData.mark_2
    } else if (currentMark == 3) {
      console.log('m', marksData.mark_3)
      price -= marksData.mark_3
    } else if (currentMark == 4) {
      console.log('m', marksData.mark_4)
      price -= marksData.mark_4
    } else if (currentMark == 5) {
      console.log('m', marksData.mark_5)
      price -= marksData.mark_5
    }
    console.log('current', currentRank.name)
    console.log('Desired', desiredRank.name)
    console.log('CDivision', currentDision)
    console.log('DDivision', desiredDivision)
    console.log('Mark', currentMark)
    console.log('price', price)

    $(".price-container").find("p").remove();
    $(".price-container").find("h4").remove();
    $('.price-container').append(`
    <p class='fs-5 text-uppercase my-4'>Boosting <span class='fw-bold'>From ${currentRank.name} ${currentDision} ${currentMark} Marks to ${desiredRank.name} ${desiredDivision}</span></p>
    <h4>$${price}</h4>
`)
  })
});
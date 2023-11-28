$(document).ready(function () {
  $(".current").click(function () {
    let currentId = $(this).data("id");
    let currentName = $(this).data("name");
    let currentDivision = $(this).data("division");
    let currentMarks = $(this).data("mark");
    console.log("current-id", currentId)
    console.log("current-name", currentName)
    console.log("current-Division", currentDivision)
    console.log("current-marks", currentMarks)
    $(".current").removeClass("clicked");
    $(this).addClass("clicked");

    $(".current-division").find("a").remove();
    for(let i = 1; i <= currentDivision; i++){
      $(".current-division").append(`
        <a id="current-division${i}" class="current-divison px-3 py-2 mb-3 border border-1 bg-light text-dark me-2 rounded-3 text-decoration-none" data-number="${i}">${i}</a>
      `)
    }

    $(".current-marks").find("a").remove();
    for(let i = 0; i <= currentMarks; i++){
      if(currentMarks != 0) {
        $(".current-marks").append(`
          <a id="current-mark${i}" class="current-mark px-3 py-2 mb-3 border border-1 bg-light text-dark me-2 rounded-3 text-decoration-none" data-number="${i}">${i} Mark</a>
        `)
      }
      }

  });

  $(".desired").click(function () {
    let desiredId = $(this).data("id");
    let desiredName = $(this).data("name");
    let desiredDivision = $(this).data("division");
    let desiredMarks = $(this).data("mark");
    console.log("desired-id", desiredId)
    console.log("desired-name", desiredName)
    console.log("desired-Division", desiredDivision)
    console.log("desired-marks", desiredMarks)
    $(this).css("background-color", "lightblue");
    $(".desired").removeClass("clicked");
    $(this).addClass("clicked");

    $(".desired-division").find("a").remove();
    for(let i = 1; i <= desiredDivision; i++){
      $(".desired-division").append(`
      <a id="desired-division${i}" class="desired-divison px-3 py-2 mb-3 border border-1 bg-light text-dark me-2 rounded-3 text-decoration-none" data-number="${i}">${i}</a>
      `)
    }
  });
});
// ----------------------------- Arena 2x2 Boost ---------------------------------
var currentArena2x2 = document.getElementById('currentArena2x2');
var currentArena2x2Value = document.getElementById('currentArena2x2Value');
var desiredArena2x2 = document.getElementById('desiredArena2x2');
var desiredArena2x2Value = document.getElementById('desiredArena2x2Value');

// Initail Values
currentArena2x2.value = 0
desiredArena2x2.value = 0
var currentArena2x2_InputValue = parseFloat(currentArena2x2Value.value);
var desiredArena2x2_InputValue = parseFloat(desiredArena2x2Value.value);

function getArena2x2Price() {
  let result = (desiredArena2x2Value.value - currentArena2x2Value.value) * 0.02

  // Apply extra charges to the result
  result += result * total_Percentage;
  result = parseFloat(result.toFixed(2)); 

  // From Value
  $('.arena-boost input[name="current_RP"]').val(currentArena2x2Value.value);
  $('.arena-boost input[name="desired_RP"]').val(desiredArena2x2Value.value);
  $('.arena-boost input[name="price"]').val(result);
}

getArena2x2Price()

// Current Arena 2x2
currentArena2x2.addEventListener('input', function() {
  currentArena2x2Value.value = currentArena2x2.value;
  getArena2x2Price()
});
currentArena2x2Value.addEventListener('input', function() {
  if (!isNaN(currentArena2x2_InputValue)) {
    currentArena2x2.value = currentArena2x2_InputValue;
    getArena2x2Price()
  }
});
currentArena2x2Value.addEventListener('input', function() {
  currentArena2x2.value = currentArena2x2Value.value;
  getArena2x2Price()
});

// Desired Arena 2x2
desiredArena2x2.addEventListener('input', function() {
  desiredArena2x2Value.value = desiredArena2x2.value;
  getArena2x2Price()
});
desiredArena2x2Value.addEventListener('input', function() {
  if (!isNaN(desiredArena2x2_InputValue)) {
    desiredArena2x2.value = desiredArena2x2_InputValue;
    getArena2x2Price()
  }
});
desiredArena2x2Value.addEventListener('input', function() {
  desiredArena2x2.value = desiredArena2x2Value.value;
  getArena2x2Price()
});
// ================================================================================
// ----------------------------- Arena 2vs2 Boost ---------------------------------
    // Current 2vs2 Varible
    const current2vs2Arena = $('#current-2vs2-arena');
    const current2vs2Steps = $('.current-2vs2.step-indicator .step');
    let current2vs2ArenaValue = Number(current2vs2Arena.val())
    let current2vs2Rank = getRank(current2vs2ArenaValue)

    // Desired 2vs2 Varible
    const desired2vs2Arena = $('#desired-2vs2-arena');
    const desired2vs2Steps = $('.desired-2vs2.step-indicator .step');
    let desired2vs2ArenaValue = Number(current2vs2Arena.val())
    let desired2vs2Rank = getRank(desired2vs2ArenaValue)

    // 2vs2 Arena Server
    const arena_2vs2_server_select_element = $('.arena-2vs2-servers-select');
    let selected2vs2ArenaServer = arena_2vs2_server_select_element.val()

    function get2vs2ArenaPrice() {
      // Current
      $('#current-2vs2 .current-2vs2-rp').html(current2vs2ArenaValue);
      $('.current-2vs2-selected-img').attr('src', `/media/wow/images/${current2vs2Rank}.png`);
      $('.current.current-2vs2').removeClass().addClass(`current current-2vs2 rank-${current2vs2Rank}`);
      $('.current-2vs2-selected-info').html(`${current2vs2ArenaValue} MMR`)

      // Desired
      $('#desired-2vs2 .desired-2vs2-rp').html(desired2vs2ArenaValue);
      $('.desired-2vs2-selected-img').attr('src', `/media/wow/images/${desired2vs2Rank}.png`);
      $('.desired.desired-2vs2').removeClass().addClass(`desired desired-2vs2 rank-${desired2vs2Rank}`);
      $('.desired-2vs2-selected-info').html(`${desired2vs2ArenaValue} MMR`)

      // Form
      $('#arena-form input[name="server"]').val(selected2vs2ArenaServer);


    }
    get2vs2ArenaPrice()

    current2vs2Arena.on("input", function (event) {
      current2vs2ArenaValue = Number(event.target.value);
      current2vs2Rank = getRank(current2vs2ArenaValue)

      if((desired2vs2ArenaValue - current2vs2ArenaValue) < 50) {
        desired2vs2Arena.val(current2vs2ArenaValue + 50);
        desired2vs2ArenaValue = current2vs2ArenaValue + 50;
        desired2vs2Rank = getRank(desired2vs2ArenaValue)

        const progress = ((desired2vs2ArenaValue) / (desired2vs2Arena.prop("max"))) * 100;

        desired2vs2Arena.css({
          "background": `linear-gradient(to right, #F36E3F ${progress}%, #251D16 ${progress}%)`
        });
      }
      
      const progress = ((current2vs2ArenaValue) / (current2vs2Arena.prop("max"))) * 100;

      current2vs2Arena.css({
        "background": `linear-gradient(to right, #F36E3F ${progress}%, #251D16 ${progress}%)`
      });
      
      current2vs2Steps.each((step, index) => {
        
        if (parseInt(index.innerText) < current2vs2ArenaValue) {
          index.classList.add('selected')
        } else {
          index.classList.remove('selected');
        }
      });

      get2vs2ArenaPrice()

    })

    desired2vs2Arena.on("input", function (event) {
      desired2vs2ArenaValue = Number(event.target.value);
      desired2vs2Rank = getRank(desired2vs2ArenaValue)

      if((desired2vs2ArenaValue - current2vs2ArenaValue) < 50) {
        desired2vs2Arena.val(current2vs2ArenaValue + 50);
        desired2vs2ArenaValue = current2vs2ArenaValue + 50;
        desired2vs2Rank = getRank(desired2vs2ArenaValue)
      }
      
      const progress = ((desired2vs2ArenaValue) / (desired2vs2Arena.prop("max"))) * 100;

      desired2vs2Arena.css({
        "background": `linear-gradient(to right, #F36E3F ${progress}%, #251D16 ${progress}%)`
      });
      
      desired2vs2Steps.each((step, index) => {
        
        if (parseInt(index.innerText) < desired2vs2ArenaValue) {
          index.classList.add('selected')
        } else {
          index.classList.remove('selected');
        }
      });

      get2vs2ArenaPrice()

    })

    // Server Changes
    arena_2vs2_server_select_element.on("change", function() {
      selected2vs2ArenaServer = $(this).val();
      $('#arena-form input[name="server"]').val(selected2vs2ArenaServer);
    });

    // ----------------------------- Arena 3vs3 Boost ---------------------------------
    // Current 3vs3 Varible
    const current3vs3Arena = $('#current-3vs3-arena');
    const current3vs3Steps = $('.current-3vs3.step-indicator .step');
    let current3vs3ArenaValue = Number(current3vs3Arena.val())
    let current3vs3Rank = getRank(current3vs3ArenaValue)

    // Desired 3vs3 Varible
    const desired3vs3Arena = $('#desired-3vs3-arena');
    const desired3vs3Steps = $('.desired-3vs3.step-indicator .step');
    let desired3vs3ArenaValue = Number(current3vs3Arena.val())
    let desired3vs3Rank = getRank(desired3vs3ArenaValue)

    // 3vs3 Arena Server
    const arena_3vs3_server_select_element = $('.arena-3vs3-servers-select');
    let selected3vs3ArenaServer = arena_3vs3_server_select_element.val()

    function get3vs3ArenaPrice() {
      // Current
      $('#current-3vs3 .current-3vs3-rp').html(current3vs3ArenaValue);
      $('.current-3vs3-selected-img').attr('src', `/media/wow/images/${current3vs3Rank}.png`);
      $('.current.current-3vs3').removeClass().addClass(`current current-3vs3 rank-${current3vs3Rank}`);
      $('.current-3vs3-selected-info').html(`${current3vs3ArenaValue} MMR`)

      // Desired
      $('#desired-3vs3 .desired-3vs3-rp').html(desired3vs3ArenaValue);
      $('.desired-3vs3-selected-img').attr('src', `/media/wow/images/${desired3vs3Rank}.png`);
      $('.desired.desired-3vs3').removeClass().addClass(`desired desired-3vs3 rank-${desired3vs3Rank}`);
      $('.desired-3vs3-selected-info').html(`${desired3vs3ArenaValue} MMR`)

      // Form
      $('#arena-form input[name="server"]').val(selected3vs3ArenaServer);
    }
    get3vs3ArenaPrice()

    current3vs3Arena.on("input", function (event) {
      current3vs3ArenaValue = Number(event.target.value);
      current3vs3Rank = getRank(current3vs3ArenaValue)
      
      const progress = ((current3vs3ArenaValue) / (current3vs3Arena.prop("max"))) * 100;

      current3vs3Arena.css({
        "background": `linear-gradient(to right, #F36E3F ${progress}%, #251D16 ${progress}%)`
      });
      
      current3vs3Steps.each((step, index) => {
        
        if (parseInt(index.innerText) < current3vs3ArenaValue) {
          index.classList.add('selected')
        } else {
          index.classList.remove('selected');
        }
      });

      get3vs3ArenaPrice()

    })

    desired3vs3Arena.on("input", function (event) {
      desired3vs3ArenaValue = Number(event.target.value);
      desired3vs3Rank = getRank(desired3vs3ArenaValue);

      if((desired3vs3ArenaValue - current3vs3ArenaValue) < 50) {
        desired3vs3Arena.val(current3vs3ArenaValue + 50);
        desired3vs3ArenaValue = current3vs3ArenaValue + 50;
        desired3vs3Rank = getRank(desired3vs3ArenaValue)
      }
      
      const progress = ((desired3vs3ArenaValue) / (desired3vs3Arena.prop("max"))) * 100;

      desired3vs3Arena.css({
        "background": `linear-gradient(to right, #F36E3F ${progress}%, #251D16 ${progress}%)`
      });
      
      desired3vs3Steps.each((step, index) => {
        
        if (parseInt(index.innerText) < desired3vs3ArenaValue) {
          index.classList.add('selected')
        } else {
          index.classList.remove('selected');
        }
      });

      get3vs3ArenaPrice()

    })

    // Server Changes
    arena_3vs3_server_select_element.on("change", function() {
      selected3vs3ArenaServer = $(this).val();
      $('#arena-form input[name="server"]').val(selected3vs3ArenaServer);
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

        get2vs2ArenaPrice()
        get3vs3ArenaPrice()
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
        get2vs2ArenaPrice()
        get3vs3ArenaPrice()
      })
    });

    promo_form.addEventListener('submit', async function(event) {
      event.preventDefault();
      discount_amount = await fetch_promo(); 
      get2vs2ArenaPrice(); 
      get3vs3ArenaPrice();
    });

// ===========================================================

const ranks = ["UNRANK", "0-1599", "1600-1799", "1800-2099", "2100-2499"];
const MIN_DESIRED_DIFFERENCE = 50;

function getRank(rp)  {
  if (rp >= 2100) {
    return ranks[4]
  } 

  if (rp >= 1800 && rp < 2100) {
    return ranks[3]
  }

  if (rp >= 1600 && rp < 1799) {
    return ranks[2]
  }

  if (rp < 1600) {
    return ranks[1]
  }
}
(async function() {
  try {
    const [price_of_2vs2, price_of_3vs3] = await new Promise((resolve, reject) => {
      $.getJSON('/static/wow/data/prices.json', function (data) {
        resolve(data);
      }).fail(reject);
    });

    // Current Change Function
    function currentArenaChange(arenaType, currentArena, currentRank, currentArenaValue, currentSteps) {
      currentRank = getRank(currentArenaValue)
      
      const progress = ((currentArenaValue) / (currentArena.prop("max"))) * 100;

      currentArena.css({
        "background": `linear-gradient(to right, #F36E3F ${progress}%, #251D16 ${progress}%)`
      });
      
      currentSteps.each((step, index) => {
        
        if (parseInt(index.innerText) < currentArenaValue) {
          index.classList.add('selected')
        } else {
          index.classList.remove('selected');
        }
      });
      
      // Current
      $(`#current-${arenaType} .current-${currentArenaValue}-rp`).html(currentArenaValue);
      $(`.current-${arenaType}-selected-img`).attr('src', `/media/wow/images/${currentRank}.png`);
      $(`.current.current-${arenaType}`).removeClass().addClass(`current current-2vs2 rank-${currentRank}`);
      $(`.current-${arenaType}-selected-info`).html(`${currentArenaValue} MMR`)
    }

    // Desired Change Function
    function desiredArenaChange(arenaType, desiredArena, desiredRank, desiredArenaValue, desiredSteps) {
      desiredRank = getRank(desiredArenaValue)
      
      const progress = ((desiredArenaValue) / (desiredArena.prop("max"))) * 100;
  
      desiredArena.css({
        "background": `linear-gradient(to right, #F36E3F ${progress}%, #251D16 ${progress}%)`
      });
      
      desiredSteps.each((step, index) => {
        
        if (parseInt(index.innerText) < desiredArenaValue) {
          index.classList.add('selected')
        } else {
          index.classList.remove('selected');
        }
      });

      // Desired
      $(`#desired-${arenaType} .desired-${arenaType}-rp`).html(desiredArenaValue);
      $(`.desired-${arenaType}-selected-img`).attr('src', `/media/wow/images/${desiredRank}.png`);
      $(`.desired.desired-${arenaType}`).removeClass().addClass(`desired desired-2vs2 rank-${desiredRank}`);
      $(`.desired-${arenaType}-selected-info`).html(`${desiredArenaValue} MMR`)

    }

    // Price Fuction
    function getPrice(arenaType, ) {

      // Form
      $('#arena-form input[name="is_Arena_2x2"]').val(arenaType == '2vs2');
      $('#arena-form input[name="server"]').val(selected2vs2ArenaServer);
    }


    // ----------------------------- Arena 2vs2 Boost ---------------------------------
    // Current 2vs2 Varible
    const current2vs2Arena = $('#current-2vs2-arena');
    const current2vs2Steps = $('.current-2vs2.step-indicator .step');
    let current2vs2ArenaValue = Number(current2vs2Arena.val())
    let current2vs2Rank = getRank(current2vs2ArenaValue)

    // Desired 2vs2 Varible
    const desired2vs2Arena = $('#desired-2vs2-arena');
    const desired2vs2Steps = $('.desired-2vs2.step-indicator .step');
    let desired2vs2ArenaValue = Number(current2vs2Arena.val())
    let desired2vs2Rank = getRank(desired2vs2ArenaValue)

    // 2vs2 Arena Server
    const arena_2vs2_server_select_element = $('.arena-2vs2-servers-select');
    let selected2vs2ArenaServer = arena_2vs2_server_select_element.val()

    current2vs2Arena.on("input", function (event) {
      current2vs2ArenaValue = Number(event.target.value);

      // Call Function To Change
      currentArenaChange('2vs2', current2vs2Arena, current2vs2Rank, current2vs2ArenaValue, current2vs2Steps)

      if((desired2vs2ArenaValue - current2vs2ArenaValue) < MIN_DESIRED_DIFFERENCE) {
        desired2vs2Arena.val(current2vs2ArenaValue + MIN_DESIRED_DIFFERENCE);
        desired2vs2ArenaValue = current2vs2ArenaValue + MIN_DESIRED_DIFFERENCE;

        desiredArenaChange('2vs2', desired2vs2Arena, desired2vs2Rank, desired2vs2ArenaValue, desired2vs2Steps)
      }

    })

    desired2vs2Arena.on("input", function (event) {
      desired2vs2ArenaValue = Number(event.target.value);

      // Call Function To Change
      desiredArenaChange('2vs2', desired2vs2Arena, desired2vs2Rank, desired2vs2ArenaValue, desired2vs2Steps)

      if((desired2vs2ArenaValue - current2vs2ArenaValue) < MIN_DESIRED_DIFFERENCE) {

        desired2vs2Arena.val(current2vs2ArenaValue + MIN_DESIRED_DIFFERENCE);
        desired2vs2ArenaValue = current2vs2ArenaValue + MIN_DESIRED_DIFFERENCE;

        desiredArenaChange('2vs2', desired2vs2Arena, desired2vs2Rank, desired2vs2ArenaValue, desired2vs2Steps)
      }

    })

    // Server Changes
    arena_2vs2_server_select_element.on("change", function() {
      selected2vs2ArenaServer = $(this).val();
      $('#arena-form input[name="server"]').val(selected2vs2ArenaServer);
    });

    // ----------------------------- Arena 3vs3 Boost ---------------------------------
    // Current 3vs3 Varible
    const current3vs3Arena = $('#current-3vs3-arena');
    const current3vs3Steps = $('.current-3vs3.step-indicator .step');
    let current3vs3ArenaValue = Number(current3vs3Arena.val())
    let current3vs3Rank = getRank(current3vs3ArenaValue)

    // Desired 3vs3 Varible
    const desired3vs3Arena = $('#desired-3vs3-arena');
    const desired3vs3Steps = $('.desired-3vs3.step-indicator .step');
    let desired3vs3ArenaValue = Number(current3vs3Arena.val())
    let desired3vs3Rank = getRank(desired3vs3ArenaValue)

    // 3vs3 Arena Server
    const arena_3vs3_server_select_element = $('.arena-3vs3-servers-select');
    let selected3vs3ArenaServer = arena_3vs3_server_select_element.val()

    function get3vs3ArenaPrice() {
      // Current
      $('#current-3vs3 .current-3vs3-rp').html(current3vs3ArenaValue);
      $('.current-3vs3-selected-img').attr('src', `/media/wow/images/${current3vs3Rank}.png`);
      $('.current.current-3vs3').removeClass().addClass(`current current-3vs3 rank-${current3vs3Rank}`);
      $('.current-3vs3-selected-info').html(`${current3vs3ArenaValue} MMR`)

      // Desired
      $('#desired-3vs3 .desired-3vs3-rp').html(desired3vs3ArenaValue);
      $('.desired-3vs3-selected-img').attr('src', `/media/wow/images/${desired3vs3Rank}.png`);
      $('.desired.desired-3vs3').removeClass().addClass(`desired desired-3vs3 rank-${desired3vs3Rank}`);
      $('.desired-3vs3-selected-info').html(`${desired3vs3ArenaValue} MMR`)

      // Form
      $('#arena-form input[name="server"]').val(selected3vs3ArenaServer);
    }
    get3vs3ArenaPrice()

    current3vs3Arena.on("input", function (event) {
      current3vs3ArenaValue = Number(event.target.value);
      current3vs3Rank = getRank(current3vs3ArenaValue)
      
      const progress = ((current3vs3ArenaValue) / (current3vs3Arena.prop("max"))) * 100;

      current3vs3Arena.css({
        "background": `linear-gradient(to right, #F36E3F ${progress}%, #251D16 ${progress}%)`
      });
      
      current3vs3Steps.each((step, index) => {
        
        if (parseInt(index.innerText) < current3vs3ArenaValue) {
          index.classList.add('selected')
        } else {
          index.classList.remove('selected');
        }
      });

      get3vs3ArenaPrice()

    })

    desired3vs3Arena.on("input", function (event) {
      desired3vs3ArenaValue = Number(event.target.value);
      desired3vs3Rank = getRank(desired3vs3ArenaValue);

      if((desired3vs3ArenaValue - current3vs3ArenaValue) < 50) {
        desired3vs3Arena.val(current3vs3ArenaValue + 50);
        desired3vs3ArenaValue = current3vs3ArenaValue + 50;
        desired3vs3Rank = getRank(desired3vs3ArenaValue)
      }
      
      const progress = ((desired3vs3ArenaValue) / (desired3vs3Arena.prop("max"))) * 100;

      desired3vs3Arena.css({
        "background": `linear-gradient(to right, #F36E3F ${progress}%, #251D16 ${progress}%)`
      });
      
      desired3vs3Steps.each((step, index) => {
        
        if (parseInt(index.innerText) < desired3vs3ArenaValue) {
          index.classList.add('selected')
        } else {
          index.classList.remove('selected');
        }
      });

      get3vs3ArenaPrice()

    })

    // Server Changes
    arena_3vs3_server_select_element.on("change", function() {
      selected3vs3ArenaServer = $(this).val();
      $('#arena-form input[name="server"]').val(selected3vs3ArenaServer);
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

        get2vs2ArenaPrice()
        get3vs3ArenaPrice()
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
        get2vs2ArenaPrice()
        get3vs3ArenaPrice()
      })
    });

    promo_form.addEventListener('submit', async function(event) {
      event.preventDefault();
      discount_amount = await fetch_promo(); 
      get2vs2ArenaPrice(); 
      get3vs3ArenaPrice();
    });

  } catch (error) {
    console.error('Error:', error);
  }
})();
// ===================#
let price = (desired3vs3ArenaValue - current3vs3ArenaValue) * (price_of_3vs3 / MIN_DESIRED_VALUE);

// Apply extra charges to the result
price += price * total_Percentage;

// Apply promo code 
price -= price * (discount_amount/100 )

price = parseFloat(price.toFixed(2)); 

// Current
$('#current-3vs3 .current-3vs3-rp').html(current3vs3ArenaValue);
$('.current-3vs3-selected-img').attr('src', `/media/wow/images/${current3vs3Rank}.png`);
$('.current.current-3vs3').removeClass().addClass(`current current-3vs3 rank-${current3vs3Rank}`);
$('.current-3vs3-selected-info').html(`${current3vs3ArenaValue} MMR`)

// Desired
$('#desired-3vs3 .desired-3vs3-rp').html(desired3vs3ArenaValue);
$('.desired-3vs3-selected-img').attr('src', `/media/wow/images/${desired3vs3Rank}.png`);
$('.desired.desired-3vs3').removeClass().addClass(`desired desired-3vs3 rank-${desired3vs3Rank}`);
$('.desired-3vs3-selected-info').html(`${desired3vs3ArenaValue} MMR`)

// Price
$('#arena-3vs3-price').html(`$${price}`)

// Form
$('#arena-form input[name="is_Arena_2x2"]').val(false);
$('#arena-form input[name="current_rank"]').val(getRank(current3vs3ArenaValue)[1]);
$('#arena-form input[name="current_RP"]').val(current3vs3ArenaValue);
$('#arena-form input[name="desired_rank"]').val(getRank(desired3vs3ArenaValue)[1]);
$('#arena-form input[name="desired_RP"]').val(desired3vs3ArenaValue);
$('#arena-form input[name="server"]').val(selected3vs3ArenaServer);
$('#arena-form input[name="price"]').val(price);
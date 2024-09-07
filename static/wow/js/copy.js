document.addEventListener("DOMContentLoaded", function () {

  const ranks = ["UNRANK", "0-1599", "1600-1799", "1800-2099", "2100-2499"]
  const MIN_DESIRED_VALUE = 50

  function getRank(rp)  {
    if (rp >= 2100) {
      return [ranks[4], 4]
    } 

    if (rp >= 1800 && rp < 2100) {
      return [ranks[3], 3]
    }

    if (rp >= 1600 && rp < 1799) {
      return [ranks[2], 2]
    }

    if (rp < 1600) {
      return [ranks[1], 1]
    }
  }

  const total_Percentage_value_arena = ()=>{
    const extraCheckbox = document.getElementsByName('extra-checkbox');
    let total_Percentage = 0
    extraCheckbox.forEach((checkbox) => {
      if (checkbox.checked) {
        if (!['tournament', 'timed'].includes(checkbox.id)) {
          total_Percentage += parseInt(checkbox.value);
        }
      }
    })
    return (total_Percentage / 100)
  }

  const prices = document.getElementById('WorldOfWarcraftRpsPrice');
  const price_of_2vs2 = parseFloat(prices.dataset.rp2vs2);
  const price_of_3vs3 = parseFloat(prices.dataset.rp3vs3);


  function changeUI(achivedValue, arena, steps) {
    // const progress = ((achivedValue) / (arena.prop("max"))) * 100;

    // arena.css({
    //   "background": `linear-gradient(to right, #F36E3F ${progress}%, #251D16 ${progress}%)`
    // });
    
    // steps.each((step, index) => {
      
    //   if (parseInt(index.innerText) < achivedValue) {
    //     index.classList.add('selected')
    //   } else {
    //     index.classList.remove('selected');
    //   }
    // });
  }

  // ----------------------------- Arena 2vs2 Boost Varible ---------------------------------
  // Current 2vs2 Varible
  const current2vs2Arena = $('#current-2vs2-arena');
  const current2vs2Steps = $('.current-2vs2.step-indicator .step');
  let current2vs2ArenaValue = Number(current2vs2Arena.val())
  let current2vs2Rank = getRank(current2vs2ArenaValue)[0]

  // Desired 2vs2 Varible
  const desired2vs2Arena = $('#desired-2vs2-arena');
  const desired2vs2Steps = $('.desired-2vs2.step-indicator .step');
  let desired2vs2ArenaValue = Number(current2vs2Arena.val())
  let desired2vs2Rank = getRank(desired2vs2ArenaValue)[0]

  // 2vs2 Arena Server
  const arena_2vs2_server_select_element = $('.arena-2vs2-servers-select');
  let selected2vs2ArenaServer = arena_2vs2_server_select_element.val();

  // ----------------------------- Arena 3vs3 Boost Variable ---------------------------------
  // Current 3vs3 Varible
  const current3vs3Arena = $('#current-3vs3-arena');
  const current3vs3Steps = $('.current-3vs3.step-indicator .step');
  let current3vs3ArenaValue = Number(current3vs3Arena.val())
  let current3vs3Rank = getRank(current3vs3ArenaValue)[0];

  // Desired 3vs3 Varible
  const desired3vs3Arena = $('#desired-3vs3-arena');
  const desired3vs3Steps = $('.desired-3vs3.step-indicator .step');
  let desired3vs3ArenaValue = Number(current3vs3Arena.val())
  let desired3vs3Rank = getRank(desired3vs3ArenaValue)[0];

  // 3vs3 Arena Server
  const arena_3vs3_server_select_element = $('.arena-3vs3-servers-select');
  let selected3vs3ArenaServer = arena_3vs3_server_select_element.val()


  if(extend_order) {
    let orderID = parseInt(extend_order, 10);
    document.getElementById('extendOrder').value = orderID; 
    const extends_from_2vs2 = valuesToSetExtra[0]

    arena_2vs2_server_select_element.disabled = true
    arena_3vs3_server_select_element.disabled = true

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
        total_Percentage += percentege[checkbox.value];
        $(`input#${checkbox.value}`).val(true)

      } else if (checkbox.value === "turboBoost" && valuesToSetAdditional[2]) {
        checkbox.checked = true
        total_Percentage += percentege[checkbox.value];
        $(`input#${checkbox.value}`).val(true)

      } else if (checkbox.value === "streaming" && valuesToSetAdditional[3]) {
        checkbox.checked = true
        total_Percentage += percentege[checkbox.value];
        $(`input#${checkbox.value}`).val(true)

      } else if (checkbox.value === "boosterChampions" && valuesToSetAdditional[4]) {
        checkbox.checked = true
        total_Percentage += percentege[checkbox.value];
        $(`input#${checkbox.value}`).val(true)

      } else {
        checkbox.checked = false
        $(`input#${checkbox.value}`).val(false)
      } 
      
      $(checkbox).prop('disabled', true)
    }) 

    // Check Type 
    if(extends_from_2vs2) {
      $('input[type="radio"]#arena-3vs3').prop('disabled', true)
      
      // Change Values
      current2vs2Rank = getRank(valuesToSet[1])[0]
      desired2vs2Rank = getRank(valuesToSet[4])[0]
      current2vs2ArenaValue = valuesToSet[1]
      desired2vs2ArenaValue = valuesToSet[4]

      // Change Range Value
      current2vs2Arena.val(current2vs2ArenaValue) 
      desired2vs2Arena.val(desired2vs2ArenaValue) 

      // Change Range UI
      changeUI(current2vs2ArenaValue, current2vs2Arena, current2vs2Steps)
      changeUI(desired2vs2ArenaValue, desired2vs2Arena, desired2vs2Steps)

      // Disable Current
      current2vs2Arena.prop('disabled', true)

      function get2vs2ArenaPrice() {
        // Price
        let price = (desired2vs2ArenaValue - valuesToSet[4]) * (price_of_2vs2 / MIN_DESIRED_VALUE);
      
        // Apply extra charges to the result
        const total_Percentage = total_Percentage_value_arena();
        price += price * total_Percentage;
      
        // Apply promo code 
        price -= price * (discountAmount / 100 )
      
        price = parseFloat(price.toFixed(2));
      
        // Current
        $('#current-2vs2 .current-2vs2-rp').html(current2vs2ArenaValue);
        $('.current-2vs2-selected-img').attr('src', `https://storage.googleapis.com/mad-boost.appspot.com/wow/images/${getRank(current2vs2ArenaValue)[0]}.png`);
        $('.current.current-2vs2').removeClass().addClass(`current current-2vs2 rank-${getRank(valuesToSet[4])[0]}`);
        $('.current-2vs2-selected-info').html(`${valuesToSet[4]} MMR`)
      
        // Desired
        $('#desired-2vs2 .desired-2vs2-rp').html(desired2vs2ArenaValue);
        $('.desired-2vs2-selected-img').attr('src', `https://storage.googleapis.com/mad-boost.appspot.com/wow/images/${desired2vs2Rank}.png`);
        $('.desired.desired-2vs2').removeClass().addClass(`desired desired-2vs2 rank-${desired2vs2Rank}`);
        $('.desired-2vs2-selected-info').html(`${desired2vs2ArenaValue} MMR`)
      
        // Price
        $('#arena-2vs2-price').html(`$${price}`)
      
        // Form
        $('#arena-form input[name="is_arena_2vs2"]').val(true);
        $('#arena-form input[name="current_rank"]').val(getRank(current2vs2ArenaValue)[1]);
        $('#arena-form input[name="current_RP"]').val(current2vs2ArenaValue);
        $('#arena-form input[name="desired_rank"]').val(getRank(desired2vs2ArenaValue)[1]);
        $('#arena-form input[name="desired_RP"]').val(desired2vs2ArenaValue);
        $('#arena-form input[name="server"]').val(server);
        $('#arena-form input[name="price"]').val(price);

        // SET PROMO CODE IN FORM
        $('#arena-form input[name="promo_code"]').val(extendPromoCode);
        
      }
    } else {
      $('input[type="radio"]#arena-3vs3').prop('checked', true);
      $('input[type="radio"]#arena-2vs2').prop('disabled', true)
      
      // Change Values
      current3vs3Rank = getRank(valuesToSet[1])[0]
      desired3vs3Rank = getRank(valuesToSet[4])[0]
      current3vs3ArenaValue = valuesToSet[1]
      desired3vs3ArenaValue = valuesToSet[4]

      // Change Range Value
      current3vs3Arena.val(current3vs3ArenaValue) 
      desired3vs3Arena.val(desired3vs3ArenaValue) 

      // Change Range UI
      changeUI(current3vs3ArenaValue, current3vs3Arena, current3vs3Steps)
      changeUI(desired3vs3ArenaValue, desired3vs3Arena, desired3vs3Steps)

      // Disable Current
      current3vs3Arena.prop('disabled', true)

      function get3vs3ArenaPrice() {
        // Price
        let price = (desired3vs3ArenaValue - valuesToSet[4]) * (price_of_3vs3 / MIN_DESIRED_VALUE);
        
        const total_Percentage = total_Percentage_value_arena();
        // Apply extra charges to the result
        price += price * total_Percentage;
      
        // Apply promo code 
        price -= price * (discountAmount / 100 )
      
        price = parseFloat(price.toFixed(2));
      
        // Current
        $('#current-3vs3 .current-3vs3-rp').html(current3vs3ArenaValue);
        $('.current-3vs3-selected-img').attr('src', `https://storage.googleapis.com/mad-boost.appspot.com/wow/images/${getRank(current3vs3ArenaValue)[0]}.png`);
        $('.current.current-3vs3').removeClass().addClass(`current current-3vs3 rank-${getRank(valuesToSet[4])[0]}`);
        $('.current-3vs3-selected-info').html(`${valuesToSet[4]} MMR`)
      
        // Desired
        $('#desired-3vs3 .desired-3vs3-rp').html(desired3vs3ArenaValue);
        $('.desired-3vs3-selected-img').attr('src', `https://storage.googleapis.com/mad-boost.appspot.com/wow/images/${desired3vs3Rank}.png`);
        $('.desired.desired-3vs3').removeClass().addClass(`desired desired-3vs3 rank-${desired3vs3Rank}`);
        $('.desired-3vs3-selected-info').html(`${desired3vs3ArenaValue} MMR`)
      
        // Price
        $('#arena-3vs3-price').html(`$${price}`)
      
        // Form
        $('#arena-form input[name="is_arena_2vs2"]').val(false);
        $('#arena-form input[name="current_rank"]').val(getRank(current3vs3ArenaValue)[1]);
        $('#arena-form input[name="current_RP"]').val(current3vs3ArenaValue);
        $('#arena-form input[name="desired_rank"]').val(getRank(desired3vs3ArenaValue)[1]);
        $('#arena-form input[name="desired_RP"]').val(desired3vs3ArenaValue);
        $('#arena-form input[name="server"]').val(server);
        $('#arena-form input[name="price"]').val(price);

        // SET PROMO CODE IN FORM
        $('#arena-form input[name="promo_code"]').val(extendPromoCode);
        
      }
    }

  } else {

    function get2vs2ArenaPrice() {
      // Price
      let price = (desired2vs2ArenaValue - current2vs2ArenaValue) * (price_of_2vs2 / MIN_DESIRED_VALUE);

      const total_Percentage = total_Percentage_value_arena();
      
      // Apply extra charges to the result
      price += price * total_Percentage;
    
      // Apply promo code 
      price -= price * (discount_amount / 100 )
    
      price = parseFloat(price.toFixed(2));
    
      // Current
      $('#current-2vs2 .current-2vs2-rp').html(current2vs2ArenaValue);
      $('.current-2vs2-selected-img').attr('src', `https://storage.googleapis.com/mad-boost.appspot.com/wow/images/${current2vs2Rank}.png`);
      $('.current.current-2vs2').removeClass().addClass(`current current-2vs2 rank-${current2vs2Rank}`);
      $('.current-2vs2-selected-info').html(`${current2vs2ArenaValue} MMR`)
    
      // Desired
      $('#desired-2vs2 .desired-2vs2-rp').html(desired2vs2ArenaValue);
      $('.desired-2vs2-selected-img').attr('src', `https://storage.googleapis.com/mad-boost.appspot.com/wow/images/${desired2vs2Rank}.png`);
      $('.desired.desired-2vs2').removeClass().addClass(`desired desired-2vs2 rank-${desired2vs2Rank}`);
      $('.desired-2vs2-selected-info').html(`${desired2vs2ArenaValue} MMR`)
    
      // Price
      $('#arena-2vs2-price').html(`$${price}`)
    
      // Form
      if ($('#arena-form').data('type') == 'arena2vs2') {
        $('#arena-form input[name="is_arena_2vs2"]').val(true);
        $('#arena-form input[name="current_rank"]').val(getRank(current2vs2ArenaValue)[1]);
        $('#arena-form input[name="current_RP"]').val(current2vs2ArenaValue);
        $('#arena-form input[name="desired_rank"]').val(getRank(desired2vs2ArenaValue)[1]);
        $('#arena-form input[name="desired_RP"]').val(desired2vs2ArenaValue);
        $('#arena-form input[name="server"]').val(selected2vs2ArenaServer);
        $('#arena-form input[name="price"]').val(price);
      }
      
    }
    
    function get3vs3ArenaPrice() {
      // Price
      let price = (desired3vs3ArenaValue - current3vs3ArenaValue) * (price_of_3vs3 / MIN_DESIRED_VALUE);
      
      const total_Percentage = total_Percentage_value_arena();

      // Apply extra charges to the result
      price += price * total_Percentage;
    
      // Apply promo code 
      price -= price * (discount_amount/100 )
    
      price = parseFloat(price.toFixed(2)); 
    
      // Current
      $('#current-3vs3 .current-3vs3-rp').html(current3vs3ArenaValue);
      $('.current-3vs3-selected-img').attr('src', `https://storage.googleapis.com/mad-boost.appspot.com/wow/images/${current3vs3Rank}.png`);
      $('.current.current-3vs3').removeClass().addClass(`current current-3vs3 rank-${current3vs3Rank}`);
      $('.current-3vs3-selected-info').html(`${current3vs3ArenaValue} MMR`)
    
      // Desired
      $('#desired-3vs3 .desired-3vs3-rp').html(desired3vs3ArenaValue);
      $('.desired-3vs3-selected-img').attr('src', `https://storage.googleapis.com/mad-boost.appspot.com/wow/images/${desired3vs3Rank}.png`);
      $('.desired.desired-3vs3').removeClass().addClass(`desired desired-3vs3 rank-${desired3vs3Rank}`);
      $('.desired-3vs3-selected-info').html(`${desired3vs3ArenaValue} MMR`)
    
      // Price
      $('#arena-3vs3-price').html(`$${price}`)
    
      if($('#arena-form').data('type') == 'arena3vs3') {
        // Form
        $('#arena-form input[name="is_arena_2vs2"]').val(false);
        $('#arena-form input[name="current_rank"]').val(getRank(current3vs3ArenaValue)[1]);
        $('#arena-form input[name="current_RP"]').val(current3vs3ArenaValue);
        $('#arena-form input[name="desired_rank"]').val(getRank(desired3vs3ArenaValue)[1]);
        $('#arena-form input[name="desired_RP"]').val(desired3vs3ArenaValue);
        $('#arena-form input[name="server"]').val(selected3vs3ArenaServer);
        $('#arena-form input[name="price"]').val(price);
      }
    }

  }

  get2vs2ArenaPrice()
  get3vs3ArenaPrice()
  // ----------------------------- Arena 2vs2 Boost Changes ---------------------------------
  current2vs2Arena.on("input", function (event) {
    current2vs2ArenaValue = Number(event.target.value);
    current2vs2Rank = getRank(current2vs2ArenaValue)[0];

    if((desired2vs2ArenaValue - current2vs2ArenaValue) < MIN_DESIRED_VALUE) {
      let newValue = current2vs2ArenaValue + MIN_DESIRED_VALUE;

      if(newValue > 2400) {
        newValue = 2400;
        current2vs2Arena.val(newValue - MIN_DESIRED_VALUE);
        current2vs2ArenaValue = newValue - MIN_DESIRED_VALUE;
        current2vs2Rank = getRank(current2vs2ArenaValue)[0];
      }
      desired2vs2Arena.val(newValue);
      desired2vs2ArenaValue = newValue;
      desired2vs2Rank = getRank(desired2vs2ArenaValue)[0];

      changeUI(desired2vs2ArenaValue, desired2vs2Arena, desired2vs2Steps);
    }
    
    changeUI(current2vs2ArenaValue, current2vs2Arena, current2vs2Steps)

    get2vs2ArenaPrice()

  })

  desired2vs2Arena.on("input", function (event) {
    desired2vs2ArenaValue = Number(event.target.value);
    desired2vs2Rank = getRank(desired2vs2ArenaValue)[0];

    if((desired2vs2ArenaValue - current2vs2ArenaValue) < MIN_DESIRED_VALUE) {
      let newValue = current2vs2ArenaValue + MIN_DESIRED_VALUE;

      if(newValue > 2400) {
        newValue = 2400;
        current2vs2Arena.val(newValue - MIN_DESIRED_VALUE);
        current2vs2ArenaValue = newValue - MIN_DESIRED_VALUE;
        current2vs2Rank = getRank(current2vs2ArenaValue)[0];
      }
      desired2vs2Arena.val(newValue);
      desired2vs2ArenaValue = newValue;
      desired2vs2Rank = getRank(desired2vs2ArenaValue)[0];

      changeUI(desired2vs2ArenaValue, desired2vs2Arena, desired2vs2Steps);
    }
    
    if (extend_order && extends_from_2vs2 && desired2vs2ArenaValue < valuesToSet[4]) {
      desired2vs2Arena.val(valuesToSet[4])
      desired2vs2ArenaValue = valuesToSet[4];
      desired2vs2Rank = getRank(desired2vs2ArenaValue)[0];
      changeUI(desired2vs2ArenaValue, desired2vs2Arena, desired2vs2Steps);
    }

    changeUI(desired2vs2ArenaValue, desired2vs2Arena, desired2vs2Steps);

    get2vs2ArenaPrice()

  })

  // Server Changes
  arena_2vs2_server_select_element.on("change", function() {
    selected2vs2ArenaServer = $(this).val();
    $('#arena-form input[name="server"]').val(selected2vs2ArenaServer);
  });

  // ----------------------------- Arena 3vs3 Boost Changes ---------------------------------
  current3vs3Arena.on("input", function (event) {
    current3vs3ArenaValue = Number(event.target.value);
    current3vs3Rank = getRank(current3vs3ArenaValue)[0];

    if((desired3vs3ArenaValue - current3vs3ArenaValue) < MIN_DESIRED_VALUE) {
      let newValue = current3vs3ArenaValue + MIN_DESIRED_VALUE;

      if(newValue > 2400) {
        newValue = 2400;
        current3vs3Arena.val(newValue - MIN_DESIRED_VALUE);
        current3vs3ArenaValue = newValue - MIN_DESIRED_VALUE;
        current3vs3Rank = getRank(current3vs3ArenaValue)[0];
      }
      desired3vs3Arena.val(newValue);
      desired3vs3ArenaValue = newValue;
      desired3vs3Rank = getRank(desired3vs3ArenaValue)[0];

      changeUI(desired3vs3ArenaValue, desired3vs3Arena, desired3vs3Steps);
    }
    
    changeUI(current3vs3ArenaValue, current3vs3Arena, current3vs3Steps)


    get3vs3ArenaPrice()

  })

  desired3vs3Arena.on("input", function (event) {
    desired3vs3ArenaValue = Number(event.target.value);
    desired3vs3Rank = getRank(desired3vs3ArenaValue)[0];

    if((desired3vs3ArenaValue - current3vs3ArenaValue) < MIN_DESIRED_VALUE) {
      let newValue = current3vs3ArenaValue + MIN_DESIRED_VALUE;

      if(newValue > 2400) {
        newValue = 2400;
        current3vs3Arena.val(newValue - MIN_DESIRED_VALUE);
        current3vs3ArenaValue = newValue - MIN_DESIRED_VALUE;
        current3vs3Rank = getRank(current3vs3ArenaValue)[0];
      }
      desired3vs3Arena.val(newValue);
      desired3vs3ArenaValue = newValue;
      desired3vs3Rank = getRank(desired3vs3ArenaValue)[0];

      changeUI(desired3vs3ArenaValue, desired3vs3Arena, desired3vs3Steps);
    }

    if (extend_order && !extends_from_2vs2 && desired3vs3ArenaValue < valuesToSet[4]) {
      desired3vs3Arena.val(valuesToSet[4])
      desired3vs3ArenaValue = valuesToSet[4];
      desired3vs3Rank = getRank(desired3vs3ArenaValue)[0];
      changeUI(desired3vs3ArenaValue, desired3vs3Arena, desired3vs3Steps);
    }
    
    changeUI(desired3vs3ArenaValue, desired3vs3Arena, desired3vs3Steps);

    get3vs3ArenaPrice()

  })

  // Server Changes
  arena_3vs3_server_select_element.on("change", function() {
    selected3vs3ArenaServer = $(this).val();
    $('#arena-form input[name="server"]').val(selected3vs3ArenaServer);
  });


  // Extra Buttons
extraOptions.forEach(function (checkbox, index) {
  checkbox.addEventListener('change', function () {
      get2vs2ArenaPrice();
      get3vs3ArenaPrice();
  })
});

promo_form.addEventListener('submit', async function(event) {
  event.preventDefault();  
  if(!extend_order) {
      discount_amount = await fetch_promo(); 
      get2vs2ArenaPrice();
      get3vs3ArenaPrice()
  }
});


}); // end of document ready


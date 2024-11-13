document.addEventListener("DOMContentLoaded", function () {
  const ranks = ["UNRANK", "0-1599", "1600-1799", "1800-2099", "2100-2499"];
  const MIN_DESIRED_VALUE = 50;
  const getRank = (rp) => {
    if (rp >= 2100) {
      return [ranks[4], 4];
    }

    if (rp >= 1800 && rp < 2100) {
      return [ranks[3], 3];
    }

    if (rp >= 1600 && rp < 1799) {
      return [ranks[2], 2];
    }

    if (rp < 1600) {
      return [ranks[1], 1];
    }
  }

  const total_Percentage_value_arena = () => {
    const extraCheckbox = document.getElementsByName("extra-checkbox");
    let total_Percentage = 0;
    extraCheckbox.forEach((checkbox) => {
      if (checkbox.checked) {
        if (!["loot_priority", "timed"].includes(checkbox.id)) {
          total_Percentage += parseInt(checkbox.value);
        }
      }
    });
    return total_Percentage / 100;
  };

  const prices = document.getElementById("WorldOfWarcraftRpsPrice");
  const price_of_2vs2 = parseFloat(prices.dataset.rp2vs2);
  const price_of_3vs3 = parseFloat(prices.dataset.rp3vs3);

  const current2v2Input = document.getElementById('current-2v2-input');
  const current2v2Range = document.getElementById('current-2v2-range');
  const desired2v2Input = document.getElementById('desired-2v2-input');
  const desired2v2Range = document.getElementById('desired-2v2-range');

  const current3v3Input = document.getElementById('current-3v3-input');
  const current3v3Range = document.getElementById('current-3v3-range');
  const desired3v3Input = document.getElementById('desired-3v3-input');
  const desired3v3Range = document.getElementById('desired-3v3-range');


  const setArenaData = (price, current, desired, name) => {
    const form = document.getElementById(`arena-${name}-form`);

    $(form).find('input[name="price"]').val(price);
    $(form).find('input[name="current_RP"]').val(current);
    $(form).find('input[name="desired_RP"]').val(desired);
    
    $(`#arena-${name}-price`).html(`$${price}`);

    // Current
    $(`.current-${name}-selected-img`).attr(
      "src",
      `https://storage.googleapis.com/mad-boost.appspot.com/wow/images/${getRank(current)[0]}.png`
    );
    $(`.current.current-${name}`)
      .removeClass()
      .addClass(`current current-${name} rank-${getRank(current)[0]}`);
    $(`.current-${name}-selected-info`).html(`${current} MMR`);

    // Desired
    $(`.desired-${name}-selected-img`).attr(
      "src",
      `https://storage.googleapis.com/mad-boost.appspot.com/wow/images/${getRank(desired)[0]}.png`
    );
    $(`.desired.desired-${name}`)
      .removeClass()
      .addClass(`desired desired-${name} rank-${getRank(desired)[0]}`);
    $(`.desired-${name}-selected-info`).html(`${desired} MMR`);
  }

  function getArenaPrice(currentValue, desiredValue, name) {
    let price_of_arena = 0;
    let boost_metod_value = 0;
    if (name === '2vs2') {
      price_of_arena = price_of_2vs2;
    } else if (name === '3vs3') {
      price_of_arena = price_of_3vs3;
    }else{
      console.error('Wrong name');
    }
    const boost_method = document.getElementsByName(`boost-method-arena${name}`);
    if (boost_method[2].checked) {
      boost_metod_value = 0.3;
    } 
    let point_number = (desiredValue - currentValue) 
    if (point_number < 0) {
      point_number = 0
    }
    let price = point_number * (price_of_arena / MIN_DESIRED_VALUE);

    const total_Percentage = total_Percentage_value_arena();
    const new_total_Percentage = total_Percentage + boost_metod_value;

    // Apply extra charges to the result
    price += price * new_total_Percentage;

    // Apply promo code
    price = setPromoAmount(price, discount_amount)

    price = parseFloat(price.toFixed(2));
    setArenaData(price, currentValue, desiredValue, name);
  }

  // Arena2v2
  MadBoostInputAndRange(current2v2Input, current2v2Range, () => getArenaPrice(current2v2Range.value, desired2v2Range.value, '2vs2'));
  MadBoostInputAndRange(desired2v2Input, desired2v2Range, () => getArenaPrice(current2v2Range.value, desired2v2Range.value, '2vs2'));

  // // Arena3v3
  MadBoostInputAndRange(current3v3Input, current3v3Range, () => getArenaPrice(current3v3Range.value, desired3v3Range.value, '3vs3'));
  MadBoostInputAndRange(desired3v3Input, desired3v3Range, () => getArenaPrice(current3v3Range.value, desired3v3Range.value, '3vs3'));

  setBoostMethod('arena2vs2', () => getArenaPrice(current2v2Range.value, desired2v2Range.value, '2vs2'));
  setBoostMethod('arena3vs3', () => getArenaPrice(current3v3Range.value, desired3v3Range.value, '3vs3'));

  // server select
  const server2vs2 = document.getElementById('arena-2vs2-servers-select');
  const server3vs3 = document.getElementById('arena-3vs3-servers-select');

  // on change set server val in form 
  server2vs2.addEventListener("change", function () {
    const form = document.getElementById('arena-2vs2-form');
    $(form).find('input[name="server"]').val(server2vs2.value);
  })

  server3vs3.addEventListener("change", function () {
    const form = document.getElementById('arena-3vs3-form');
    $(form).find('input[name="server"]').val(server3vs3.value);
  })



  // Extra Buttons
  extraOptions.forEach(function (checkbox, index) {
    checkbox.addEventListener("change", function () {
      getArenaPrice(current2v2Range.value, desired2v2Range.value, '2vs2');
      getArenaPrice(current3v3Range.value, desired3v3Range.value, '3vs3');
    });
  });

  promo_form.addEventListener("submit", async function (event) {
    event.preventDefault();
    if (!extend_order) {
      discount_amount = await fetch_promo();
      getArenaPrice(current2v2Range.value, desired2v2Range.value, '2vs2');
      getArenaPrice(current3v3Range.value, desired3v3Range.value, '3vs3');
    }
  });
});

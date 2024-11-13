document.addEventListener('DOMContentLoaded', function() {
    const currentLevelUpInput = document.getElementById('current-level-up-input');
    const currentLevelUpRange = document.getElementById('current-level-up-range');

    const desiredLevelUpInput = document.getElementById('desired-level-up-input');
    const desiredLevelUpRange = document.getElementById('desired-level-up-range');

    const levelForm = document.getElementById('level-up-form');

    const level_price_div = document.getElementById('level-up-price-container');
    const level_price = parseInt(level_price_div.dataset.price);

    const total_Percentage_value_levelup = ()=>{
        const extraCheckbox = document.getElementsByName('extra-checkbox');
        let total_Percentage = 0
        extraCheckbox.forEach((checkbox) => {
        if (checkbox.checked) {
            if (!['loot-priority', 'timed', 'tournament', 'rank1'].includes(checkbox.id)) {
            total_Percentage += parseInt(checkbox.value);
            }
        }
        })
        return (total_Percentage / 100)
    }
    
    const details_set = (price) => {
        $('.current-level-up-selected-info').html(`level ${currentLevelUpRange.value}`);
        $('.desired-level-up-selected-info').html(`level ${desiredLevelUpRange.value}`);
        $('#level-up-price').html(`$${price}`);

        // form data
        $(levelForm).find('input[name="price"]').val(price);
        $(levelForm).find('input[name="current_level"]').val(currentLevelUpRange.value);
        $(levelForm).find('input[name="desired_level"]').val(desiredLevelUpRange.value);
    }

    const getLevePrice = () =>{
        const total_Percentage = total_Percentage_value_levelup();
        numberOfLevels = desiredLevelUpRange.value - currentLevelUpInput.value;

        if (numberOfLevels < 0) {
            numberOfLevels = 0;
        }

        price = numberOfLevels * level_price;
        priceWithPercentage = (price * total_Percentage) + price;
        // Apply promo code
        priceWithPercentage = setPromoAmount(priceWithPercentage, discount_amount)

        Fullprice = parseFloat(priceWithPercentage.toFixed(2));

        details_set(Fullprice);
        return Fullprice;
    }
    
    getLevePrice();
    MadBoostInputAndRange(currentLevelUpInput, currentLevelUpRange, getLevePrice);
    MadBoostInputAndRange(desiredLevelUpInput, desiredLevelUpRange, getLevePrice);



    // Extra Buttons
    extraOptions.forEach(function (checkbox, index) {
        checkbox.addEventListener('change', function () {
            const form_input_name = document.getElementsByName(checkbox.id);
            if (checkbox.checked) {
                form_input_name.forEach((input) => {
                    input.value = true;
                })
            }
            else {
                form_input_name.forEach((input) => {
                    input.value = false;
                })
            }
            getLevePrice();
        })
    });

    promo_form.addEventListener('submit', async function(event) {
        event.preventDefault();  
        discount_amount = await fetch_promo(); 
        getLevePrice()
    });

    
    const levelUpServer = document.getElementById('level-up-servers-select');
    if (levelUpServer) {
        levelUpServer.addEventListener('change', function () {
            $(levelForm).find('input[name="server"]').val(levelUpServer.value);
        });
    }
    
});
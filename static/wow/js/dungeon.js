    const dungeonForm = document.getElementById('dungeon-simple-form');
    const dungeonBundleForm = document.getElementById('dungeon-bundle-form');
    const keynumbersNumberInput = document.getElementById('keynumbers-number-input');
    const keynumbersRangeInput = document.getElementById('keynumbers-range-input');
    const counterBtns = document.querySelectorAll('.counter button');
    const keystoneNumberInput = document.getElementById('keystone-number-input');
    const keystoneRangeInput = document.getElementById('keystone-range-input');
    const dungeon_maps_selector = document.getElementById('dungeon-maps-selector');
    const mapPreferred = document.getElementsByName('map-preferred-selector');
    const tradersSelector = document.getElementsByName('traders');
    const armorTypeDiv = document.getElementById('armor-type');
    const dungeonServerRadio = document.getElementsByName('dungeon-server');
    const armorTypeSelect = document.getElementById('armor-type-select');

    const dungeon_keystone_info = document.getElementById('dungeon-keystone-info');
    const dungeon_keys_info = document.getElementById('dungeon-keys-info');
    const dungeon_traders_info = document.getElementById('dungeon-traders-info');
    const dungeon_server_info = document.getElementById('dungeon-server-info');

    const dungeon_prices_container = document.getElementById('dungeon-prices-container');
    const keyStonePrice = dungeon_prices_container.dataset.prices;
    const keyStonePriceList = keyStonePrice
        .replace(/[\[\]]/g, '')  // Remove the square brackets
        .split(',')              // Split by commas
        .map(Number);            // Convert each element to a float
    let mainMapCount = 0;

    // simple function to Get selected radio value
    const getSelectedRadioValue = (radios) => {
        for (let radio of radios) {
            if (radio.checked) {
                return radio.value;
            }
        }
    }

    const total_Percentage_value_dungeon = ()=>{
        const extraCheckbox = document.getElementsByName('extra-checkbox');
        let total_Percentage = 0
        extraCheckbox.forEach((checkbox) => {
        if (checkbox.checked) {
            if (!['loot-priority', 'tournament', 'rank1'].includes(checkbox.id)) {
            total_Percentage += parseInt(checkbox.value);
            }
        }
        })
        return (total_Percentage / 100)
    }


    
    const SetMapCount = () => {
        const maps = document.querySelectorAll('.map-count');
        maps.forEach((map) => {
            const value = map.getAttribute('data-value')
            const id = map.getAttribute('id')
            $(dungeonForm).find(`input[name="${id}"]`).val(value);
        })
    }

    armorTypeSelect.addEventListener('change', () => {
        $(dungeonForm).find(`input[name="traders_armor_type"]`).val(armorTypeSelect.value);
    });

    // start counter 
    counterBtns.forEach(button => {
        button.addEventListener('click', function() {
            // Get the associated span and current count
            const span = this.parentElement.querySelector('span');
            let count = parseInt(span.textContent);
            let dataValue = span.getAttribute('data-value');
            
            // Increment or decrement based on button clicked
            if (this.id.startsWith('increment')) {
                if (keynumbersRangeInput.value > mainMapCount ){
                    count++;
                    mainMapCount++;
                    dataValue++;
                } 
            } else if (this.id.startsWith('decrement')) {
                if (count > 0) {
                    count--;
                    mainMapCount--;
                    dataValue--;
                }
            }

            // Update the span with the new count
            span.textContent = count;
            span.setAttribute('data-value', dataValue);
            SetMapCount();
        });
    });
    // end counter

    // start keystone Range and Number input
    keystoneNumberInput.addEventListener('input', function () {
        keystoneChange(keystoneNumberInput.value);
    });

    keystoneRangeInput.addEventListener('input', function () {
        keystoneChange(keystoneRangeInput.value);
    });
    const keystoneChange = (strValue) => {
        let value = parseInt(strValue, 10);
        if (isNaN(value)) {
            value = 0;
        }
        if  ((value) > 20){
            value = 20;
        }
        else if ((value) < 0) {
            value = 0;
        }else if (value === 1) {
            value = 2;
        }
        keystoneNumberInput.value = value;
        keystoneRangeInput.value = value;
        dungeon_keystone_info.innerHTML = value;
        getDungeonSimplePrice();
    };
    // end keystone Range and Number input

    // start keynumbers Range and Number input
    keynumbersNumberInput.addEventListener('input', function () {
        keynumbersChange(keynumbersNumberInput.value);
    });

    keynumbersRangeInput.addEventListener('input', function () {
        keynumbersChange(keynumbersRangeInput.value);
    });
    const keynumbersChange = (strValue) => {
        let value = parseInt(strValue, 10);
        if (isNaN(value)) {
            value = 1;
            counterBtns.forEach(button => {
                button.parentElement.querySelector('span').textContent = 0;
                button.parentElement.querySelector('span').setAttribute('data-value', 0);
            });
            SetMapCount();
            mainMapCount = 0
        }
        if (value < mainMapCount){
            value = mainMapCount
        }
        if  ((value) > 20){
            value = 20;
        }
        else if ((value) < 1) {
            value = 1;
        }
        keynumbersNumberInput.value = value;
        keynumbersRangeInput.value = value;
        dungeon_keys_info.innerHTML = value;
        getDungeonSimplePrice();
    };
    // end keynumbers Range and Number input



    // start map preferred
    mapPreferred.forEach(radio => {
        radio.addEventListener('change', function () {
            const value = getSelectedRadioValue(mapPreferred);
            if (value === 'Random') {
                dungeon_maps_selector.classList.add('d-none');
                counterBtns.forEach(button => {
                    button.parentElement.querySelector('span').textContent = 0;
                    button.parentElement.querySelector('span').setAttribute('data-value', 0);
                });
                SetMapCount();
                mainMapCount = 0
            } else if (value === 'Specific') {
                dungeon_maps_selector.classList.remove('d-none');
            }
            $(dungeonForm).find(`input[name="map_preferred"]`).val(value);
            getDungeonSimplePrice();
        })
    })
    // end map preferred

    // start traders
    tradersSelector.forEach(radio => {
        radio.addEventListener('change', function () {
            const value = getSelectedRadioValue(tradersSelector)
            if (value === 'Personal Loot') {
                armorTypeDiv.classList.add('d-none');
            } else {
                armorTypeDiv.classList.remove('d-none');
            }
            $(dungeonForm).find(`input[name="traders"]`).val(value);
            dungeon_traders_info.innerHTML = value;
            getDungeonSimplePrice();
        })
    })
    // end traders

    
    const getDungeonSimplePrice = () => {
        let boost_metod_value = 0
        const boost_method = document.getElementsByName(`boost-method-dungeon`);
        if (boost_method[2].checked) {
          boost_metod_value = 0.3;
        } 

        let extra_value = 0
        const keystoneValue = keystoneNumberInput.value
        const keynumbersValue = keynumbersNumberInput.value
        const KayesWithKaysPrice = keynumbersValue * keyStonePriceList[keystoneValue]

        const tradersValue = getSelectedRadioValue(tradersSelector)
        if (tradersValue === 'Personal Loot') {
            extra_value += 0
        } else if (tradersValue === '1 trader') {
            extra_value += 0.15
        }else if (tradersValue === '2 trader') {
            extra_value += 0.30
        }else if (tradersValue === '3 trader') {
            extra_value += 0.40
        }else if (tradersValue === 'full-Priority') {
            extra_value += 0.50
        }
        const mapDungeon = getSelectedRadioValue(mapPreferred); 

        if (mapDungeon === 'Random') {
            extra_value += 0
        } else if (mapDungeon === 'Specific') {
            extra_value += 0.05
        }
        const total_Percentage_price = total_Percentage_value_dungeon()
        const new_percentage  = extra_value + total_Percentage_price + boost_metod_value
        let result = KayesWithKaysPrice + (KayesWithKaysPrice * new_percentage)

        // Apply promo code
        result = setPromoAmount(result, discount_amount)

        result = parseFloat(result.toFixed(2));
            
        $('#dungeon-price').text(`$${result}`)
        $(dungeonForm).find('input[name="price"]').val(result);
        $(dungeonForm).find('input[name="keystone"]').val(keystoneValue);
        $(dungeonForm).find('input[name="keys"]').val(keynumbersValue);
        
        SetMapCount();

    }


    getDungeonSimplePrice()
    
    function getSelectedDungeonServer() {
        let selectedValue;
        // Loop through the radio buttons to find the checked one
        for (const radio of dungeonServerRadio) {
            if (radio.checked) {
                selectedValue = radio.value;
                break;
            }
        }
        dungeon_server_info.innerHTML = selectedValue;
        $(dungeonForm).find('input[name="server"]').val(selectedValue);
        $(dungeonBundleForm).find('input[name="server"]').val(selectedValue);
        return selectedValue;
    }
    getSelectedDungeonServer()

    dungeonServerRadio.forEach((radio) => {
        radio.addEventListener('change', function () {
            getSelectedDungeonServer();
        })
    })

    setBoostMethod('dungeon', getDungeonSimplePrice);

// Extra Buttons
extraOptions.forEach(function (checkbox, index) {
    checkbox.addEventListener('change', function () {
        getDungeonSimplePrice()
    })
  });
  
promo_form.addEventListener('submit', async function(event) {
    event.preventDefault();  
    if(!extend_order) {
        discount_amount = await fetch_promo(); 
        getDungeonSimplePrice()
    }
});
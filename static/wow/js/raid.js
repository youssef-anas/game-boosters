document.addEventListener("DOMContentLoaded", function () {
    let bandelPrice = 0;
    let selectedBundel_id = 0;

    const get_checked_mode = () => {
        const radio = document.querySelector('input[type="radio"][name="radio-group-type"]:checked');
        return radio.id
    }
    const scrollToChoiseDiv = () => {
        const choiseDiv = document.getElementById('choise-div');
        const offset = 30; // Offset in pixels
        const elementPosition = choiseDiv.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.scrollY - offset;
    
        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    };

    const total_percentage_value_raid = () => {
        const extraCheckbox = document.getElementsByName("extra-checkbox");
        let total_Percentage = 0;
        extraCheckbox.forEach((checkbox) => {
          if (checkbox.checked) {
            if (!["rank1_player", "timed", "tournament_player"].includes(checkbox.id)) {
              total_Percentage += parseInt(checkbox.value);
            }
          }
        });
        return total_Percentage / 100;
      };

    // ------------------------

    const applyBandelsBtns = document.querySelectorAll('.apply-bandel')
    const removeBandelsBtns = document.querySelectorAll('.remove-bandel-btn')
    const removeBandelDiv = document.getElementById('remove-bandel-div')
    const bandelViewDiv = document.getElementById('bandel-view-div')
    const mainRemoveBandelBtn = document.getElementById('main-remove-bandel-btn')
    const awakenedRaidDiv = document.getElementById('awakened-raids-div')
    const awakened_raid_difficulty = document.getElementById('awakened-raid-difficulty')
    const bossesSelectDiv = document.getElementById('bosses-select-div')
    const raidPrice = document.getElementById('raid-price')
    const difficultyRadio = document.querySelectorAll('input[type="radio"][name="difficulty"]');
    const mapSelection = document.querySelectorAll('input[type="radio"][name="map"]');
    const bossesList = document.querySelectorAll('.bosses-list-with-checkboxes')

    const raid_bundle_info = document.getElementById('raid-bundle-info');
    const raid_difficulty_info = document.getElementById('raid-difficulty-info');

    // forms
    const raidForm = document.getElementById('raid-simple-form');
    const raidBundleForm = document.getElementById('raid-bundle-form');

    bossesList.forEach(function(container) {
        checkFirstCheckbox(container);
        const checkboxes = container.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(function(checkbox) {
            checkbox.addEventListener('change', function() {
                getRaidPrice();
            });
        });

    });

    const getSelectedMap = () => {
        let selectedMap = null;
        mapSelection.forEach((map) => {
            if (map.checked) {
                selectedMap = map.value
            }
        })
        return selectedMap
    }

    const toggleViewBosses = () => {
        const map = getSelectedMap();
        if (get_checked_mode() === 'raid') {
            bossesList.forEach((bosses) => {
                if (bosses.id == map) {
                    bosses.classList.remove('d-none')
                }else{
                    bosses.classList.add('d-none')
                }
            })
        }
    }
    toggleViewBosses();

    mapSelection.forEach((map) => {
        map.addEventListener('change', function () {
            toggleViewBosses();
            getRaidPrice();
        })
    })


    const removeBandelBtnAction = () => {
        raid_difficulty_info.classList.remove('d-none')
        raid_bundle_info.classList.add('d-none')
        awakened_raid_difficulty.classList.remove('d-none')
        removeBandelDiv.classList.add('d-none')
        bandelViewDiv.classList.add('d-none')
        awakenedRaidDiv.classList.remove('d-none')
        bossesSelectDiv.classList.remove('d-none')
        raidBundleForm.classList.add('d-none')
        raidForm.classList.remove('d-none')
        toggleViewBosses()

        removeBandelsBtns.forEach((removeBtn) => {
            removeBtn.classList.add('d-none')
        });
        applyBandelsBtns.forEach((applyBtn) => {
            applyBtn.classList.remove('d-none')
        })
        bandelPrice = 0
        getRaidPrice();
    }

    const applyBandelBtnAction = () => {
        raid_difficulty_info.classList.add('d-none')
        raid_bundle_info.classList.remove('d-none')
        awakened_raid_difficulty.classList.add('d-none')
        removeBandelDiv.classList.remove('d-none')
        bandelViewDiv.classList.remove('d-none')
        awakenedRaidDiv.classList.add('d-none')
        bossesSelectDiv.classList.add('d-none')
        raidBundleForm.classList.remove('d-none')
        raidForm.classList.add('d-none')
        // TODO get selected map then view only bosses with that map
        bossesList.forEach((bosses) => {
            bosses.classList.add('d-none')
        })

        // wait 2 seconds
        setTimeout(() => {
            scrollToChoiseDiv();
        }, 200); 
    }


    removeBandelsBtns.forEach((btn) => {
        btn.addEventListener('click', function () {
            removeBandelBtnAction();
        })
    })

    mainRemoveBandelBtn.addEventListener('click', function () {
        removeBandelBtnAction();
    })


    applyBandelsBtns.forEach((btn) => {
        btn.addEventListener('click', (event) => {
            selectedBundel_id = btn.id;
            removeBandelsBtns.forEach((removeBtn) => {
                if (removeBtn.id == btn.id){
                    removeBtn.classList.remove('d-none')
                    applyBandelBtnAction();
                }else{
                    removeBtn.classList.add('d-none')
                }
            });
            applyBandelsBtns.forEach((applyBtn) => {
                if (applyBtn.id == btn.id){
                    applyBtn.classList.add('d-none')
                } else {
                    applyBtn.classList.remove('d-none')
                }
            })

            const bundleDiv = event.target.closest('.swiper-slide');
            const price = bundleDiv.querySelector('h2').innerText;
            const bundleName = bundleDiv.querySelector('h3:nth-of-type(2)').innerText;
            const features = Array.from(bundleDiv.querySelectorAll('.texts-bandel p')).map(p => p.innerText);
            const backgroundImage = getComputedStyle(bundleDiv).backgroundImage;
            // conver price to float
            bandelPrice = parseFloat(price.replace('$', ''));
            updateBandelView(bundleName, features, backgroundImage);
            raid_bundle_info.innerText = bundleName;
            getRaidPrice();
        })
    })
    
    const updateBandelView = (bundleName, features, backgroundImage) => {
        const bandelViewDiv = document.getElementById('bandel-view-div');
    
        // Update the bundle name
        bandelViewDiv.querySelector('h5').innerText = bundleName;
    
        // Clear and update the features list
        const textsBandelDiv = bandelViewDiv.querySelector('.texts-bandel');
        textsBandelDiv.innerHTML = '';  
    
        features.forEach(feature => {
            const p = document.createElement('p');
            p.classList.add('my-auto', 'py-2');
            p.innerHTML = `<i class="fa-solid fa-check"></i>${feature}`;
            textsBandelDiv.appendChild(p);
        });

        // Update the background image
        const imageBorder = document.querySelector('.image-border img');
        imageBorder.src = getImgPathFromUrl(backgroundImage);
    }

    const getRaidPrice = () => {
        let boost_metod_value = 0;
        let raidMainPrice = 0;
        const boost_method = document.getElementsByName(`boost-method-raid`);
        if (boost_method[2].checked) {
          boost_metod_value = 0.3;
        } 
        if (bandelPrice == 0) {
            const map = getSelectedMap();
            const checkboxes = document.querySelectorAll(`input[type="checkbox"][name="${map}-bossescheckboxes"]`);
            const bossesSelected = [];

            checkboxes.forEach((checkbox) => {
                if (checkbox.checked) {
                    const value = parseFloat(checkbox.value);
                    raidMainPrice += value;
                    bossesSelected.push(checkbox.id);
                }
            })
            const difficultyValue = getSelectedDifficulty();
            const new_total_Percentage = total_percentage_value_raid() + difficultyValue + boost_metod_value;

            

            // Apply extra charges to the result
            raidMainPrice += raidMainPrice * new_total_Percentage;
            // Apply promo code 
            raidMainPrice = setPromoAmount(raidMainPrice, discount_amount)
            raidMainPrice = parseFloat(raidMainPrice.toFixed(2)); 

            const visualPrice = "$" + raidMainPrice
            raidPrice.innerText = visualPrice


            // raid simple form 
            $(raidForm).find('input[name="price"]').val(raidMainPrice);
            $(raidForm).find('input[name="map"]').val(map);
            $(raidForm).find('input[name="bosses"]').val(bossesSelected);
            $(raidForm).find('input[name="difficulty_chosen"]').val(difficultyValue);

        }else{
            let price = bandelPrice;
            const new_total_Percentage = total_percentage_value_raid() + boost_metod_value;

            // Apply extra charges to the result
            price += price * new_total_Percentage;
            // Apply promo code 
            price -= price * (discount_amount/100 )
            price = parseFloat(price.toFixed(2)); 

            const visualPrice = "$" + price
            raidPrice.innerText = visualPrice


            // raid bundle form
            $(raidBundleForm).find('input[name="price"]').val(price);
            $(raidBundleForm).find('input[name="bundle_id"]').val(selectedBundel_id);
        }

    }

    setBoostMethod('raid', getRaidPrice);


    // function get selected difficulty value
    const getSelectedDifficulty = () => {
        let selectedValue = null;
        difficultyRadio.forEach((radio) => {
            if (radio.checked) {
                selectedValue = parseFloat(radio.value);
                raid_difficulty_info.innerHTML = radio.id;
            }
        });
        return selectedValue;
    }

    const raidServerRadio = document.getElementsByName('raid-server');
    const raid_server_info = document.getElementById('raid-server-info');
    const getSelectedRaidServer = () => {
        let selectedValue;
        // Loop through the radio buttons to find the checked one
        for (const radio of raidServerRadio) {
            if (radio.checked) {
                selectedValue = radio.value;
                raid_server_info.innerHTML = radio.value;
                break;
            }
        }
        $(raidForm).find('input[name="server"]').val(selectedValue);
        $(raidBundleForm).find('input[name="server"]').val(selectedValue);
        return selectedValue;
    }
    getSelectedRaidServer()

    raidServerRadio.forEach((radio) => {
        radio.addEventListener('change', function () {
            getSelectedRaidServer();
        })
    })


    difficultyRadio.forEach((radio) => {
        radio.addEventListener('change', function () {
            getRaidPrice();
        })
    })


    // Extra Buttons
    extraOptions.forEach(function (checkbox, index) {
        checkbox.addEventListener("change", function () {
            getRaidPrice();
        });
    });

    promo_form.addEventListener("submit", async function (event) {
        event.preventDefault();
        if (!extend_order) {
            discount_amount = await fetch_promo();
            getRaidPrice();
        }
    });

    const radioModesBtns= document.querySelectorAll('input[type="radio"][name="radio-group-type"]');

    radioModesBtns.forEach((radio) => {
        radio.addEventListener('change', function () {
            if (get_checked_mode() === 'raid') {
                raidForm.classList.remove('d-none') 
            }else{
                removeBandelBtnAction();
                raidForm.classList.add('d-none')
                bossesSelectDiv.classList.add('d-none')
            }
        })
    })
    getRaidPrice();
    
});
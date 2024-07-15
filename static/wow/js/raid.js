document.addEventListener("DOMContentLoaded", function () {
    const bosses_btn = document.getElementById('view-bosses');
    const bosses = document.getElementById('popup-bosses-form');
    const close_bosses = document.getElementById('close-booses');
    const piloted = document.getElementById('piloted-checkbox');
    const selfplay = document.getElementById('selfplay-checkbox');
    let bandelPrice = 0;
    let selectedBundel_id = 0;

    const closeBoosesForm = () => {
        bosses.style.display = 'none';
    }
    const openBoosesForm = () => {
        bosses.style.display = 'block';
    }
    const toggleBoosesForm = () => {
        if (bosses.style.display === 'none') {
            openBoosesForm();
        } else {
            closeBoosesForm();
        }
    }

    bosses_btn.addEventListener('click', function () {
        toggleBoosesForm();
    })
    close_bosses.addEventListener('click', function () {
        closeBoosesForm();
    })

    const selfplayandpilotedSwitch = (value) => {
        if (value === 'selfplay') {
            if (selfplay.checked) {
                piloted.checked = false;
                selfplay.checked = true;
            }else{
                piloted.checked = true;
                selfplay.checked = false;
            }
        }
        else{
            if (piloted.checked) {
                selfplay.checked = false;
                piloted.checked = true;
            }else{
                selfplay.checked = true;
                piloted.checked = false;
            }
        }
    }

    selfplay.addEventListener('change', function () {
        selfplayandpilotedSwitch(this.value);
    })
    piloted.addEventListener('change', function () {
        selfplayandpilotedSwitch(this.value);
    })

    // Initialize the checkboxes to ensure one is checked and the other is unchecked
    selfplayandpilotedSwitch('piloted');


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

    // ------------------------

    const applyBandelsBtns = document.querySelectorAll('.apply-bandel')
    const removeBandelsBtns = document.querySelectorAll('.remove-bandel-btn')
    const removeBandelDiv = document.getElementById('remove-bandel-div')
    const bandelViewDiv = document.getElementById('bandel-view-div')
    const mainRemoveBandelBtn = document.getElementById('main-remove-bandel-btn')
    const awakenedRaidDiv = document.getElementById('awakened-raids-div')
    const bossesSelectDiv = document.getElementById('bosses-select-div')
    const raidPrice = document.getElementById('raid-price')
    const difficultyRadio = document.querySelectorAll('input[type="radio"][name="difficulty"]');
    const mapSelection = document.querySelectorAll('input[type="radio"][name="map"]');
    const bossesList = document.querySelectorAll('.bosses-list-with-checkboxes')

    // forms
    const raidForm = document.getElementById('raid-simple-form');
    const raidBundleForm = document.getElementById('raid-bundle-form');
    
    // Function to find and check the first checkbox in a container
    function checkFirstCheckbox(container) {
        // Find all checkboxes within the container
        const checkboxes = container.querySelectorAll('input[type="checkbox"]');
        
        // Iterate through checkboxes to find the first one and check it
        for (let i = 0; i < checkboxes.length; i++) {
            if (i === 0) {
                checkboxes[i].checked = true;
            }
        }
    }

    // Iterate through each bossesList container
    bossesList.forEach(function(container) {
        checkFirstCheckbox(container);

        // Add event listener to each checkbox
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
        bossesList.forEach((bosses) => {
            if (bosses.id == map) {
                bosses.classList.remove('d-none')
            }else{
                bosses.classList.add('d-none')
            }
        })
    }
    toggleViewBosses();

    mapSelection.forEach((map) => {
        map.addEventListener('change', function () {
            toggleViewBosses();
            getRaidPrice();
        })
    })


    const removeBandelBtnAction = () => {
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
            getRaidPrice();
        })
    })


    const getImgPathFromUrl=(backgroundImage)=> {
        // extract path from backgroundImage
        const path = backgroundImage.match(/url\((.*)\)/)[1];
        // replace &quot; with "
        const newPath = path.replace(/&quot;/g, '"');
        // replace url(" with ""
        const newPath2 = newPath.replace(/url\((.*)\)/, '$1');
        // replace " with ""
        const newPath3 = newPath2.replace(/"/g, '');
        // replace ' with ""
        const newPath4 = newPath3.replace(/'/g, '');
        return newPath4
    }
    
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
        let raidMainPrice = 0;
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
            const new_total_Percentage = total_Percentage + difficultyValue

            // Apply extra charges to the result
            raidMainPrice += raidMainPrice * new_total_Percentage;
            // Apply promo code 
            raidMainPrice -= raidMainPrice * (discount_amount/100 )
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
            const difficultyValue = getSelectedDifficulty();
            const new_total_Percentage = total_Percentage + difficultyValue

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
            $(raidBundleForm).find('input[name="difficulty_chosen"]').val(difficultyValue);
        }

    }




    // function get selected difficulty value
    const getSelectedDifficulty = () => {
        let selectedValue = null;
        difficultyRadio.forEach((radio) => {
            if (radio.checked) {
                selectedValue = parseFloat(radio.value);
            }
        });
        return selectedValue;
    }

    const raidServerRadio = document.getElementsByName('raid-server');
    function getSelectedServer() {
        let selectedValue;
        // Loop through the radio buttons to find the checked one
        for (const radio of raidServerRadio) {
            if (radio.checked) {
                selectedValue = radio.value;
                break;
            }
        }
        $(raidForm).find('input[name="server"]').val(selectedValue);
        $(raidBundleForm).find('input[name="server"]').val(selectedValue);
        return selectedValue;
    }
    getSelectedServer()

    raidServerRadio.forEach((radio) => {
        radio.addEventListener('change', function () {
            getSelectedServer();
        })
    })


    difficultyRadio.forEach((radio) => {
        radio.addEventListener('change', function () {
            getRaidPrice();
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
      get2vs2ArenaPrice();
      get3vs3ArenaPrice();
      getRaidPrice();
    })
  });
  
  promo_form.addEventListener('submit', async function(event) {
    event.preventDefault();  
    if(!extend_order) {
      discount_amount = await fetch_promo(); 
  
      get2vs2ArenaPrice(); 
      get3vs3ArenaPrice();
      getRaidPrice();
    }
  });

  getRaidPrice();
})
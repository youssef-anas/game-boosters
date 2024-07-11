document.addEventListener("DOMContentLoaded", function () {
    const bosses_btn = document.getElementById('view-bosses');
    const bosses = document.getElementById('popup-bosses-form');
    const close_bosses = document.getElementById('close-booses');
    const piloted = document.getElementById('piloted-checkbox');
    const selfplay = document.getElementById('selfplay-checkbox');
    let bandelPrice = 0;

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


    const bossesList = document.querySelectorAll('.bosses-list-with-checkboxes')

    const removeBandelBtnAction = () => {
        removeBandelDiv.classList.add('d-none')
        bandelViewDiv.classList.add('d-none')
        awakenedRaidDiv.classList.remove('d-none')
        bossesSelectDiv.classList.remove('d-none')
        // TODO get selected map then view only bosses with that map
        bossesList.forEach((bosses) => {
            bosses.classList.remove('d-none')
        })

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
})
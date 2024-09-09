document.addEventListener("DOMContentLoaded", function () {
  const divisionBoostRadio = document.getElementById('division-boost');
  const placementsBoostRadio = document.getElementById('placements-boost');
  
  const divisionBoostDiv = document.querySelectorAll('.division-boost');
  const placementsBoostDiv = document.querySelectorAll('.placements-boost');

  // const divisionForm = document.getElementById('division-boost');
  // const placementsForm = document.getElementById('placements-boost');

  // Initial setup
  if (divisionBoostRadio){  
  if (divisionBoostRadio.checked) {
    divisionBoostDiv.forEach(div => div.classList.remove('d-none'));
    placementsBoostDiv.forEach(div => div.classList.add('d-none'));
    divisionBoostDiv.forEach(div => div.classList.add('active'));
    placementsBoostDiv.forEach(div => div.classList.remove('active'));
    // divisionForm.classList.add("active");
    // placementsForm.classList.remove("active");
  } else {
    divisionBoostDiv.forEach(div => div.classList.add('d-none'));
    placementsBoostDiv.forEach(div => div.classList.remove('d-none'));
    divisionBoostDiv.forEach(div => div.classList.remove('active'));
    placementsBoostDiv.forEach(div => div.classList.add('active'));
    // divisionForm.classList.remove("active");
    // placementsForm.classList.add("active");
  }
}

  // Event listener for division-boost radio button
  if (divisionBoostRadio){
  divisionBoostRadio.addEventListener('change', function () {
    if (divisionBoostRadio.checked) {
      divisionBoostDiv.forEach(div => div.classList.remove('d-none'));
      placementsBoostDiv.forEach(div => div.classList.add('d-none'));
      divisionBoostDiv.forEach(div => div.classList.add('active'));
      placementsBoostDiv.forEach(div => div.classList.remove('active'));
      // divisionForm.classList.add("active");
      // placementsForm.classList.remove("active");
    } else {
      divisionBoostDiv.forEach(div => div.classList.add('d-none'));
      divisionBoostDiv.forEach(div => div.classList.remove('active'));
      // divisionForm.classList.remove("active");
    }
  });
  }

  // Event listener for placements-boost radio button
  if (placementsBoostRadio){
  placementsBoostRadio.addEventListener('change', function () {
    if (placementsBoostRadio.checked) {
      divisionBoostDiv.forEach(div => div.classList.add('d-none'));
      placementsBoostDiv.forEach(div => div.classList.remove('d-none'));
      divisionBoostDiv.forEach(div => div.classList.remove('active'));
      placementsBoostDiv.forEach(div => div.classList.add('active'));
      // divisionForm.classList.remove("active");
      // placementsForm.classList.add("active");
    } else {
      placementsBoostDiv.forEach(div => div.classList.add('d-none'));
      placementsBoostDiv.forEach(div => div.classList.remove('active'));
      // placementsForm.classList.remove("active");
    }
  });
}

});


//popup champion
const championDataInputs= document.querySelectorAll('.champion-data')
const checkboxes = document.querySelectorAll('.hidden-checkbox');
const selectBoosterButton = document.getElementById('selectBoosterButton')
const selectChampionButton = document.getElementById('selectChampionButton')
let selectedIds = [];

function disableButton(disable, type='both') {
  if(type == 'champion') {
    if (selectChampionButton){
      selectChampionButton.disabled = disable;
    }
  } else if(type == 'booster') {
    selectBoosterButton.disabled = disable;
  } else {
    selectBoosterButton.disabled = disable;
    if (selectChampionButton){
      selectChampionButton.disabled = disable;
    }
  }
}

disableButton(true)

function togglePopupChampion() {
  const checkbox = document.getElementById("select_champion");
  if (checkbox.checked == true) {
    openFormChampoin();
  } else {
    closeFormChampion();
    championDataInputs.forEach(input => {
      input.value = 'null'; 
    });
  }
}

function closeFormChampionWithMakechekboxfalse() {
  closeFormChampion();
  const checkbox = document.getElementById("select_champion");
  checkbox.click();
  championDataInputs.forEach(input => {
    input.value = 'null'; 
  });
}

function openFormChampoin() {
  document.getElementById("popup-champion-form").style.display = "flex";
  championDataInputs.forEach(input => {
    input.value = 'null'; 
  });
  selectedIds = [];
  checkboxes.forEach(checkbox => {
    checkbox.checked = false;
  });
}

function closeFormChampion() {
  const selectChampionButton = document.getElementById('selectChampionButton')
  selectChampionButton.disabled = true
  document.getElementById("popup-champion-form").style.display = "none";
  checkboxes.forEach(checkbox => {
    checkbox.checked = false;
  });
  selectedIds = [];
}
checkboxes.forEach(checkbox => {
  checkbox.addEventListener('change', () => {
    if (checkbox.checked) {      
      selectedIds.push(checkbox.id);
      if (selectedIds.length > 3) {
        const lastCheckedId = selectedIds.shift();
        document.getElementById(lastCheckedId).checked = false;
      }

    } else {
      const index = selectedIds.indexOf(checkbox.id);
      if (index !== -1) {
        selectedIds.splice(index, 1);
      }
    }
    const result = selectedIds.join('');

    championDataInputs.forEach(input => {
      input.value = result;
    });

    if (selectedIds.length != 0) {
      disableButton(false, 'champion')
    } else {
      disableButton(true, 'champion')
    }
  });
});


// popup booster
const boostersCards = document.querySelectorAll('.booster-card');
const chooseBoosterInput = document.querySelectorAll('.choose-booster')
function togglePopupBooster() {
  const checkbox = document.getElementById("select-booster");
  if (chooseBoosterValue == null){
    if (checkbox.checked == true) {
      openFormBooster();
    } else {
      closeFormBooster();
      chooseBoosterInput.forEach(input => {
        input.value = 0; 
      });
    }
  }
}

function closeFormBoosterWithMakechekboxfalse() {
  closeFormBooster();
  const checkbox = document.getElementById("select-booster");
  checkbox.click();
  const chooseBoosterInput = document.querySelectorAll(".choose-booster-input");
  chooseBoosterInput.forEach(input => {
    input.value = 0;
  });
}


function openFormBooster() {
  document.getElementById("popup-booster-form").style.display = "block";
}

function closeFormBooster() {
  const selectBoosterButton = document.getElementById('selectBoosterButton')
  selectBoosterButton.disabled = true
  document.getElementById("popup-booster-form").style.display = "none";
  boostersCards.forEach(card => {
    card.classList.remove('selected-booster');
  });
}


function SetBooster(clickedCard) {
  boostersCards.forEach(card => {
    card.classList.remove('selected-booster');
  });

  clickedCard.classList.add('selected-booster');
  chooseBoosterInput.forEach(input => {
    input.value = clickedCard.id; 
  });

  disableButton(false, 'booster')
}
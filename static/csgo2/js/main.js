const divisionBoostRadio = document.getElementById('division-boost');
const premierBoostRadio = document.getElementById('premier-boost');
const faceitBoostRadio = document.getElementById('faceit-boost');

const divisionBoostDiv = document.querySelectorAll('.division-boost');
const premierBoostDiv = document.querySelectorAll('.premier-boost');
const faceitBoostDiv = document.querySelectorAll('.faceit-boost');

function divisionBoostChecked() {
  divisionBoostDiv.forEach(div => div.classList.remove('d-none'));
  premierBoostDiv.forEach(div => div.classList.add('d-none'));
  faceitBoostDiv.forEach(div => div.classList.add('d-none'));
}

function premierBoostChecked() {
  divisionBoostDiv.forEach(div => div.classList.add('d-none'));
  premierBoostDiv.forEach(div => div.classList.remove('d-none'));
  faceitBoostDiv.forEach(div => div.classList.add('d-none'));
}

function faceitBoostChecked() {
  divisionBoostDiv.forEach(div => div.classList.add('d-none'));
  premierBoostDiv.forEach(div => div.classList.add('d-none'));
  faceitBoostDiv.forEach(div => div.classList.remove('d-none'));
}

// Initial setup
if (divisionBoostRadio.checked) {
  divisionBoostChecked()

} else if (premierBoostRadio.checked) {
  premierBoostChecked()

} else if (faceitBoostRadio.checked) {
  faceitBoostChecked()

}

// Event listener for division-boost radio button
divisionBoostRadio.addEventListener('change', function () {
  if (divisionBoostRadio.checked) {
    divisionBoostChecked()

  } else {
    divisionBoostDiv.forEach(div => div.classList.add('d-none'));
  }
});


// Event listener for premier-boost radio button
premierBoostRadio.addEventListener('change', function () {
  if (premierBoostRadio.checked) {
    premierBoostChecked()

  } else {
    premierBoostDiv.forEach(div => div.classList.add('d-none'));
  }
});

// Event listener for faceit-boost radio button
faceitBoostRadio.addEventListener('change', function () {
  if (faceitBoostRadio.checked) {
    faceitBoostChecked()

  } else {
    faceitBoostDiv.forEach(div => div.classList.add('d-none'));
  }
});
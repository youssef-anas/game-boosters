document.addEventListener("DOMContentLoaded", function () {
    const divisionBoostRadio = document.getElementById('division-boost');
    const placementsBoostRadio = document.getElementById('placements-boost');

    const divisionBoostDiv = document.querySelector('.division-boost');
    const placementsBoostDiv = document.querySelector('.placements-boost');

    // Initial setup
    if (divisionBoostRadio.checked) {
        divisionBoostDiv.classList.remove('d-none');
        placementsBoostDiv.classList.add('d-none');
    } else {
        divisionBoostDiv.classList.add('d-none');
        placementsBoostDiv.classList.remove('d-none');
    }

    // Event listener for division-boost radio button
    divisionBoostRadio.addEventListener('change', function () {
        if (divisionBoostRadio.checked) {
            divisionBoostDiv.classList.remove('d-none');
            placementsBoostDiv.classList.add('d-none');
        } else {
            divisionBoostDiv.classList.add('d-none');
        }
    });

    // Event listener for placements-boost radio button
    placementsBoostRadio.addEventListener('change', function () {
        if (placementsBoostRadio.checked) {
            divisionBoostDiv.classList.add('d-none');
            placementsBoostDiv.classList.remove('d-none');
        } else {
            placementsBoostDiv.classList.add('d-none');
        }
    });
});
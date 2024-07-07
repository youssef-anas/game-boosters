document.addEventListener("DOMContentLoaded", function () {
    const bosses_btn = document.getElementById('view-bosses');
    const bosses = document.getElementById('popup-bosses-form');
    const close_bosses = document.getElementById('close-booses');
    const piloted = document.getElementById('piloted-checkbox');
    const selfplay = document.getElementById('selfplay-checkbox');

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
})
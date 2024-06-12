document.addEventListener('DOMContentLoaded', function() {
    const availableBtns = document.querySelectorAll('.available-btn');
    const FIFTEEN_MINUTES_IN_MS = 15 * 60 * 1000;

    function startCountdown(duration, display) {
        let timer = duration, minutes, seconds;
        const countdownInterval = setInterval(() => {
            minutes = parseInt(timer / 60, 10);
            seconds = parseInt(timer % 60, 10);

            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            display.textContent = `Try again in ${minutes}:${seconds}`;

            if (--timer < 0) {
                clearInterval(countdownInterval);
                display.disabled = false;
                display.textContent = 'Available to Play';
                const orderId = display.id;
                const cacheKey = `disableUntil_${orderId}`;
                localStorage.removeItem(cacheKey);
            }
        }, 1000);
    }

    function disableButtonWithTimeout(btn) {
        const disableUntil = new Date().getTime() + FIFTEEN_MINUTES_IN_MS;
        const orderId = btn.id;
        const cacheKey = `disableUntil_${orderId}`;
        localStorage.setItem(cacheKey, disableUntil);

        btn.disabled = true;

        const remainingTime = FIFTEEN_MINUTES_IN_MS / 1000;
        startCountdown(remainingTime, btn);
    }

    function checkButtonStatus() {
        availableBtns.forEach(btn => {
            const orderId = btn.id; // Get the button's id
            const cacheKey = `disableUntil_${orderId}`; // Unique storage key for each button
            const disableUntil = localStorage.getItem(cacheKey);
            if (disableUntil) {
                const now = new Date().getTime();
                const remainingTime = (disableUntil - now) / 1000;
                if (remainingTime > 0) {
                    btn.disabled = true;
                    startCountdown(remainingTime, btn);
                }
            }
        });
    }

    availableBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            btn.disabled = true;
            btn.textContent = 'Sending....';

            const orderId = btn.id;
            fetch(`/customer/available/${orderId}/`, {
                method: 'GET',
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response);
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                btn.textContent = 'Request Sent';
                disableButtonWithTimeout(btn);
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
                btn.disabled = false;
                btn.textContent = 'Available to Play';
            });
        });
    });

    checkButtonStatus();
});

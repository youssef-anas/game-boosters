document.addEventListener('DOMContentLoaded', function() {
  const game_id = parseInt(document.querySelector('form.purchaseForm input[name="game_id"]').value);

  const urls = document.getElementById('urls');

  // --------------------- DIVISION ---------------------

  if (game_id == 6) {
    const arenaForm = document.getElementById('arena-form');
    const arenaPaypalBtn = document.getElementById('arena-paypal-btn');
    const arenaCryptomusBtn = document.getElementById('arena-cryptomus-btn');

    arenaPaypalBtn.addEventListener('click', function() {
      // Get the PayPal URL from data attribute
      const paypalUrl = urls.dataset.paypalUrl;
      // Set the form action
      arenaForm.action = paypalUrl;
      // Submit the form
      arenaForm.submit();
    });

    arenaCryptomusBtn.addEventListener('click', function() {
      // Get the Cryptomus URL from data attribute
      const cryptomusUrl = urls.dataset.cryptomusUrl;
      // Set the form action
      arenaForm.action = cryptomusUrl;
      // Submit the form
      arenaForm.submit();
    });
    
  } else {
    const divisionForm = document.getElementById('division-boost-form');
    const divisionPaypalBtn = document.getElementById('division-paypal-btn');
    const divisionCryptomusBtn = document.getElementById('division-cryptomus-btn');

    divisionPaypalBtn.addEventListener('click', function() {
      // Get the PayPal URL from data attribute
      const paypalUrl = urls.dataset.paypalUrl;
      // Set the form action
      divisionForm.action = paypalUrl;
      // Submit the form
      divisionForm.submit();
    });

    divisionCryptomusBtn.addEventListener('click', function() {
      // Get the Cryptomus URL from data attribute
      const cryptomusUrl = urls.dataset.cryptomusUrl;
      // Set the form action
      divisionForm.action = cryptomusUrl;
      // Submit the form
      divisionForm.submit();
    });
  }

  // --------------------- PLACEMNET ---------------------

  if (game_id != 1 && game_id != 6 && game_id != 11) {
    const placementForm = document.getElementById('placements-boost-form');
    const placementPaypalBtn = document.getElementById('placement-paypal-btn');
    const placementCryptomusBtn = document.getElementById('placement-cryptomus-btn');

    if(placementPaypalBtn){
      placementPaypalBtn.addEventListener('click', function() {
        // Get the PayPal URL from data attribute
        const paypalUrl = urls.dataset.paypalUrl;
        // Set the form action
        placementForm.action = paypalUrl;
        // Submit the form
        placementForm.submit();
      });
    }

    if(placementCryptomusBtn){
      placementCryptomusBtn.addEventListener('click', function() {
        // Get the Cryptomus URL from data attribute
        const cryptomusUrl = urls.dataset.cryptomusUrl;
        // Set the form action
        placementForm.action = cryptomusUrl;
        // Submit the form
        placementForm.submit();
      });
    }
  }

  // --------------------- OTHERS ---------------------
  if(game_id == 9) {
    // --------------------- SEASONAL ---------------------
    const seasonalForm = document.getElementById('seasonal-reward-form');
    const seasonalPaypalBtn = document.getElementById('seasonal-paypal-btn');
    const seasonalCryptomusBtn = document.getElementById('seasonal-cryptomus-btn');

    if(seasonalPaypalBtn){
      seasonalPaypalBtn.addEventListener('click', function() {
        // Get the PayPal URL from data attribute
        const paypalUrl = urls.dataset.paypalUrl;
        // Set the form action
        seasonalForm.action = paypalUrl;
        // Submit the form
        seasonalForm.submit();
      });
    }

    if(seasonalCryptomusBtn){
      seasonalCryptomusBtn.addEventListener('click', function() {
        // Get the Cryptomus URL from data attribute
        const cryptomusUrl = urls.dataset.cryptomusUrl;
        // Set the form action
        seasonalForm.action = cryptomusUrl;
        // Submit the form
        seasonalForm.submit();
      });
    }

    // --------------------- TOURNAMENT ---------------------
    const tournamentForm = document.getElementById('tournament-boost-form');
    const tournamentPaypalBtn = document.getElementById('tournament-paypal-btn');
    const tournamentCryptomusBtn = document.getElementById('tournament-cryptomus-btn');

    if(tournamentPaypalBtn){
      tournamentPaypalBtn.addEventListener('click', function() {
        // Get the PayPal URL from data attribute
        const paypalUrl = urls.dataset.paypalUrl;
        // Set the form action
        tournamentForm.action = paypalUrl;
        // Submit the form
        tournamentForm.submit();
      });
    }

    if(tournamentCryptomusBtn){
      tournamentCryptomusBtn.addEventListener('click', function() {
        // Get the Cryptomus URL from data attribute
        const cryptomusUrl = urls.dataset.cryptomusUrl;
        // Set the form action
        tournamentForm.action = cryptomusUrl;
        // Submit the form
        tournamentForm.submit();
      });
    }
  }
});

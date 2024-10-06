// Refresh If Return From Pay
if(performance.navigation.type == 2){
  location.reload(true);
}

document.addEventListener('DOMContentLoaded', function() {

  function disable_alert(alert){
    setTimeout(() => {
      alert.classList.add('d-none')
      alert.classList.remove('loader-active');
    }, 5100);
  }
  
  const run_allerts = (alert) => {
    // Show the loader
    alert.classList.remove('d-none');
    setTimeout(function() {
      alert.classList.add('loader-active');
    }, 100);
  }

  const handleAllerts = (message) => {
    const alert = document.getElementById('alert-div');
    const alertText = document.getElementById('alert-text-info');
    window.scrollTo({ top: 0, behavior: 'smooth' });
    alertText.innerHTML = message;
    run_allerts(alert)
    disable_alert(alert)
  }




  // const game_id = parseInt(document.querySelector('form.purchaseForm input[name="game_id"]').value);

  const urls = document.getElementById('urls');
  const paypalBtns = document.querySelectorAll('.paypal-btn');
  const cryptomusBtns = document.querySelectorAll('.cryptomus-btn');

  const getParentFormWIthBtnClicked = (btn) => {
    return btn.closest('form');
  }

  paypalBtns.forEach((btn) => {
    btn.addEventListener('click', function() {
      console.log('paypal btn clicked')
      // Get the PayPal URL from data attribute
      const paypalUrl = urls.dataset.paypalUrl;
      // Set the form action
      const form = getParentFormWIthBtnClicked(btn);
      form.action = paypalUrl;
      // Submit the form

      // Create a hidden input field with name 'cryptomus' and value 'true'      
      let cryptomusInput = form.querySelector('input[name="cryptomus"]');
      if (!cryptomusInput) {
          cryptomusInput = document.createElement('input');
        }
      cryptomusInput.type = 'hidden';
      cryptomusInput.name = 'cryptomus';
      cryptomusInput.value = 'false';
      form.appendChild(cryptomusInput);
        
      const formData = new FormData(form);
      getpaymentUrl(formData, paypalUrl)
    })
  })

  cryptomusBtns.forEach((btn) => {
    btn.addEventListener('click', function() {
      // Get the Cryptomus URL from data attribute
      const cryptomusUrl = urls.dataset.cryptomusUrl;
      const paypalUrl = urls.dataset.paypalUrl;
      // Set the form action
      const form = getParentFormWIthBtnClicked(btn);
      form.action = paypalUrl;
      
      // Create a hidden input field with name 'cryptomus' and value 'true'      
      let cryptomusInput = form.querySelector('input[name="cryptomus"]');
      if (!cryptomusInput) {
          cryptomusInput = document.createElement('input');
        }
      cryptomusInput.type = 'hidden';
      cryptomusInput.name = 'cryptomus';
      cryptomusInput.value = 'true';
      form.appendChild(cryptomusInput); 

      // Append the hidden input field to the form
      form.appendChild(cryptomusInput);

      const formData = new FormData(form);
      getpaymentUrl(formData, paypalUrl)
    })
  })


  const getpaymentUrl = async (formData, URL) => {
    // Show the loader and disable all buttons
    document.getElementById('loader').style.display = 'flex';
    disableAllButtons(true);
    try {
      // Send the form data using fetch
      const response = await fetch(URL, {
          method: 'POST',
          body: formData,
          headers: {
              'Accept': 'application/json'
          }
      });
      // Parse the JSON response
      const data = await response.json();
      // when not authorized redirect to login
        if (response.status === 401 || response.status === 403 ){
          window.location.href = '/accounts/login/';
        }

        if (data.url) {
            // Redirect to the provided URL
            window.location.href = data.url;
        } else {
          handleAllerts(data.message)
        }
    } catch (error) {
        console.error('Error during the fetch request:', error);
    }finally {
      // Hide the loader and re-enable all buttons
      document.getElementById('loader').style.display = 'none';
      disableAllButtons(false);
  }
  }

  function disableAllButtons(disable) {
    document.querySelectorAll('button').forEach((button) => {
        button.disabled = disable;
    });
  }

    // const arenaForm = document.getElementById('arena-form');
    // const arenaPaypalBtn = document.getElementById('arena-paypal-btn');
    // const arenaCryptomusBtn = document.getElementById('arena-cryptomus-btn');

    // arenaPaypalBtn.addEventListener('click', function() {
    //   // Get the PayPal URL from data attribute
    //   const paypalUrl = urls.dataset.paypalUrl;
    //   // Set the form action
    //   arenaForm.action = paypalUrl;
    //   // Submit the form
    //   arenaForm.submit();
    // });

    // arenaCryptomusBtn.addEventListener('click', function() {
    //   // Get the Cryptomus URL from data attribute
    //   const cryptomusUrl = urls.dataset.cryptomusUrl;
    //   // Set the form action
    //   arenaForm.action = cryptomusUrl;
    //   // Submit the form
    //   arenaForm.submit();
    // });
    
  // } else {
  //   const divisionForm = document.getElementById('division-boost-form');
  //   const divisionPaypalBtn = document.getElementById('division-paypal-btn');
  //   const divisionCryptomusBtn = document.getElementById('division-cryptomus-btn');

  //   divisionPaypalBtn.addEventListener('click', function() {
  //     // Get the PayPal URL from data attribute
  //     const paypalUrl = urls.dataset.paypalUrl;
  //     // Set the form action
  //     divisionForm.action = paypalUrl;
  //     // Submit the form
  //     divisionForm.submit();
  //   });

  //   divisionCryptomusBtn.addEventListener('click', function() {
  //     // Get the Cryptomus URL from data attribute
  //     const cryptomusUrl = urls.dataset.cryptomusUrl;
  //     // Set the form action
  //     divisionForm.action = cryptomusUrl;
  //     // Submit the form
  //     divisionForm.submit();
  //   });
  // }

  // // --------------------- PLACEMNET ---------------------

  // if (game_id != 1 && game_id != 6 && game_id != 11) {
  //   const placementForm = document.getElementById('placements-boost-form');
  //   const placementPaypalBtn = document.getElementById('placement-paypal-btn');
  //   const placementCryptomusBtn = document.getElementById('placement-cryptomus-btn');

  //   if(placementPaypalBtn){
  //     placementPaypalBtn.addEventListener('click', function() {
  //       // Get the PayPal URL from data attribute
  //       const paypalUrl = urls.dataset.paypalUrl;
  //       // Set the form action
  //       placementForm.action = paypalUrl;
  //       // Submit the form
  //       placementForm.submit();
  //     });
  //   }

  //   if(placementCryptomusBtn){
  //     placementCryptomusBtn.addEventListener('click', function() {
  //       // Get the Cryptomus URL from data attribute
  //       const cryptomusUrl = urls.dataset.cryptomusUrl;
  //       // Set the form action
  //       placementForm.action = cryptomusUrl;
  //       // Submit the form
  //       placementForm.submit();
  //     });
  //   }
  // }

  // // --------------------- OTHERS ---------------------
  // if(game_id == 9) {
  //   // --------------------- SEASONAL ---------------------
  //   const seasonalForm = document.getElementById('seasonal-reward-form');
  //   const seasonalPaypalBtn = document.getElementById('seasonal-paypal-btn');
  //   const seasonalCryptomusBtn = document.getElementById('seasonal-cryptomus-btn');

  //   if(seasonalPaypalBtn){
  //     seasonalPaypalBtn.addEventListener('click', function() {
  //       // Get the PayPal URL from data attribute
  //       const paypalUrl = urls.dataset.paypalUrl;
  //       // Set the form action
  //       seasonalForm.action = paypalUrl;
  //       // Submit the form
  //       seasonalForm.submit();
  //     });
  //   }

  //   if(seasonalCryptomusBtn){
  //     seasonalCryptomusBtn.addEventListener('click', function() {
  //       // Get the Cryptomus URL from data attribute
  //       const cryptomusUrl = urls.dataset.cryptomusUrl;
  //       // Set the form action
  //       seasonalForm.action = cryptomusUrl;
  //       // Submit the form
  //       seasonalForm.submit();
  //     });
  //   }

  //   // --------------------- TOURNAMENT ---------------------
  //   const tournamentForm = document.getElementById('tournament-boost-form');
  //   const tournamentPaypalBtn = document.getElementById('tournament-paypal-btn');
  //   const tournamentCryptomusBtn = document.getElementById('tournament-cryptomus-btn');

  //   if(tournamentPaypalBtn){
  //     tournamentPaypalBtn.addEventListener('click', function() {
  //       // Get the PayPal URL from data attribute
  //       const paypalUrl = urls.dataset.paypalUrl;
  //       // Set the form action
  //       tournamentForm.action = paypalUrl;
  //       // Submit the form
  //       tournamentForm.submit();
  //     });
  //   }

  //   if(tournamentCryptomusBtn){
  //     tournamentCryptomusBtn.addEventListener('click', function() {
  //       // Get the Cryptomus URL from data attribute
  //       const cryptomusUrl = urls.dataset.cryptomusUrl;
  //       // Set the form action
  //       tournamentForm.action = cryptomusUrl;
  //       // Submit the form
  //       tournamentForm.submit();
  //     });
  //   }
  // } 

  // if(game_id == 13) {
  //   // --------------------- Premier ---------------------
  //   const premierForm = document.getElementById('premier-boost-form');
  //   const premierPaypalBtn = document.getElementById('premier-paypal-btn');
  //   const fpremierCryptomusBtn = document.getElementById('premier-cryptomus-btn');

  //   if(premierPaypalBtn){
  //     premierPaypalBtn.addEventListener('click', function() {
  //       // Get the PayPal URL from data attribute
  //       const paypalUrl = urls.dataset.paypalUrl;
  //       // Set the form action
  //       premierForm.action = paypalUrl;
  //       // Submit the form
  //       premierForm.submit();
  //     });
  //   }

  //   if(fpremierCryptomusBtn){
  //     fpremierCryptomusBtn.addEventListener('click', function() {
  //       // Get the Cryptomus URL from data attribute
  //       const cryptomusUrl = urls.dataset.cryptomusUrl;
  //       // Set the form action
  //       premierForm.action = cryptomusUrl;
  //       // Submit the form
  //       premierForm.submit();
  //     });
  //   }

  //   // --------------------- FACEIT ---------------------
  //   const faceitForm = document.getElementById('faceit-boost-form');
  //   const faceitPaypalBtn = document.getElementById('faceit-paypal-btn');
  //   const faceitCryptomusBtn = document.getElementById('faceit-cryptomus-btn');

  //   if(faceitPaypalBtn){
  //     faceitPaypalBtn.addEventListener('click', function() {
  //       // Get the PayPal URL from data attribute
  //       const paypalUrl = urls.dataset.paypalUrl;
  //       // Set the form action
  //       faceitForm.action = paypalUrl;
  //       // Submit the form
  //       faceitForm.submit();
  //     });
  //   }

  //   if(faceitCryptomusBtn){
  //     faceitCryptomusBtn.addEventListener('click', function() {
  //       // Get the Cryptomus URL from data attribute
  //       const cryptomusUrl = urls.dataset.cryptomusUrl;
  //       // Set the form action
  //       faceitForm.action = cryptomusUrl;
  //       // Submit the form
  //       faceitForm.submit();
  //     });
  //   }
  // }

  // const battlegrounds_boost_form = document.getElementById('battlegrounds-boost-form');
  // const battlegrounds_paypal_btn = document.getElementById('battlegrounds-paypal-btn');
  // const battlegrounds_cryptomus_btn = document.getElementById('battlegrounds-cryptomus-btn');

  // if(battlegrounds_boost_form) {
  //   battlegrounds_paypal_btn.addEventListener('click', function() {
  //     const paypalUrl = urls.dataset.paypalUrl;
  //     battlegrounds_boost_form.action = paypalUrl;
  //     battlegrounds_boost_form.submit();
  //   });

  //   battlegrounds_cryptomus_btn.addEventListener('click', function() {
  //     const cryptomusUrl = urls.dataset.cryptomusUrl;
  //     battlegrounds_boost_form.action = cryptomusUrl;
  //     battlegrounds_boost_form.submit();
  //   });
  // }
});

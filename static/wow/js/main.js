// document.addEventListener("DOMContentLoaded", function () {
//   const arena2vs2Radio = document.getElementById('arena-2vs2');
//   const arena3vs3Radio = document.getElementById('arena-3vs3');

//   const arena2vs2Div = document.querySelectorAll('.arena-2vs2');
//   const arena3vs3Div = document.querySelectorAll('.arena-3vs3');

//   function arena2vs2Action() {
//     arena2vs2Div.forEach(div => div.classList.remove('d-none'));
//     arena3vs3Div.forEach(div => div.classList.add('d-none'));
//     $('#arena-form').data('type', 'arena2vs2');
//     get2vs2ArenaPrice()
//   }

//   function arena3vs3Action() {
//     arena2vs2Div.forEach(div => div.classList.add('d-none'));
//     arena3vs3Div.forEach(div => div.classList.remove('d-none'));
//     $('#arena-form').data('type', 'arena3vs3');
//     get3vs3ArenaPrice();
//   }

//   // Initial setup
//   if (arena2vs2Radio.checked) {
//     arena2vs2Action()
//   } else {
//     arena3vs3Action()
//   }

//   // Extend 
//   extend_order && (valuesToSetExtra[0] ? arena2vs2Action() : arena3vs3Action())

//   // Event listener for division-boost radio button
//   arena2vs2Radio.addEventListener('change', function () {
//     if (arena2vs2Radio.checked) {
//       arena2vs2Action()
//     } else {
//       arena3vs3Action()
//     }
//   });

//   // Event listener for placements-boost radio button
//   arena3vs3Radio.addEventListener('change', function () {
//     if (arena3vs3Radio.checked) {
//       arena3vs3Action()
//     } else {
//       arena3vs3Action()
//     }
//   });

// });



document.addEventListener("DOMContentLoaded", function () {
  const mapSelection = document.querySelectorAll('input[type="radio"][name="map"]');
  const bossesList = document.querySelectorAll('.bosses-list-with-checkboxes')

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

  const radioModes= document.querySelectorAll('input[type="radio"][name="radio-group-type"]');
  // Convert NodeList to array to use map
  const radioArray = Array.from(radioModes);
  const radio_ids = radioArray.map(radio => radio.id);

  const get_checked_mode = () => {
    const radio = document.querySelector('input[type="radio"][name="radio-group-type"]:checked');
    return radio.id
  }

  const chnage_mode = () =>{
    radio_ids.forEach(id => {
      const hideElement = document.querySelectorAll(`.${id}`);
      hideElement.forEach(element => {
        element.classList.add('d-none');
      })
    }) 
    const checked_id = get_checked_mode();
    // document.getElementById('arena-form').dataset.type = checked_id;
    const viewElements = document.querySelectorAll(`.${checked_id}`);
      viewElements.forEach(element => {
        element.classList.remove('d-none');
      })
  }

  radioModes.forEach(radio => {
    radio.addEventListener('change', function () {
      chnage_mode();
      if (get_checked_mode() == 'raid') {
        toggleViewBosses();
      }
      else{
        // const fullPriority = document.getElementById('full-priority');
        // fullPriority.checked = false
      }
    });
  })

  // const arena2vs2Radio = document.getElementById('arena-2vs2');
  // const arena3vs3Radio = document.getElementById('arena-3vs3');

  // make arena2vs2Radio or arena3vs3Radio checked if the extend_order
  // extend_order && (valuesToSetExtra[0] ? arena2vs2Radio.checked = true: arena3vs3Radio.checked = true)

  chnage_mode();
});
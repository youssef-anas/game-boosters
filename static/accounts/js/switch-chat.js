const boosterChatRadio = document.getElementById('chat-booster-option');
const adminChatRadio = document.getElementById('chat-admin-option');

const boosterChatDiv = document.getElementById('chat-booster-container');
const adminChatDiv = document.getElementById('chat-admin-container');


// Initial setup
if (boosterChatRadio.checked) {
  boosterChatDiv.classList.remove('d-none');
  adminChatDiv.classList.add('d-none');

} else {
  boosterChatDiv.classList.add('d-none');
  adminChatDiv.classList.remove('d-none');

}

// Event listener for division-boost radio button
if (boosterChatRadio){
  boosterChatRadio.addEventListener('change', function () {
    if (boosterChatRadio.checked) {
      boosterChatDiv.classList.remove('d-none');
      adminChatDiv.classList.add('d-none');
    
    } else {
      boosterChatDiv.classList.add('d-none');
      
    }
  });
}

// Event listener for placements-boost radio button
if (adminChatRadio){
  adminChatRadio.addEventListener('change', function () {
    if (adminChatRadio.checked) {
      boosterChatDiv.classList.add('d-none');
      adminChatDiv.classList.remove('d-none');
      
    } else {
      adminChatDiv.classList.add('d-none');
    
    }
  });
}
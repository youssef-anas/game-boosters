$('document').ready(function () {
  let ordersDivs = $('.order');
  let ordersRadio = $('input[name="radio-order"]')

  // Intial 
  let intialOrderId = $('input[name="radio-order"]:checked').data('order');
  ordersDivs.each(function () {
    let currentOrderId = $(this).data('order');
    if (currentOrderId == intialOrderId) {
      $(this).show("slow");
      let booster_room_name = $(this).data('room');
      let roomName = $(this).data('slug');
      chat(booster_room_name, roomName, currentOrderId)
    } else {
      $(this).hide("slow");
    }
  })

  ordersRadio.each(function () {
    let orderId = $(this).data('order');
    $(this).on('change', function () {
        ordersDivs.each(function () {
            let currentOrderId = $(this).data('order');
            if (currentOrderId == orderId) {
                $(this).show("slow");
                let booster_room_name = $(this).data('room');
                let roomName = $(this).data('slug');
                chat(booster_room_name, roomName, currentOrderId);
                
                // Remove focus from any input fields
                $(this).find('input').blur();
            } else {
                $(this).hide("slow");
            }
        })
    })
})

})
// ----------------------------- Chats -----------------------------
function chat(booster_room_name, roomName, orderId) {
  if (currentSocket) {
    currentSocket.close();
  }

  const user = JSON.parse(document.getElementById('user').textContent);
  
  const chatbox = document.getElementById(`customer-messages-container-${orderId}`);
  
  
  // Function to scroll to the bottom of the chatbox
  function scrollToBottom() {
    chatbox.scrollTop = chatbox.scrollHeight;
  }
  scrollToBottom();

  const wsProtocol = window.location.protocol === "https:" ? "wss://" : "ws://";
  const chatSocket = new WebSocket(wsProtocol + window.location.host + "/ws/chat/" + roomName + "/");
  currentSocket = chatSocket;

  chatSocket.onopen = function (e) {
    console.log("The connection was setup successfully !", orderId);
  };
  chatSocket.onclose = function (e) {
    console.log("WebSocket closed." , orderId);
  };
  $(`#message-input-${orderId}`).focus();
  document.querySelector(`#chat-form-${orderId}`).addEventListener("submit", function (e) {
    e.preventDefault();
  });

  $(`#message-input-${orderId}`).on('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) { // Check if Enter key is pressed and Shift key is not held down
      e.preventDefault();
      let input = e.target;
      let start = input.selectionStart;
      let end = input.selectionEnd;
      input.value = input.value.slice(0, start) + '\n' + input.value.slice(end);
      input.selectionStart = input.selectionEnd = start + 1;
    }
  });
  
  $(`#message-submit-order-${orderId}`).on('click', function (e) {
    e.preventDefault(); // Prevent default form submission behavior
    var messageInput = $(`#message-input-order-${orderId}`).val();
  
    if (messageInput.length == 0) {
      alert("Add some Input First Or Press Send Button!")
    } else {
      chatSocket.send(JSON.stringify({ message: messageInput, username: user, room_name: booster_room_name }));
      $(`#message-input-order-${orderId}`).val(""); // Clear the input field after sending the message
    }
  });

  $(`#message-submit-${orderId}`).on('click', function (e) {
    var messageInput = $(`#message-input-${orderId}`).val();

    if (messageInput.length == 0) {
      alert("Add some Input First Or Press Send Button!")
    }
    else {
      console.log("preesed")
      chatSocket.send(JSON.stringify({ message: messageInput, username: user, room_name: booster_room_name }));
    }

  });

  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    $('.no-messages').html('');

    let div = document.createElement("div");
    let messageContent = data.message;
    let messageElement = document.createElement("p");
    
    if (data.msg_type === 1) {
      messageElement.classList.add("message", "mb-0");
      messageElement.textContent = messageContent;
  
    } else if (data.msg_type === 3) {
  
      div.classList.add("booster-chat-message", "changes-message");
      div.style.backgroundColor = "transparent";
  
      messageElement.classList.add("info-message", "mb-0");
      messageElement.innerHTML = `<i class="fa-solid fa-circle-info ms-1"></i> ${data.message}`;
    }
  

    applyReadMore(messageElement)

    // Create and append the message time element
    let messageTimeElement = document.createElement("p");
    messageTimeElement.textContent = "Just Now";
    
    if (data.username === user) {
      messageTimeElement.classList.add("message-time", "mb-0", "me-2");
      const booster_image = JSON.parse(document.getElementById('booster_image').textContent);
    
      const imageDiv = document.createElement('div');
      imageDiv.className = 'image ms-3';
      
      const imgElement = document.createElement('img');
      imgElement.src = booster_image || staticUrl; // Use booster_image if available, otherwise fallback to staticUrl
      imgElement.alt = '';
      imgElement.width = 40;
      imgElement.height = 40;
    
      imageDiv.appendChild(imgElement);
    
      div.appendChild(messageTimeElement);
      div.appendChild(messageElement);
      div.appendChild(imageDiv);
    } else {
      const voiceSound = document.getElementById('notificationSound');
      // run voice sound
      console.log();
      if (getSoundValue()){
        voiceSound.play();
      }
      
      messageTimeElement.classList.add("message-time", "mb-0", "ms-2");

      if (data.message.msg_type == 4) {
        const imageDiv = document.createElement('div');
        imageDiv.className = 'image ms-3';
        
        const imgElement = document.createElement('img');
        imgElement.src = staticUrl; // Use booster_image if available, otherwise fallback to staticUrl
        imgElement.alt = '';
        imgElement.width = 40;
        imgElement.height = 40;
      
        imageDiv.appendChild(imgElement);

        div.appendChild(messageTimeElement);
        div.appendChild(messageElement);
        div.appendChild(imageDiv);
      } else {
        div.appendChild(messageElement);   
        div.appendChild(messageTimeElement);
      }
    }
    

    // Add class based on user authentication
    if (data.username === user) {
      div.classList.add("chat-message", "user-message");
    } else {
      if (data.message.msg_type == 2) {
        div.classList.add("chat-message", "tip-message");
      } else if (data.message.msg_type == 3) {
        div.classList.add("chat-message", "changes-message");
      } else if (data.message.msg_type == 4) {
        div.classList.add("chat-message", "from-admin-message");
      } else {
        div.classList.add("chat-message", "customer-message");
      }
    }

    $(`#message-input-${orderId}`).val("");
  
    document.querySelector(`#chatbox-${orderId}`).appendChild(div);
    scrollToBottom();
  };
}

$('.finish_image').on('change', function () {
  previewImage(this);
});

function previewImage(input) {
  let preview = $(input).closest('.modal-content').find('.image-preview')[0];
  let file = input.files[0];

  if (file) {
    let reader = new FileReader();

    reader.onload = function (e) {
      $(preview).attr('src', e.target.result);
      $(preview).css('display', 'block');
    };

    reader.readAsDataURL(file);
  } else {
    $(preview).css('display', 'none');
  }
}

const dropContainers = document.querySelectorAll(".dropcontainer");
const fileInputs = document.querySelectorAll(".finish_image");

dropContainers.forEach(dropContainer => {
  dropContainer.addEventListener("dragover", (e) => {
    e.preventDefault();
  }, false);

  dropContainer.addEventListener("dragenter", () => {
    dropContainer.classList.add("drag-active");
  });

  dropContainer.addEventListener("dragleave", () => {
    dropContainer.classList.remove("drag-active");
  });

  dropContainer.addEventListener("drop", (e) => {
    e.preventDefault();
    dropContainer.classList.remove("drag-active");
    const fileInput = e.currentTarget.querySelector('.finish_image');
    fileInput.files = e.dataTransfer.files;
    previewImage(fileInput);
  });
});


const customer_ids = document.querySelectorAll('.customer-ids');
let ids = [];
for (let id of customer_ids) {
  if (!ids.includes(id.dataset.customerId)){
    ids.push(id.dataset.customerId);
  }
}
console.log(ids)

const getHeadStatus = (customerId) => {
  return document.querySelectorAll(`.head-state${customerId}-id`);
}
const getStatus = (customerId) => {
  return document.querySelectorAll(`.state${customerId}-id`);
}

// Sleep function to create a delay (1 second in this case)
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Function to fetch and update user status
async function getUserStatus() {
  for (let id of ids) {
    const headStatusElements = getHeadStatus(id);
    const statusElements = getStatus(id); // Corrected to call getStatus

    try {
      const response = await fetch(`/chat/status/${id}/`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      const message = data.status;

      if (data.status === 'Online') {
        headStatusElements.forEach(function (headStatusElement) {
          headStatusElement.innerHTML = `
            <span class="online"></span> ${message}
          `;
        });
        statusElements.forEach(function (statusElement) {
          statusElement.innerHTML = `
            <span class="online"></span> ${message}
          `;
        });
      } else {
        headStatusElements.forEach(function (headStatusElement) {
          headStatusElement.innerHTML = `
            <span class="offline"></span> Offline
          `;
        });
        statusElements.forEach(function (statusElement) {
          statusElement.innerHTML = `
            <span class="offline"></span> Last seen ${message}
          `;
        });
      }
    } catch (error) {
      console.warn('Error fetching data:', error);
    }

    // Sleep for 1 second between requests
    await sleep(1000);
  }
}

// Initial call to getUserStatus
getUserStatus();

// Set interval to call getUserStatus every 50 seconds
setInterval(getUserStatus, 50000);
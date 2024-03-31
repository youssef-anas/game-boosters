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
          chat(booster_room_name, roomName, currentOrderId)
        } else {
          $(this).hide("slow");
        }
      })
    })
  })


  var rankSelect = $('#reached_rank_wildrift');
  var divisionSelect = $('#reached_division_wildrift');
  var marksSelect = $('#reached_marks_wildrift');

  if(rankSelect && divisionSelect && marksSelect) {
    var originalDivisionOptions = divisionSelect.html();
    var originalMarksOptions = marksSelect.html();
  
    function updateOptions() {
      var selectedRank = rankSelect.find(':selected');
      var markNumber = selectedRank.data('mark');
  
      divisionSelect.html(originalDivisionOptions);
      
      marksSelect.html(originalMarksOptions);
  
      if (parseInt(selectedRank.val()) === 8) {
        divisionSelect.val(1);
        divisionSelect.addClass('d-none')
        marksSelect.addClass('d-none')
      } else {
        divisionSelect.removeClass('d-none')
        marksSelect.removeClass('d-none')
        marksSelect.find('option').each(function () {
          if ($(this).val() > markNumber) {
            $(this).hide();
          } else {
            $(this).show();
          }
        });
      }

    }
  
    updateOptions();
  
    rankSelect.change(updateOptions);
  }
})
// ----------------------------- Chats -----------------------------
function chat(booster_room_name, roomName, orderId) {
  if (currentSocket) {
    currentSocket.close();
  }

  const user = JSON.parse(document.getElementById('user').textContent);

  const chatbox = document.getElementById(`chat-box-${orderId}`);

  // Function to scroll to the bottom of the chatbox
  function scrollToBottom() {
    chatbox.scrollTop = chatbox.scrollHeight;
  }
  scrollToBottom();


  const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/" + roomName + "/");
  currentSocket = chatSocket;

  chatSocket.onopen = function (e) {
    console.log("The connection was setup successfully !", orderId);
  };
  chatSocket.onclose = function (e) {
    console.log("WebSocket closed." , orderId);
  };
  $(`#message-input-${orderId}`).focus();
  document.querySelector(`#booster_chat_form-${orderId}`).addEventListener("submit", function (e) {
    e.preventDefault();
  });
  $(`#message-input-${orderId}`).on('keyup', function (e) {
    if (e.keyCode == 13) {
      e.preventDefault();
      $(`#message-submit-${orderId}`).click();
    }
  });
  $(`#message-submit-${orderId}`).on('click', function (e) {
    var messageInput = $(`#message-input-${orderId}`).val();

    if (messageInput.length == 0) {
      alert("Add some Input First Or Press Send Button!")
    }
    else {
      chatSocket.send(JSON.stringify({ message: messageInput, username: user, room_name: booster_room_name }));
    }

  });

  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    $('.no-messages').html('');

    let div = document.createElement("div");
    let messageContent = data.message;
    let messageElement = document.createElement("p");
    messageElement.classList.add("message", "mb-0");
    messageElement.textContent = messageContent;

    applyReadMore(messageElement)

    // Create and append the message time element
    let messageTimeElement = document.createElement("p");
    messageTimeElement.classList.add("message-time", "mb-0", "me-1");
    messageTimeElement.textContent = "Just Now";
    
    if(data.username === user){
      div.appendChild(messageTimeElement);
      div.appendChild(messageElement);
    }
    else {
      const customer_first_name = JSON.parse(document.getElementById('customer_first_name').textContent);
      const customer_last_name = JSON.parse(document.getElementById('customer_last_name').textContent);

      if (booster_image){
        div.appendChild(messageTimeElement);
        div.appendChild(messageElement);
      }

      div.innerHTML = `
          <div class="image">
            <img src="${staticUrl}" alt="" width="40" height="40">
          </div>
          <div class="message p-3 rounded-3 ">
              <p class="username mb-1">
              ${customer_first_name} ${customer_last_name}
              </p>
              <p class="content mb-1">${data.message}</p>
              <p class="text-end mb-1" style="font-size: 10px; color:#ffffffbf">Just Now</p>
          </div>
          `
    }

    // Add class based on user authentication
    if (data.username === user) {
      div.classList.add("chat-message", "userMessage");
    } else {
      if (data.message.msg_type == 2) {
        div.classList.add("tip-message");
      } else {
        div.classList.add("chat-message", "otherMessage");
      }
    }

    $(`#my_input_${orderId}`).val("");
  
    document.querySelector(`#chatbox-${orderId}`).appendChild(div);
    scrollToBottom();
  };
}

$('.finish_image').on('change', function () {
  previewImage(this);
});

function previewImage(input) {
  var preview = $(input).closest('.modal-content').find('.image-preview')[0];
  var file = input.files[0];

  if (file) {
    var reader = new FileReader();

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
customer_ids.forEach(function(element) {
  const customerId = element.dataset.customerId;
  const headStatusElement = document.getElementById(`head-state${customerId}-id`)
  const statusElement = document.getElementById(`state${customerId}-id`)
  function fetchData() {
    fetch(`/chat/status/${customerId}/`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        const message = data.status

        if (data.status == 'Online') {
          headStatusElement.innerHTML = `
          <span class="online"></span> ${message}
          `;
          statusElement.innerHTML = `
            <span class="online"></span> ${message}
          `;
        } else {
          headStatusElement.innerHTML = `
          <span class="offline"></span> Offline
          `;
          statusElement.innerHTML = `
            <span class="offline"></span> Last seen ${message}
          `;
        }
      })
      .catch(error => {
        console.warn('Error fetching data:', error);
      });
  }
  fetchData()
  setInterval(fetchData, 50000);
});
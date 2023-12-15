$('document').ready(function () {
  let ordersDivs = $('.order');
  console.log('Divs: ', ordersDivs)
  let ordersRadio = $('input[name="radio-order"]')
  // let booster_room_name = JSON.parse(document.getElementById('booster_room_name').textContent)
  // let roomName = JSON.parse(document.getElementById('room_slug').textContent);

  // Intial 
  let intialOrderId = $('input[name="radio-order"]:checked').data('order');
  console.log('intialOrderId: ', intialOrderId)
  ordersDivs.each(function () {
    let currentOrderId = $(this).data('order');
    if (currentOrderId == intialOrderId) {
      $(this).show();
      let booster_room_name = $(this).data('room');
      let roomName = $(this).data('slug');
      chat(booster_room_name, roomName, currentOrderId)
    } else {
      $(this).hide();
    }
  })

  ordersRadio.each(function () {
    let orderId = $(this).data('order');
    $(this).on('change', function () {
      ordersDivs.each(function () {
        let currentOrderId = $(this).data('order');
        if (currentOrderId == orderId) {
          $(this).show();
          let booster_room_name = $(this).data('room');
          let roomName = $(this).data('slug');
          chat(booster_room_name, roomName, currentOrderId)
          console.log(booster_room_name)
        } else {
          $(this).hide();
        }
      })
    })
  })


  var rankSelect = $('#reached_rank');
  var divisionSelect = $('#reached_division');
  var marksSelect = $('#reached_marks');

  var originalDivisionOptions = divisionSelect.html();
  var originalMarksOptions = marksSelect.html();

  function updateOptions() {
    var selectedRank = rankSelect.find(':selected');
    console.log('select Rank', selectedRank)
    var markNumber = selectedRank.data('mark');

    divisionSelect.html(originalDivisionOptions);
    marksSelect.html(originalMarksOptions);

    if (selectedRank.text().toLowerCase() === "master") {
      divisionSelect.find('option').hide();
      marksSelect.find('option').hide();
    } else {
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

  // ######################################### Chats #########################################
  function chat(booster_room_name, roomName, orderId){
    const user = JSON.parse(document.getElementById('user').textContent);
    console.log('user: ', user)
    
    const chatbox = document.querySelector("#chat-box");
  
    // Function to scroll to the bottom of the chatbox
    function scrollToBottom() {
      chatbox.scrollTop = chatbox.scrollHeight;
    }
    scrollToBottom();
  
  
    const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/" + roomName + "/");
    // const chatSocket = new WebSocket("ws://127.0.0.1:8000/ws/"+ roomName +"/");
    // alert(chatSocket);
    chatSocket.onopen = function (e) {
      console.log("The connection was setup successfully !");
    };
    chatSocket.onclose = function (e) {
      console.log("Something unexpected happened !");
    };
    $(`#my_input_${orderId}`).focus();
    document.querySelector("#booster_chat_form").addEventListener("submit", function (e) {
      e.preventDefault();
    });
    $(`#my_input_${orderId}`).on('keyup', function (e) {
      if (e.keyCode == 13) {
        e.preventDefault();
        $(`#submit_button_${orderId}`).click();
      }
    });
    $(`#submit_button_${orderId}`).on('click', function (e) {
      var messageInput = $(`#my_input_${orderId}`).val();
  
      if (messageInput.length == 0) {
        alert("Add some Input First Or Press Send Button!")
      }
      else {
        chatSocket.send(JSON.stringify({ message: messageInput, username: user, room_name: booster_room_name }));
      }
  
    });
  
    chatSocket.onmessage = function (e) {
      console.log('I am here')
      const data = JSON.parse(e.data);
      $('.noMessage').html('');
      var div = document.createElement("div");
      div.innerHTML = `
      <div class="message p-3 rounded-3 ">
          <p class="content mb-1">${data.message}</p>
          <p class="text-end mb-1" style="font-size: 10px; color:#ffffffbf">Just Now</p>
      </div>
      `
  
      // Add class based on user authentication
      if (data.username === user) {
        div.classList.add("chat-message", "userMessage");
      } else {
        div.classList.add("chat-message", "otherMessage");
      }
  
      $(`#my_input_${orderId}`).val("");
      document.querySelector("#chatbox").appendChild(div);
      scrollToBottom();
    };  
  }
  
  $('#finish_image').on('change', function () {
    previewImage(this);
  });
  
  function previewImage(input) {
    var preview = $('#image-preview')[0];
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
  
  const dropContainer = document.getElementById("dropcontainer")
  const fileInput = document.getElementById("finish_image")
  
  dropContainer.addEventListener("dragover", (e) => {
    e.preventDefault()
  }, false)
  
  dropContainer.addEventListener("dragenter", () => {
    dropContainer.classList.add("drag-active")
  })
  
  dropContainer.addEventListener("dragleave", () => {
    dropContainer.classList.remove("drag-active")
  })
  
  dropContainer.addEventListener("drop", (e) => {
    e.preventDefault()
    dropContainer.classList.remove("drag-active")
    fileInput.files = e.dataTransfer.files
    previewImage(fileInput);
  })
})
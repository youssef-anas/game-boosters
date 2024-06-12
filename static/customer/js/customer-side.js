$('document').ready(function () {
  const voiceSound = document.getElementById('notificationSound');
  // -------------------------- Chats --------------------------
  const user = JSON.parse(document.getElementById('user').textContent);
  const admin_room = JSON.parse(document.getElementById('admin_room').textContent);
  const booster_room_name = JSON.parse(document.getElementById('booster_room_name').textContent)
  const wsProtocol = window.location.protocol === "https:" ? "wss://" : "ws://";

  // -------------------------- Admins Chat --------------------------
  const admins_chatbox = document.getElementById("admin-messages-container");
  // Function to scroll to the bottom of the admins_chatbox
  function admins_scrollToBottom() {
    admins_chatbox.scrollTop = admins_chatbox.scrollHeight;
  }
  admins_scrollToBottom();

  const admins_roomName = JSON.parse(document.getElementById('admins_chat_slug').textContent);
  let adminsChatSocket = null;
  let reconnectInterval = null;
  let refreshPage = false;
  function connectAdminsChatSocket() {
    if (reconnectInterval != null){
      console.warn("retry connection")
    }
    adminsChatSocket = new WebSocket(wsProtocol + window.location.host + "/ws/chat/" + admins_roomName + "/");
    adminsChatSocket.onopen = function (e) {
      console.log("The connection was set up successfully for adminsChatSocket!");
      clearInterval(reconnectInterval);
      reconnectInterval = null;
      if (refreshPage){
        window.location.reload();
      }
    };
    adminsChatSocket.onclose = function (e) {
      console.warn("The connection was unexpectedly closed for adminsChatSocket!");
      if (!reconnectInterval) {
        refreshPage = true;
        reconnectInterval = setInterval(connectAdminsChatSocket, 5000); 
      }
    };
    document.querySelector("#admin-message-input").focus();
    document.querySelector("#booster-chat-form").addEventListener("submit", function (e) {
      e.preventDefault();
    });
    document.querySelector("#admin-message-input").addEventListener("keydown", function (e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        document.querySelector("#admin-message-submit").click();
      }
    });
    document.querySelector("#admin-message-submit").addEventListener("click", function (e) {
      var admins_messageInput = document.querySelector(
        "#admin-message-input"
      ).value;

      if (admins_messageInput.length == 0) {
        alert("Add some Input First Or Press Send Button! adminsChatSocket")
      }
      else {
        adminsChatSocket.send(JSON.stringify({ message: admins_messageInput, username: user, room_name: admin_room }));
      }
    });
    adminsChatSocket.onmessage = function (e) {
      const data = JSON.parse(e.data);
      $('.no-messages').html('');
      let div = document.createElement("div");
      let messageContent = data.message;
      let messageElement = document.createElement("p");
      messageElement.classList.add("message", "mb-0");
      messageElement.textContent = messageContent;

      applyReadMore(messageElement);

      let messageTimeElement = document.createElement("p");
      messageTimeElement.classList.add("message-time", "mb-0", "me-1");
      messageTimeElement.textContent = "Just Now";

      div.appendChild(messageTimeElement);
      div.appendChild(messageElement);

      if (data.username === user) {
        div.classList.add("admin-chat-message", "user-message");
      } else {
        div.classList.add("admin-chat-message", "admin-message");
      }

      document.querySelector("#admin-message-input").value = "";
      document.querySelector("#admin-chatbox").appendChild(div);
      admins_scrollToBottom();
    };
  }
  connectAdminsChatSocket();

  // -------------------------- Booster Chat --------------------------
  const chatbox = document.getElementById("booster-messages-container");
  // Function to scroll to the bottom of the chatbox
  function scrollToBottom() {
    chatbox.scrollTop = chatbox.scrollHeight;
  }
  scrollToBottom();

  const roomName = JSON.parse(document.getElementById('room_slug').textContent);

  // Construct the WebSocket URL using the determined protocol
  const chatSocket = new WebSocket(wsProtocol + window.location.host + "/ws/chat/" + roomName + "/");
  chatSocket.onopen = function (e) {
    console.log("The connection was setup successfully !");
  };
  chatSocket.onclose = function (e) {
    console.warn("Something unexpected happened !");
  };

  document.querySelector("#booster-message-input").focus();
  document.querySelector("#booster-chat-form").addEventListener("submit", function (e) {
    e.preventDefault();
  });

  document.querySelector("#booster-message-input").addEventListener("keydown", function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      document.querySelector("#booster-message-submit").click();
    }
  });
  document.querySelector("#booster-message-submit").addEventListener("click", function (e) {
    var messageInput = document.querySelector(
      "#booster-message-input"
    ).value;

    if (messageInput.length == 0) {
      alert("Add some Input First Or Press Send Button!")
    }
    else {
      chatSocket.send(JSON.stringify({ message: messageInput, username: user, room_name: booster_room_name }));
    }
  });

  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data.msg_type);

    $('.no-messages').html('');

    let div = document.createElement("div");
    let messageContent = data.message;
    let messageElement = document.createElement("p");

    let messageTimeElement = document.createElement("p");

    if (data.msg_type === 1) {
      messageElement.classList.add("message", "mb-0");
      messageElement.textContent = messageContent;

    } else if (data.msg_type === 3) {

      div.classList.add("booster-chat-message", "changes-message");
      div.style.backgroundColor = "transparent";

      messageElement.classList.add("info-message", "mb-0");
      messageElement.innerHTML = `<i class="fa-solid fa-circle-info ms-1"></i> ${data.message}`;

    }else if (data.msg_type === 5) {
      console.log("message type 5 refresh now");
      window.location.reload();
    }
    if (data.msg_type !== 5){
      applyReadMore(messageElement)
      messageTimeElement.classList.add("message-time", "mb-0", "me-1");
      messageTimeElement.textContent = "Just Now";
  
      if(data.username === user) {
        messageTimeElement.classList.add("message-time", "mb-0", "me-2");
        div.appendChild(messageTimeElement);
        div.appendChild(messageElement);
      }
      else {
        messageTimeElement.classList.add("message-time", "mb-0", "ms-2");
        const booster_image = JSON.parse(document.getElementById('booster_image').textContent);
  
        const imageDiv = document.createElement('div');
        imageDiv.className = 'image me-3';
  
        const imgElement = document.createElement('img');
        imgElement.src = booster_image || staticUrl; // Use booster_image if available, otherwise fallback to staticUrl
        imgElement.alt = '';
        imgElement.width = 40;
        imgElement.height = 40;
  
        imageDiv.appendChild(imgElement);
  
        div.appendChild(imageDiv);
        div.appendChild(messageElement);
        div.appendChild(messageTimeElement);
  
      }
  
      if (data.username === user) {
        if (data.message.msg_type == 2) {
          div.classList.add("booster-chat-message", "tip-message");
        } else if (data.message.msg_type == 3) {
          div.classList.add("booster-chat-message", "changes-message");
        } else if (data.message.msg_type == 4) {
          div.classList.add("booster-chat-message", "from-admin-message");
        } else {
          div.classList.add("booster-chat-message", "user-message");
        }
  
      } else {
        // run voice sound
        console.log();
        if (getSoundValue()){
          voiceSound.play();
        }

        div.classList.add("booster-chat-message", "booster-message");
      }
  
  
      document.querySelector("#booster-message-input").value = "";
      document.querySelector("#booster-chatbox").appendChild(div);
      scrollToBottom();
    }
  };


  // --------------------------- ONLINE - OFFLINE ---------------------------
  // get on line or last offline value
  const statusElement = $('.status');
  const user_id = document.getElementById('user-id').dataset.userId;
  function fetchData() {
    fetch(`/chat/status/${user_id}/`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        const message = data.status

        if (data.status == 'Online') {
          statusElement.html(`
            <span class="online"></span> ${message}
          `);
        } else {
          statusElement.html(`
            <span class="offline"></span> Last seen ${message}
          `);
        }
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }
  fetchData();
  setInterval(fetchData, 50000);
});
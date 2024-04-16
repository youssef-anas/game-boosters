// -------------------------- Chats --------------------------
const user = JSON.parse(document.getElementById('user').textContent);
const admin_room = JSON.parse(document.getElementById('admin_room').textContent);
const booster_room_name = JSON.parse(document.getElementById('booster_room_name').textContent)

// ################ Admins Chat 
const admins_chatbox = document.getElementById("admin-messages-container");
// Function to scroll to the bottom of the admins_chatbox
function admins_scrollToBottom() {
    admins_chatbox.scrollTop = admins_chatbox.scrollHeight;
}
admins_scrollToBottom();

const admins_roomName = JSON.parse(document.getElementById('admins_chat_slug').textContent);
let adminsChatSocket = null;
let reconnectInterval = null;
let refreshPage = false
const wsProtocol = window.location.protocol === "https:" ? "wss://" : "ws://";

function connectAdminsChatSocket() {
    if (reconnectInterval != null){
        console.warn("retry connection")
    }
    adminsChatSocket = new WebSocket(wsProtocol + window.location.host + "/ws/" + admins_roomName + "/");
    adminsChatSocket.onopen = function (e) {
        console.log("The connection was set up successfully for adminsChatSocket!");
        clearInterval(reconnectInterval);
        reconnectInterval = null;
        if (refreshPage){
            window.location.reload();
        }
    };
    adminsChatSocket.onclose = function (e) {
        console.log("The connection was unexpectedly closed for adminsChatSocket!");
        if (!reconnectInterval) {
            refreshPage = true
            reconnectInterval = setInterval(connectAdminsChatSocket, 5000); 
        }
    };
    document.querySelector("#admin-message-input").focus();
    document.querySelector("#booster-chat-form").addEventListener("submit", function (e) {
        e.preventDefault();
    });
    document.querySelector("#admin-message-input").onkeyup = function (e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            document.querySelector("#admin-message-submit").click();
        }
    };
    document.querySelector("#admin-message-submit").onclick = function (e) {
        var admins_messageInput = document.querySelector(
            "#admin-message-input"
        ).value;

        if (admins_messageInput.length == 0) {
            alert("Add some Input First Or Press Send Button! adminsChatSocket")
        }
        else {
            adminsChatSocket.send(JSON.stringify({ message: admins_messageInput, username: user, room_name: admin_room }));
        }

    };
    adminsChatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        $('.no-messages').html('');
        let div = document.createElement("div");
        let messageContent = data.message;
        let messageElement = document.createElement("p");
        messageElement.classList.add("message", "mb-0");
        messageElement.textContent = messageContent;
        // let message = `<p class="message mb-0">${data.message}</p>`

        applyReadMore(messageElement);

        let messageTimeElement = document.createElement("p");
        messageTimeElement.classList.add("message-time", "mb-0", "me-1");
        messageTimeElement.textContent = "Just Now";


        div.appendChild(messageTimeElement);
        div.appendChild(messageElement);

        // Add class based on user authentication
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
const chatSocket = new WebSocket(wsProtocol + window.location.host + "/ws/" + roomName + "/");
// const chatSocket = new WebSocket("ws://127.0.0.1:8000/ws/"+ roomName +"/");
// alert(chatSocket);
chatSocket.onopen = function (e) {
    console.log("The connection was setup successfully !");
};
chatSocket.onclose = function (e) {
    console.log("Something unexpected happened !");
};

document.querySelector("#booster-message-input").focus();
document.querySelector("#booster-chat-form").addEventListener("submit", function (e) {
    e.preventDefault();
});
document.querySelector("#booster-message-input").onkeyup = function (e) {
    if (e.keyCode == 13) {
        e.preventDefault();
        document.querySelector("#booster-message-submit").click();
    }
};
document.querySelector("#booster-message-submit").onclick = function (e) {
    var messageInput = document.querySelector(
        "#booster-message-input"
    ).value;

    if (messageInput.length == 0) {
        alert("Add some Input First Or Press Send Button!")
    }
    else {
        chatSocket.send(JSON.stringify({ message: messageInput, username: user, room_name: booster_room_name }));
    }

};

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    $('.no-messages').html('')
    let div = document.createElement("div");
    let messageContent = data.message;
    let messageElement = document.createElement("p");
    messageElement.classList.add("message", "mb-0");
    messageElement.textContent = messageContent;

    // let message = `<p class="message mb-0">${data.message}</p>`
    applyReadMore(messageElement)

    

    // Create and append the message time element
    let messageTimeElement = document.createElement("p");
    messageTimeElement.classList.add("message-time", "mb-0", "me-1");
    messageTimeElement.textContent = "Just Now";
    

    if(data.username === user){
        div.appendChild(messageTimeElement);
        div.appendChild(messageElement);
    }
    else{
        // const booster_first_name = JSON.parse(document.getElementById('booster_first_name').textContent);
        // const booster_last_name = JSON.parse(document.getElementById('booster_last_name').textContent);
        const booster_image = JSON.parse(document.getElementById('booster_image').textContent);

        if (booster_image){
            div.appendChild(`
            <div class="image me-3">
                <img src="${booster_image}" alt="" width="40" height="40">
            </div>`)
            div.appendChild(messageTimeElement);
            div.appendChild(messageElement);
        }
        else{
            div.append(`
            <div class="image me-3">
                <img src="${staticUrl}" alt="" width="40" height="40">
            </div>`)
            div.appendChild(messageTimeElement);
            div.appendChild(messageElement);
        }
    }

    // Add class based on user authentication
    if (data.username === user) {
        if (data.message.msg_type == 2) {
            div.classList.add("tip-message");
        } else {
            div.classList.add("booster-chat-message", "user-message");
        }
    } else {
        div.classList.add("booster-chat-message", "booster-message");
    }
    

    document.querySelector("#booster-message-input").value = "";
    document.querySelector("#booster-chatbox").appendChild(div);
    scrollToBottom();
};


// --------------------------- ONLINE - OFFLINE ---------------------------

// function formatMinutesToHourMin(minutes) {
//     var hours = Math.floor(minutes / 60);
//     var mins = minutes % 60;
//     var formattedTime = hours.toString().padStart(2, '0') + ':' + mins.toString().padStart(2, '0');
//     return formattedTime;
// }

// function formatTime(time) {
//     const seconds = time % 60;
//     const minutes = Math.floor((time % 3600) / 60);
//     const hours = Math.floor(time / 3600);
//     const days = Math.floor(time / (3600 * 24));
//     const months = Math.floor(time / (3600 * 24 * 30));

//     if (months > 0) {
//         return `${months} month${months > 1 ? 's' : ''} ago`;
//     } else if (days > 0) {
//         return `${days} day${days > 1 ? 's' : ''} ago`;
//     } else if (hours > 0) {
//         return `${hours} hour${hours > 1 ? 's' : ''} ago`;
//     } else if (minutes > 0) {
//         return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
//     } else {
//         return `${seconds} second${seconds > 1 ? 's' : ''} ago`;
//     }
// }

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
            statusElement
            if (data.status == 'online') {
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
// function fetchData() {
//     fetch(`/chat/status/${user_id}/`)
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();
//         })
//         .then(data => {
//             if (data.status == 'online'){
//                 statusElement.text(`
//                 <span class="online"></span> ${data.status}
//                 `);
               
//             }else if(data.status < 1440){
//                 const time = formatMinutesToHourMin(data.status)
//                 const message = `Last seen ${time} minute ago`
//                 statusElement.text(`
//                     <span class="offline"></span>${message}
//                 `);
//             }else if(data.status >= 1440){
//                 const days = Math.ceil(data.status / (24 * 60));
//                 const message = `Last seen ${days} days ago` 
//                 statusElement.text(`
//                     <span class="offline"></span>${message}
//                 `);
//             }else{
//                 console.warn("error whan get last online")
//             }
//         })
//         .catch(error => {
//             console.error('Error fetching data:', error);
//         });
// }



fetchData();
setInterval(fetchData, 50000);
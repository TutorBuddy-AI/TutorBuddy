document.addEventListener('DOMContentLoaded', function () {
    openSubDialog();
});


async function openSubDialog() {
    const pageBodyElement = document.querySelector('.page-content');

    try {
        const response = await fetch('./get_users');
        const responseData = await response.json();
        const users = responseData.users;

        const userList = pageBodyElement.querySelector('#userList');
        if (userList) {
            userList.innerHTML = '';
            users.forEach(async (user, index) => {
                const listItem = document.createElement('li');
                listItem.id = `contact-id-${user.id}`;
                listItem.dataset.name = user.name;
                listItem.dataset.tgId = user.tg_id;
                listItem.dataset.last_message = user.last_message;
                listItem.innerHTML = `
                    <a href="javascript: void(0);">
                        <div class="d-flex align-items-center">
                            <div class="flex-shrink-0 chat-user-img online align-self-center me-2 ms-0">
                                <div class="avatar-xxs">
                                    <img src="${user.profile}" class="rounded-circle img-fluid userprofile" alt="">
                                    <span class="user-status"></span>
                                </div>
                            </div>
                            <div class="flex-grow-1 overflow-hidden">
                                <p class="text-truncate mb-0">${user.name}</p>
                            </div>
                        </div>
                    </a>
                `;
                listItem.onclick = () => getMessageHistory(user.tg_id);
                
                userList.appendChild(listItem);

                // Execute updateUserDetails and getMessageHistory only for the first user
                if (index === 0) {
                    updateUserDetails(user.name, user.last_message, user.tg_id);
                    getMessageHistory(user.tg_id);
                }
            });
        } else {

        }
    } catch (error) {

    }
}


// ОБРАБОТЧИК КОТОРЫЙ НАКЛАДЫВАЕТ КЛАСС active НА АКТИВНЫЙ li
document.querySelector('.chat-user-list').addEventListener('click', function(event) {
    const clickedListItem = event.target.closest('li');
    if (clickedListItem) {
        // Удаляем класс "active" у предыдущего активного элемента
        const previousActiveItem = this.querySelector('li.active');
        if (previousActiveItem) {
            previousActiveItem.classList.remove('active');
        }
        // Добавляем класс "active" к текущему элементу
        clickedListItem.classList.add('active');
        
        const tgId = clickedListItem.dataset.tgId;
        const last_message = clickedListItem.dataset.last_message;
        const fullname = clickedListItem.dataset.name;
        updateUserDetails(fullname, last_message, tgId);
        getMessageHistory(tgId);
    }
});
 

// ОТПРАВКА НА СЕРВЕР ЗАПРОСА ПОУЛЧЕНИЯ ИСТОРИИ СООБЩЕНИЙ ПО ТГ АЙДИ
async function getMessageHistory(tg_id) {
   try {
      const messageHistoryResponse = await fetch(`./get_message_history_user/${tg_id}`);

      if (!messageHistoryResponse.ok) {
         throw new Error(`HTTP error Status: ${messageHistoryResponse.status}`);
      }

      const messageHistoryData = await messageHistoryResponse.json();
      displayDialog(messageHistoryData);
   } catch (error) {

   }
}

function scrollToBottom(id) {
    setTimeout(function () {
        var simpleBar = (document.getElementById(id).querySelector("#chat-conversation .simplebar-content-wrapper")) ?
            document.getElementById(id).querySelector("#chat-conversation .simplebar-content-wrapper") : ''

        var offsetHeight = document.getElementsByClassName("chat-conversation-list")[0] ?
        document.getElementById(id).getElementsByClassName("chat-conversation-list")[0].scrollHeight - window.innerHeight + 335 : 0;
        if (offsetHeight)
            simpleBar.scrollTo({
                top: offsetHeight,
                behavior: "smooth"
            });
    }, 100);
}
 
// ДИНАМИЧЕСКИ СОБИРАЕМ ДИАЛОГ
function displayDialog(chatData) {
    const conversationList = document.getElementById('users-conversation');
    conversationList.innerHTML = '';
    var currDate = null;

    chatData.chats.forEach(chat => {
        const chatListItem = document.createElement('li');
        chatListItem.classList.add('chat-list', chat.from_id === 1 ? 'left' : 'right');
        chatListItem.id = `chat-${chat.id}`;

        const conversationListContent = document.createElement('div');
        conversationListContent.classList.add('conversation-list');

        if (currDate != chat.date) {
            const chatListDate = document.createElement('li');
            chatListDate.classList.add('chat-list')
            // Добавление времени к сообщению
            const bubbleDate = document.createElement('div');
            bubbleDate.setAttribute("class", "bubble-date");

            const bubbleDateContent = document.createElement('div');
            bubbleDateContent.setAttribute("class", "bubble-date-content");

            const dateSpan = document.createElement('span');
            dateSpan.textContent = chat.date;

            bubbleDateContent.appendChild(dateSpan);
            bubbleDate.appendChild(bubbleDateContent);

            chatListDate.appendChild(bubbleDate)
            conversationList.appendChild(chatListDate);
            currDate = chat.date;
        }

        // Создание аватара
        const chatAvatar = document.createElement('div');
        chatAvatar.classList.add('chat-avatar');
        const avatarImg = document.createElement('img');
        avatarImg.src = chat.from_id === 1 ? './static/dist/images/user_chat.png' : './static/dist/images/tutorbuddy_welcome.png';
        chatAvatar.appendChild(avatarImg);

        conversationListContent.appendChild(chatAvatar);

        // Создание содержимого чата
        const userChatContent = document.createElement('div');
        userChatContent.classList.add('user-chat-content');
        const ctextWrap = document.createElement('div');
        ctextWrap.classList.add('ctext-wrap');
        const ctextWrapContent = document.createElement('div');
        ctextWrapContent.classList.add('ctext-wrap-content');
        ctextWrapContent.id = chat.id;
        const ctextContent = document.createElement('p');
        ctextContent.classList.add('mb-0', 'ctext-content');
        ctextContent.textContent = chat.msg;
        ctextWrapContent.appendChild(ctextContent);
        ctextWrap.appendChild(ctextWrapContent);
        userChatContent.appendChild(ctextWrap);

        // Добавление времени к сообщению
        const messageTime = document.createElement('small');
        messageTime.classList.add('text-muted', 'time');
        messageTime.textContent = chat.time;
        userChatContent.appendChild(messageTime);

        conversationListContent.appendChild(userChatContent);

        // Добавление элемента списка сообщений в диалог
        chatListItem.appendChild(conversationListContent);
        conversationList.appendChild(chatListItem);
    });
    scrollToBottom("users-chat");
}


// ПОИСК ПО ИМЕНИ 
document.getElementById('searchBoxDialog').addEventListener('input', function(event) {
    const searchTerm = event.target.value.toLowerCase();
    const userList = document.getElementById('userList');
    const users = userList.getElementsByTagName('li');

    Array.from(users).forEach(function(user) {
        const userName = user.querySelector('.text-truncate.mb-0').textContent.toLowerCase();
        if (userName.includes(searchTerm)) {
            user.style.display = '';
        } else {
            user.style.display = 'none';
        }
    });
});


// ШАПКА ПРОФИЛЯ ПРИ ДИАЛОГЕ 
function updateUserDetails(fullname, lastMessage, tgId) {
    const usernameLink = document.querySelector('.username[data-bs-toggle="offcanvas"]');
    const lastMessageElement = document.getElementById('lastMessageDisplay');
    const userImgDiv = document.querySelector('.flex-shrink-0.chat-user-img.online.user-own-img.align-self-center.me-3.ms-0');

    if (usernameLink) {
        usernameLink.textContent = fullname.trim();
        usernameLink.setAttribute('onclick', `openSubProfile('${tgId}')`);
    }

    info_profile_button = document.querySelector('.btn.btn-ghost-secondary.btn-icon.material-shadow-none[data-bs-toggle="offcanvas"]');
    if (info_profile_button) {
        info_profile_button.setAttribute('onclick', `openSubProfile('${tgId}')`);
    }

    if (lastMessageElement) {
        let messageText = '';
        if (lastMessage && lastMessage.trim() !== '') {
            messageText = lastMessage;
        }
        lastMessageElement.innerText = messageText.trim();
    }
    if (userImgDiv) {
        // Создаем новый элемент <img>
        const userAvatarImg = document.createElement('img');
        // Устанавливаем атрибуты
        userAvatarImg.src = './static/dist/images/user_chat.png';
        userAvatarImg.classList.add('rounded-circle', 'avatar-xs');
        userAvatarImg.alt = '';

        // Очищаем содержимое <div>
        userImgDiv.innerHTML = '';
        // Добавляем <img> в <div>
        userImgDiv.appendChild(userAvatarImg);
    }
}

// СКРОЛ БАР
var scrollEl = new SimpleBar(document.getElementById("chat-conversation"));
scrollEl.getScrollElement().scrollTop = document.getElementById("users-conversation").scrollHeight;
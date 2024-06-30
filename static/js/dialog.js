let showEmptyDialogs = true;

async function openSubDialogs() {
    closeSubSidebar();
    if (!subDialogsExists) {
        const subSidebar = document.createElement('div');
        subSidebar.className = 'sub-sidebar';

        try {
            const response = await fetch('./get_users');

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const users = await response.json();

            const titleContainer = document.createElement('div');
            titleContainer.className = 'title-container';

            const titleElement = document.createElement('h2');
            titleElement.textContent = 'Dialogs';
            titleElement.style.fontWeight = 'bold';
            titleElement.style.marginLeft = '10px';

            titleContainer.appendChild(titleElement);

            subSidebar.appendChild(titleContainer);

            const userListContainer = document.createElement('div');
            userListContainer.className = 'user-list-container';

            users.forEach(user => {
                const userBlock = document.createElement('div');
                userBlock.className = 'user-block';

                const avatarElement = document.createElement('img');
                avatarElement.src = './static/img/user_photo.webp';
                avatarElement.alt = 'Avatar';
                avatarElement.className = 'avatar';
                userBlock.appendChild(avatarElement);

                const userInfo = document.createElement('div');
                userInfo.className = 'user-info';


                const nameElement = document.createElement('p');
                nameElement.textContent = `${user.tg_firstName} ${user.tg_lastName}`;
                userInfo.appendChild(nameElement);

                const lastMessageElement = document.createElement('p');
                lastMessageElement.textContent = user.last_message;
                lastMessageElement.style.fontSize = '0.8em';
                lastMessageElement.style.color = '#888';

                userInfo.appendChild(lastMessageElement);

                userBlock.appendChild(userInfo);
                userListContainer.appendChild(userBlock);

                userBlock.addEventListener('click', async () => {
                    try {
                        const tg_id = user.tg_id;
                        const messageHistoryResponse = await fetch(`./get_message_history_user/${tg_id}`);

                        if (!messageHistoryResponse.ok) {
                            throw new Error(`HTTP error! Status: ${messageHistoryResponse.status}`);
                        }

                        const messageHistoryData = await messageHistoryResponse.json();
                        displayDialog(messageHistoryData);
                    } catch (error) {
                        console.error('Error fetching message history:', error);
                    }
                });
            });

            subSidebar.appendChild(userListContainer);
            userListContainer.lastChild.style.marginBottom = '40px';
            document.body.appendChild(subSidebar);
            subDialogsExists = true;
            closeBlock('.dialog-block');
            closeBlock('.profile-block');
            closeBlock('.statistic-block');
            closeBlock('.newsletter-info-block');
            closeBlock('.add-message-block');
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
}


// --------------------------------------------------------------------------------------



function createMessageElement(message) {
    const messageElement = document.createElement('div');
    messageElement.className = message.role === 'user' ? 'message user-message' : 'message assistant-message';

    const textElement = document.createElement('p');
    textElement.textContent = message.message;
    messageElement.appendChild(textElement);

    const timeElement = document.createElement('span');
    timeElement.textContent = message.created_at;
    timeElement.className = 'message-time';
    messageElement.appendChild(timeElement);

    return messageElement;
}


function lastMessageScroll(scrollElement, b) {
    if (!scrollElement) return;

    scrollElement.scrollIntoView({
        behavior: b || 'auto',
        block: 'end',
    });
}

function displayDialog(messages) {
    const dialogBlock = document.createElement('div');
    dialogBlock.className = 'dialog-block';
    dialogBlock.style.overflowY = 'auto';

    for (let i = 0; i < messages.length; i++) {
        const message = messages[i];
        const messageElement = createMessageElement(message);
        dialogBlock.appendChild(messageElement);
    }

    const previousDialogBlock = document.querySelector('.dialog-block');
    if (previousDialogBlock) {
        previousDialogBlock.remove();
    }

    document.body.appendChild(dialogBlock);
    lastMessageScroll(dialogBlock);
}



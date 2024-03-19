async function openSubNewsletter() {
    closeSubSidebar();
    if (!subNewsletterExists) {
        const subSidebar = document.createElement('div');
        subSidebar.className = 'newsletter-block';

        try {
            const response = await fetch('/get_newsletters');

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const newsletters = await response.json();

            const titleContainer = document.createElement('div');
            titleContainer.className = 'title-container';

            const titleElement = document.createElement('h2');
            titleElement.textContent = 'Рассылки';
            titleElement.style.fontWeight = 'bold';
            titleElement.style.marginLeft = '10px';


            titleContainer.appendChild(titleElement);
            subSidebar.appendChild(titleContainer);

            const userListContainer = document.createElement('div');
            userListContainer.className = 'user-list-container';

            newsletters.forEach(newsletter => {
                const userBlock = document.createElement('div');
                userBlock.className = 'user-block';

                const avatarElement = document.createElement('img');
                avatarElement.src = newsletter.path_to_data;
                avatarElement.alt = 'Avatar';
                avatarElement.className = 'avatar';
                userBlock.appendChild(avatarElement);

                const userInfo = document.createElement('div');
                userInfo.className = 'user-info';


                const nameElement = document.createElement('p');
                nameElement.textContent = `${newsletter.id}`;
                userInfo.appendChild(nameElement);

                userBlock.appendChild(userInfo);
                userListContainer.appendChild(userBlock);

                userBlock.addEventListener('click', async () => {
                    try {
                        const newsletter_id = newsletter.id;
                        const newsletter_infoResponse = await fetch(`/get_newsletter_info/${newsletter_id}`);

                        if (!newsletter_infoResponse.ok) {
                            throw new Error(`HTTP error! Status: ${newsletter_infoResponse.status}`);
                        }

                        const newsletterData = await newsletter_infoResponse.json();
                        displayNewsletter(newsletterData);
                    } catch (error) {
                        console.error('Error fetching:', error);
                    }
                });
            });

            subSidebar.appendChild(userListContainer);
            userListContainer.lastChild.style.marginBottom = '40px';
            document.body.appendChild(subSidebar);
            subNewsletterExists = true;
            closeBlock('.dialog-block');
            closeBlock('.profile-block');
            closeBlock('.statistic-block');
            closeBlock('.newsletter-info-block');

        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
}


function displayNewsletter(newsletter) {
    const NewsletterInfoBlock = document.createElement('div');
    NewsletterInfoBlock.className = 'newsletter-info-block';

    const titleElement = document.createElement('h2');
    titleElement.textContent = 'Информация о рассылке';

    NewsletterInfoBlock.appendChild(titleElement);

    const messageIdElement = document.createElement('p');
    messageIdElement.innerHTML = `ID: ${newsletter.id}`;

    const title_infoElement = document.createElement('p');
    title_infoElement.innerHTML = `title: ${newsletter.title}`;

    const messageElement = document.createElement('p');
    messageElement.innerHTML = `Message: ${newsletter.message}`;

    const pathToDataElement = document.createElement('p');
    pathToDataElement.innerHTML = `Path to Data: ${newsletter.path_to_data}`;

    const topicElement = document.createElement('p');
    topicElement.innerHTML= `Topic: ${newsletter.topic}`;

    const publication_dateElement = document.createElement('p');
    publication_dateElement.innerHTML = `publication_date: ${newsletter.publication_date}`;

    const editionElement = document.createElement('p');
    editionElement.innerHTML = `edition: ${newsletter.edition}`;

    const urlElement = document.createElement('p');
    urlElement.innerHTML = `URL: ${newsletter.url}`;

    const imageElement = document.createElement('img');
    imageElement.src = newsletter.path_to_data;
    imageElement.alt = 'Newsletter Image';

    const sendButton = document.createElement('button');
    sendButton.textContent = 'Отправить сейчас';
    sendButton.className = 'send-button';
    sendButton.addEventListener('click', () => {
        openSendModal(newsletter.id);
    });

    const send_datetimeButton = document.createElement('button');
    send_datetimeButton.textContent = 'Отправить по времени';
    send_datetimeButton.className = 'send-datetime-button';
    send_datetimeButton.addEventListener('click', () => {
        openSendDatetimeModal(newsletter.id);
    });


    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Удалить';
    deleteButton.className = 'delete-button';
    deleteButton.addEventListener('click', () => {
        openDeleteModal(newsletter.id);
    });

    // порядок отображение
    NewsletterInfoBlock.appendChild(sendButton);
    NewsletterInfoBlock.appendChild(send_datetimeButton);
    NewsletterInfoBlock.appendChild(deleteButton);
    NewsletterInfoBlock.appendChild(messageIdElement);
    NewsletterInfoBlock.appendChild(topicElement);
    NewsletterInfoBlock.appendChild(title_infoElement);
    NewsletterInfoBlock.appendChild(editionElement);
    NewsletterInfoBlock.appendChild(publication_dateElement);
    NewsletterInfoBlock.appendChild(messageElement);
    NewsletterInfoBlock.appendChild(urlElement);
    NewsletterInfoBlock.appendChild(pathToDataElement);
    NewsletterInfoBlock.appendChild(imageElement);


    document.body.appendChild(NewsletterInfoBlock);
}


function openDeleteModal(newsletterId) {
    document.getElementById('deleteModalNewsletterId').textContent = newsletterId;
    document.getElementById('deleteConfirmationModal').style.display = 'block';
}

function openSendModal(newsletterId) {
    document.getElementById('sendModalNewsletterId').textContent = newsletterId;
    document.getElementById('sendConfirmationModal').style.display = 'block';
}

function openSendDatetimeModal(newsletterId) {
    document.getElementById('sendDatetimeModalNewsletterId').textContent = newsletterId;
    document.getElementById('sendDatetimeConfirmationModal').style.display = 'block';
}

function confirmDeletion() {
    const newsletterId = document.getElementById('deleteModalNewsletterId').textContent;

    fetch(`/del_newsletter/${newsletterId}`, {
        method: 'DELETE'
    })
    .then((delete_newsletter_Response) => {
        if (!delete_newsletter_Response.ok) {
            throw new Error(`HTTP error! Status: ${delete_newsletter_Response.status}`);
        }
        return delete_newsletter_Response.json();
    })
    .then((result_delete_newsletter) => {
        window.location.reload();
    })
    .catch((error) => {
        console.error('Error:', error);
    })
    .finally(() => {
        closeModal('deleteConfirmationModal');
    });
}



function confirmSend() {
    const newsletterId = document.getElementById('sendModalNewsletterId').textContent;
    fetch(`/send_newsletter/${newsletterId}`, {
        method: 'GET'
    })
    .then((send_newsletter_Response) => {
        if (!send_newsletter_Response.ok) {
            throw new Error(`HTTP error! Status: ${send_newsletter_Response.status}`);
        }
        return send_newsletter_Response.json();
    })
    .then((result_send_newsletter) => {
        window.location.reload();
    })
    .catch((error) => {
        console.error('Error:', error);
    })
    .finally(() => {
        closeModal('sendConfirmationModal');
    });
}


function confirmSendDatetime() {
    const newsletterId = document.getElementById('sendDatetimeModalNewsletterId').textContent;
    //TODO change url !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    //TODO Написать логику отправки через время когда примут pr
    //TODO change url !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    fetch(`/send_newsletter/${newsletterId}`, {
        method: 'GET'
    })
    .then((send_newsletter_Response) => {
        if (!send_newsletter_Response.ok) {
            throw new Error(`HTTP error! Status: ${send_newsletter_Response.status}`);
        }
        return send_newsletter_Response.json();
    })
    .then((result_send_newsletter) => {
        window.location.reload();
    })
    .catch((error) => {
        console.error('Error:', error);
    })
    .finally(() => {
        closeModal('sendDatetimeConfirmationModal');
    });
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

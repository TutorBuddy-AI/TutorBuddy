async function openSubAddNewsletter() {
    closeSubSidebar();

    if (!subAddNewsletterExists) {
        const subSidebar = document.createElement('div');
        subSidebar.className = 'add-newsletter-block';

        const statisticsContainer = document.createElement('div');
        const AddNewsletterContainer = document.createElement('div');

        AddNewsletterContainer.innerHTML = `
            <div>
                <form id="addNewsletterForm">
                    <label for="topic">Тема:</label>
                    <div contenteditable="true" id="topic" name="topic" required></div>

                    <label for="url">URL:</label>
                    <div contenteditable="true" id="url" name="url" required></div>

                    <label for="title">Заголовок:</label>
                    <div contenteditable="true" id="title" name="title" required></div>

                    <label for="message">Сообщение:</label>
                    <div contenteditable="true" id="message" name="message" required></div>

                    <label for="edition">Издание(Необязательно):</label>
                    <div contenteditable="true" id="edition" name="edition"></div>

                    <label for="publication_date">Дата публикации(Необязательно):</label>
                    <div contenteditable="true" id="publication_date" name="publication_date"></div>

                    <label for="image">Изображение:</label>
                    <input type="file" id="image" name="image" accept="image/*">

                    <input type="submit" value="Сохранить">
                </form>
                <div id="resultContainer"></div>
            </div>
        `;

        statisticsContainer.appendChild(AddNewsletterContainer);
        subSidebar.appendChild(statisticsContainer);
        document.body.appendChild(subSidebar);

        document.getElementById('addNewsletterForm').addEventListener('submit', async function (event) {
            event.preventDefault();

        const topic = document.getElementById('topic').innerHTML;
        const url = document.getElementById('url').innerHTML;
        const title = document.getElementById('title').innerHTML;
        const message = document.getElementById('message').innerHTML;
        const edition = document.getElementById('edition').innerHTML;
        const publication_date = document.getElementById('publication_date').innerHTML;
        const imageInput = document.getElementById('image');


            if (imageInput.files.length > 0) {
                const imageFile = imageInput.files[0];
                const reader = new FileReader();

                reader.onload = async function (e) {
                    const buffer = e.target.result;
                    const bytes = new Uint8Array(buffer);
                    let binary = '';

                    for (let i = 0; i < bytes.byteLength; i++) {
                        binary += String.fromCharCode(bytes[i]);
                    }

                    const imageBase64 = btoa(binary);

                    const requestData = {
                        topic: topic,
                        url: url,
                        message: message,
                        title: title,
                        edition: edition,
                        publication_date: publication_date,
                        image: imageBase64,
                    };
                    console.log(requestData)
                    try {
                        const response = await fetch('/save-newsletter', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(requestData),
                        });

                        const result = await response.json();
                        console.log(result);

                        const resultContainer = document.getElementById('resultContainer');
                        resultContainer.innerHTML = `<p class="success-add-newsletter">${JSON.stringify(result)}</p>`;
                        document.getElementById('addNewsletterForm').reset();

                        subAddNewsletterExists = true;
                        closeBlock('.dialog-block');
                        closeBlock('.profile-block');
                        closeBlock('.statistic-block');
                        closeBlock('.newsletter-info-block');
                    } catch (error) {
                        console.error('Ошибка при сохранении рассылки:', error);
                        const resultContainer = document.getElementById('resultContainer');
                        resultContainer.innerHTML = `<p class="error-add-newsletter">Ошибка при сохранении рассылки: ${JSON.stringify(error)}</p>`;
                    }
                };

                reader.readAsArrayBuffer(imageFile);
            }
        });
    }
}




document.addEventListener('DOMContentLoaded', function () {
    let isButtonsShown = false; // Флаг для отслеживания, показаны ли уже кнопки
    let selectionButtonsContainer = null; // Контейнер для кнопок

    // Функция для применения стилей к выделенному тексту
    function applyStyle(style, value) {
        document.execCommand(style, false, value);
    }

    // Функция для применения tg-spoiler к выделенному тексту
    function applyTgSpoiler(value) {
        const tgSpoilerHTML = `<span class="tg-spoiler">${value}</span>`;
        document.execCommand('insertHTML', false, tgSpoilerHTML);
    }



    // Обработчик события выделения текста
    document.addEventListener('selectionchange', function () {
        const selection = window.getSelection();
        const isContentEditable = selection.anchorNode && selection.anchorNode.parentElement && selection.anchorNode.parentElement.getAttribute('contenteditable') === 'true';

        console.log('Is content editable:', isContentEditable);

        if (isContentEditable && selection.toString().length > 0 && !isButtonsShown) {
            // Показываем кнопки только если что-то выделено это внутри контейнера с contenteditable и кнопки еще не были показаны
            selectionButtonsContainer = document.createElement('div');
            selectionButtonsContainer.className = 'selection-buttons-container';

            // Создаем кнопку "B" (жирный)
            const boldButton = document.createElement('button');
            boldButton.textContent = 'B';
            boldButton.style.fontWeight = 'bold';
            boldButton.addEventListener('click', function () {
                applyStyle('bold');
            });
            selectionButtonsContainer.appendChild(boldButton);

            // Создаем кнопку "I" (курсив)
            const italicButton = document.createElement('button');
            italicButton.textContent = 'I';
            italicButton.style.fontStyle = 'italic';
            italicButton.addEventListener('click', function () {
                applyStyle('italic');
            });
            italicButton.style.marginLeft = '10px';
            selectionButtonsContainer.appendChild(italicButton);


            // Создаем кнопку "A" (подчеркнутый)
            const underlineButton = document.createElement('button');
            underlineButton.textContent = 'A';
            underlineButton.style.textDecoration = 'underline';
            underlineButton.addEventListener('click', function () {
                applyStyle('underline');
            });
            underlineButton.style.marginLeft = '10px';
            selectionButtonsContainer.appendChild(underlineButton);


            // Создаем кнопку "S" (зачеркнутый)
            const strikeButton = document.createElement('button');
            strikeButton.textContent = 'S';
            strikeButton.addEventListener('click', function () {
                applyStyle('strikeThrough');
            });
            strikeButton.style.textDecoration = 'line-through';
            strikeButton.style.marginLeft = '10px';
            selectionButtonsContainer.appendChild(strikeButton);


            // Создаем кнопку "tg-spoiler" (tg-spoiler)
            const TgSpoilerButton = document.createElement('button');
            TgSpoilerButton.textContent = 'tg-spoiler';
            TgSpoilerButton.addEventListener('click', function () {
                const selection = window.getSelection();
                const selectedText = selection.toString();
                applyTgSpoiler(selectedText);
            });
            TgSpoilerButton.style.marginLeft = '10px';
            selectionButtonsContainer.appendChild(TgSpoilerButton);


            // Устанавливаем позицию контейнера с кнопками под выделенным текстом
            const range = selection.getRangeAt(0);
            const rect = range.getBoundingClientRect();

            selectionButtonsContainer.style.position = 'absolute';
            selectionButtonsContainer.style.top = `${rect.bottom}px`;
            selectionButtonsContainer.style.left = `${rect.left}px`;


            document.body.appendChild(selectionButtonsContainer);

            isButtonsShown = true; // Устанавливаем флаг, что кнопки были показаны
        } else if (!isContentEditable || selection.toString().length === 0) {
            // Скрываем кнопки если нет выделения или выделение не в контейнере contenteditable
            if (selectionButtonsContainer) {
                selectionButtonsContainer.remove();
                selectionButtonsContainer = null;
            }

            isButtonsShown = false; // Сбрасываем флаг, если выделение потеряно
        }
    });
});


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


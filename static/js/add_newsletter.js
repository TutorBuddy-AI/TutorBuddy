async function openSubAddNewsletter() {
    closeSubSidebar();

    if (!subAddNewsletterExists) {
        const subSidebar = document.createElement('div');
        subSidebar.className = 'add-newsletter-block';

        const AddNewsletterContainer = document.createElement('div');

        AddNewsletterContainer.innerHTML = `
            <div>
                <form id="addNewsletterForm">
                    <label for="topic">Topic:</label>
                    <div contenteditable="true" id="topic" name="topic" required></div>

                    <label for="title">Title:</label>
                    <div contenteditable="true" id="title" name="title" required></div>

                    <label for="edition">Edition (Optional):</label>
                    <div contenteditable="true" id="edition" name="edition"></div>

                    <label for="publication_date">Publication Date (Optional):</label>
                    <div contenteditable="true" id="publication_date" name="publication_date"></div>

                    <label for="message">Message:</label>
                    <div contenteditable="true" id="message" name="message" required></div>

                    <label for="url">URL:</label>
                    <div contenteditable="true" id="url" name="url" required></div>

                    <label for="image">Image:</label>
                    <input type="file" id="image" name="image" accept="image/*">

                    <input type="submit" value="Сохранить">
                </form>
                <div id="resultContainer"></div>
            </div>
        `;


        subSidebar.appendChild(AddNewsletterContainer);
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

                    try {
                        const response = await fetch('/save-newsletter', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(requestData),
                        });

                        const result = await response.json();


                        const resultContainer = document.getElementById('resultContainer');
                        resultContainer.innerHTML = `<p class="success-add-newsletter">${JSON.stringify(result)}</p>`;
                        document.getElementById('addNewsletterForm').reset();

                        subAddNewsletterExists = true;
                        closeBlock('.dialog-block');
                        closeBlock('.profile-block');
                        closeBlock('.statistic-block');
                        closeBlock('.newsletter-info-block');
                        closeBlock('.add-message-block');
                    } catch (error) {
                        const resultContainer = document.getElementById('resultContainer');
                        resultContainer.innerHTML = `<p class="error-add-newsletter">Error while saving newsletter: ${JSON.stringify(error)}</p>`;
                    }
                };

                reader.readAsArrayBuffer(imageFile);
            }
        });
    }
}

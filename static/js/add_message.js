async function openSubAdd_Message() {
    closeSubSidebar();

    if (!subAddMessageExists) {
        const subSidebar = document.createElement('div');
        subSidebar.className = 'add-message-block';

        const addMessageContainer = document.createElement('div');
        const addMessageForm = document.createElement('div');

        addMessageForm.innerHTML = `
            <div>
                <form id="AddMessageForm">
                    <label for="message">Message:</label>
                    <div contenteditable="true" id="message" name="message" required></div>

                    <label for="image">Image:</label>
                    <input type="file" id="image" name="image" accept="image/*">

                    <input type="submit" value="Save">
                </form>
                <div id="resultContainer"></div>
            </div>
        `;


        addMessageContainer.appendChild(addMessageForm);
        subSidebar.appendChild(addMessageContainer);
        document.body.appendChild(subSidebar);

        document.getElementById('AddMessageForm').addEventListener('submit', async function (event) {
            event.preventDefault();

            const message = document.getElementById('message').innerHTML;
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
                        message: message,
                        image: imageBase64,
                    };

                    try {
                        const response = await fetch('/save-message', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(requestData),
                        });

                        const result = await response.json();

                        const resultContainer = document.getElementById('resultContainer');
                        resultContainer.innerHTML = `<p class="success-add-message">${JSON.stringify(result)}</p>`;
                        document.getElementById('AddMessageForm').reset();

                        subAddMessageExists = true;
                        closeBlock('.dialog-block');
                        closeBlock('.profile-block');
                        closeBlock('.statistic-block');
                        closeBlock('.newsletter-info-block');
                    } catch (error) {
                        const resultContainer = document.getElementById('resultContainer');
                        resultContainer.innerHTML = `<p class="error-add-message">Error while saving message: ${JSON.stringify(error)}</p>`;
                    }
                };

                reader.readAsArrayBuffer(imageFile);
            }
        });
    }
}

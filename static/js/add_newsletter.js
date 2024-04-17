async function openSubAddNewsletter() {
    const pageTitle = document.getElementById('page-title');
    pageTitle.innerHTML = 'Add newsletter message';
    const passField = document.getElementById("main_content_cont");
    passField.innerHTML = '';

    const AddNewsletterContainer = document.createElement('div');

    AddNewsletterContainer.innerHTML = `
        <div class="col-md-12">
          <form class="card" id="addNewsletterForm">
            <div class="card-body">
              <div class="mb-3">
                <label class="form-label required">Topic</label>
                <div>
                  <select class="form-select" multiple="" id="topic">
                    <option value="psychology">Psychology</option>
                    <option value="business">Business</option>
                    <option value="startups">StartUps</option>
                    <option value="innovations">Innovations</option>
                    <option value="fashion">Fashion</option>
                    <option value="art">Art&Design</option>
                    <option value="games">Games</option>
                    <option value="science">Science</option>
                    <option value="travel">Travel</option>
                    <option value="books">Books</option>
                    <option value="sports">Sports</option>
                    <option value="health">Health</option>
                    <option value="movies">Movies</option>
                  </select>
                  <input type="text" class="form-control" placeholder="Article Topic" id="topic">
                </div>
              </div>
              <label class="form-label">Message content<span class="form-label-description" id="message-len">0</span></label>
              <fieldset class="form-fieldset">
                  <div class="mb-3">
                    <label class="form-label required">Title<span class="form-label-description" id="title-len">0</span></label>
                    <div>
                      <input type="text" class="form-control" placeholder="New Title" id="title">
                    </div>
                  </div>
                  <div class="mb-3">
                    <label class="form-label">Publisher<span class="form-label-description" id="publisher-len">0</span></label>
                    <div>
                      <input type="text" class="form-control" placeholder="Article Publisher" id="publisher">
                    </div>
                  </div>
                  <div class="mb-3">
                    <label class="form-label">Publication Date<span class="form-label-description" id="publication-date-len">0</span></label>
                    <div>
                      <input type="text" class="form-control" placeholder="Publication Date"  id="publication_date">
                    </div>
                  </div>
                  <div class="mb-3">
                    <label class="form-label required">Article text<span class="form-label-description" id="article-len">0</span></label>
                    <textarea class="form-control" name="example-textarea-input" rows="6" placeholder="Content.." style="height: 218px;" id="message">
                    </textarea>
                  </div>
              </fieldset>
              <div class="mb-3">
                <label class="form-label required">URL</label>
                <div>
                  <input type="text" class="form-control" placeholder="Article URL" id="url">
                </div>
              </div>
              <div class="mb-3">
                <div class="form-label required">Message Image</div>
                <input type="file" class="form-control" wfd-id="id155" accept="image/*" id="image">
              </div>
            </div>
            <div class="card-footer text-end">
              <div id="resultContainer"></div>
              <button type="submit" class="btn btn-primary">Submit</button>
            </div>
          </form>
        </div>
    `;
    passField.appendChild(AddNewsletterContainer);
    document.getElementById('addNewsletterForm').addEventListener('submit', async function (event) {
        event.preventDefault();

        const topic = document.getElementById('topic').value;
        const url = document.getElementById('url').innerHTML;
        const title = document.getElementById('title').innerHTML;
        const message = document.getElementById('message').innerHTML;
        const publisher = document.getElementById('publisher').innerHTML;
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
                    publisher: publisher,
                    publication_date: publication_date,
                    image: imageBase64,
                };

                try {
                    const response = await fetch('./save-newsletter', {
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
                } catch (error) {
                    const resultContainer = document.getElementById('resultContainer');
                    resultContainer.innerHTML = `<p class="error-add-newsletter">Error while saving newsletter: ${JSON.stringify(error)}</p>`;
                }
            };
            reader.readAsArrayBuffer(imageFile);
        }
        else {
            const resultContainer = document.getElementById('resultContainer');
        }
    });
}

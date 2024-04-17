async function openSubSendMessage() {
    const pageTitle = document.getElementById('page-title');
    pageTitle.innerHTML = 'Send message';
    const passField = document.getElementById("main_content_cont");
    passField.innerHTML = '';

    const SendMessageContainer = document.createElement('div');

    SendMessageContainer.innerHTML = `
        <div class="col-md-12">
          <form class="card" id="sendMessageForm">
            <div class="card-body">
              <div class="mb-3">
                <label class="form-label required">Message text<span class="form-label-description" id="article-len">0</span></label>
                <textarea class="form-control" name="example-textarea-input" rows="6" placeholder="Content.." style="height: 218px;" id="message">
                </textarea>
              </div>
              <div class="mb-3">
                <div class="form-label">Message Image</div>
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
    passField.appendChild(SendMessageContainer);


//    let options = {
//      mode : "textareas",
//      height: 300,
//      menubar: false,
//      statusbar: false,
//      plugins: [
//        "advlist", "autolink", "lists", "link", "image",
//         "charmap", "preview", "anchor",
//         "searchreplace", "visualblocks", "code", "fullscreen",
//         "insertdatetime", "media", "table", "code", "help", "wordcount"
//      ],
//      toolbar: 'undo redo | formatselect | ' +
//        'bold italic backcolor | alignleft aligncenter ' +
//        'alignright alignjustify | bullist numlist outdent indent | ' +
//        'removeformat code',
//      content_style: 'body { font-family: -apple-system, BlinkMacSystemFont, San Francisco, Segoe UI, Roboto, Helvetica Neue, sans-serif; font-size: 14px; -webkit-font-smoothing: antialiased; }',
//      //paste Core plugin options
//      // paste_block_drop: false,
//      //paste_data_images: false,
//      //paste_as_text: false,
//      force_br_newlines : true,
//      force_p_newlines : false,
//      forced_root_block : false,
//      convert_newlines_to_brs: true,
//      valid_elements: "span[class],strong/b,i/em,code,strike,br", //class="tg-spoiler"
//      invalid_elements: 'div,img,a,table,td,th,tr,header,font,body,h,h1,h2,h3,h4,h5',
//      invalid_styles: 'color font-size text-decoration font-weight'
//    }
//    if (localStorage.getItem("xdialerTheme") === 'dark') {
//      options.skin = 'oxide-dark';
//      options.content_css = 'dark';
//    }
    let options = {
  theme : "advanced",
  mode : "textareas",
    theme_advanced_buttons1 : "bold,italic,underline,undo,redo,link,unlink,image,forecolor,styleselect,removeformat,cleanup,code",
  theme_advanced_buttons2 : "",
  theme_advanced_buttons3 : "",
  theme_advanced_toolbar_location : "top",
  theme_advanced_toolbar_align : "center",
//        force_br_newlines : true,
//      force_p_newlines : false,
      forced_root_block : false,
//      convert_newlines_to_brs: true,
      valid_elements: "span[class],strong/b,i/em,code,strike,br", //class="tg-spoiler"
      invalid_elements: 'div,img,a,table,td,th,tr,header,font,body,h,h1,h2,h3,h4,h5',
      invalid_styles: 'color font-size text-decoration font-weight',
      width: "100%"
    };
    tinyMCE.init(options);

    document.getElementById('sendMessageForm').addEventListener('submit', async function (event) {
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
                    const response = await fetch('./send-message', {
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
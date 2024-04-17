async function openSubSendMessage2() {
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
              <div class="mb-3">
                <div role="application" class="tox tox-tinymce" style="visibility: hidden; height: 300px;" aria-disabled="false">
                    <div class="tox-editor-container">
                        <div data-alloy-vertical-dir="toptobottom" class="tox-editor-header">
                            <div role="group" class="tox-toolbar-overlord" aria-disabled="false">
                                <div role="group" class="tox-toolbar__primary">
                                    <div title="" role="toolbar" data-alloy-tabstop="true" tabindex="-1" class="tox-toolbar__group">
                                        <button aria-label="Undo" title="Undo" type="button" tabindex="-1" class="tox-tbtn" aria-disabled="false" style="width: 34px;">
                                            <span class="tox-icon tox-tbtn__icon-wrap">
                                                <svg width="24" height="24" focusable="false"><path d="M6.4 8H12c3.7 0 6.2 2 6.8 5.1.6 2.7-.4 5.6-2.3 6.8a1 1 0 0 1-1-1.8c1.1-.6 1.8-2.7 1.4-4.6-.5-2.1-2.1-3.5-4.9-3.5H6.4l3.3 3.3a1 1 0 1 1-1.4 1.4l-5-5a1 1 0 0 1 0-1.4l5-5a1 1 0 0 1 1.4 1.4L6.4 8Z" fill-rule="nonzero"></path></svg>
                                            </span>
                                        </button>
                                        <button aria-label="Redo" title="Redo" type="button" tabindex="-1" class="tox-tbtn tox-tbtn--disabled" aria-disabled="true" style="width: 34px;">
                                            <span class="tox-icon tox-tbtn__icon-wrap">
                                                <svg width="24" height="24" focusable="false"><path d="M17.6 10H12c-2.8 0-4.4 1.4-4.9 3.5-.4 2 .3 4 1.4 4.6a1 1 0 1 1-1 1.8c-2-1.2-2.9-4.1-2.3-6.8.6-3 3-5.1 6.8-5.1h5.6l-3.3-3.3a1 1 0 1 1 1.4-1.4l5 5a1 1 0 0 1 0 1.4l-5 5a1 1 0 0 1-1.4-1.4l3.3-3.3Z" fill-rule="nonzero"></path></svg>
                                            </span>
                                        </button></div><div title="" role="toolbar" data-alloy-tabstop="true" tabindex="-1" class="tox-toolbar__group">
                                        <button aria-label="Bold" title="Bold" type="button" tabindex="-1" class="tox-tbtn" aria-disabled="false" aria-pressed="false" style="width: 34px;">
                                            <span class="tox-icon tox-tbtn__icon-wrap">
                                                <svg width="24" height="24" focusable="false"><path d="M7.8 19c-.3 0-.5 0-.6-.2l-.2-.5V5.7c0-.2 0-.4.2-.5l.6-.2h5c1.5 0 2.7.3 3.5 1 .7.6 1.1 1.4 1.1 2.5a3 3 0 0 1-.6 1.9c-.4.6-1 1-1.6 1.2.4.1.9.3 1.3.6s.8.7 1 1.2c.4.4.5 1 .5 1.6 0 1.3-.4 2.3-1.3 3-.8.7-2.1 1-3.8 1H7.8Zm5-8.3c.6 0 1.2-.1 1.6-.5.4-.3.6-.7.6-1.3 0-1.1-.8-1.7-2.3-1.7H9.3v3.5h3.4Zm.5 6c.7 0 1.3-.1 1.7-.4.4-.4.6-.9.6-1.5s-.2-1-.7-1.4c-.4-.3-1-.4-2-.4H9.4v3.8h4Z" fill-rule="evenodd"></path></svg>
                                            </span>
                                        </button><button aria-label="Italic" title="Italic" type="button" tabindex="-1" class="tox-tbtn" aria-disabled="false" aria-pressed="false" style="width: 34px;">
                                            <span class="tox-icon tox-tbtn__icon-wrap">
                                                <svg width="24" height="24" focusable="false"><path d="m16.7 4.7-.1.9h-.3c-.6 0-1 0-1.4.3-.3.3-.4.6-.5 1.1l-2.1 9.8v.6c0 .5.4.8 1.4.8h.2l-.2.8H8l.2-.8h.2c1.1 0 1.8-.5 2-1.5l2-9.8.1-.5c0-.6-.4-.8-1.4-.8h-.3l.2-.9h5.8Z" fill-rule="evenodd"></path></svg>
                                            </span>
                                        </button>


                                        <div aria-pressed="false" aria-label="Background color" title="Background color" role="button" aria-haspopup="true" tabindex="-1" unselectable="on" class="tox-split-button" style="user-select: none;" aria-disabled="false" aria-expanded="false" aria-describedby="aria_1388481641481713124470083">
                                            <span role="presentation" class="tox-tbtn" aria-disabled="false" style="width: 34px;">
                                                <span class="tox-icon tox-tbtn__icon-wrap">
                                                    <svg width="24" height="24" focusable="false"><g fill-rule="evenodd"><path id="tox-icon-highlight-bg-color__color" d="M3 18h18v3H3z" fill="#000000"></path><path fill-rule="nonzero" d="M7.7 16.7H3l3.3-3.3-.7-.8L10.2 8l4 4.1-4 4.2c-.2.2-.6.2-.8 0l-.6-.7-1.1 1.1zm5-7.5L11 7.4l3-2.9a2 2 0 0 1 2.6 0L18 6c.7.7.7 2 0 2.7l-2.9 2.9-1.8-1.8-.5-.6"></path></g></svg>
                                                </span>
                                            </span>
                                            <span role="presentation" class="tox-tbtn tox-split-button__chevron" aria-disabled="false">
                                                <svg width="10" height="10" focusable="false"><path d="M8.7 2.2c.3-.3.8-.3 1 0 .4.4.4.9 0 1.2L5.7 7.8c-.3.3-.9.3-1.2 0L.2 3.4a.8.8 0 0 1 0-1.2c.3-.3.8-.3 1.1 0L5 6l3.7-3.8Z" fill-rule="nonzero"></path></svg>
                                            </span>
                                            <span aria-hidden="true" style="display: none;" id="aria_1388481641481713124470083">To open the popup, press Shift+Enter
                                            </span>
                                        </div>
                                    </div>
                                    <div title="" role="toolbar" data-alloy-tabstop="true" tabindex="-1" class="tox-toolbar__group">
                                        <button aria-label="Align left" title="Align left" type="button" tabindex="-1" class="tox-tbtn" aria-disabled="false" aria-pressed="false" style="width: 34px;">
                                            <span class="tox-icon tox-tbtn__icon-wrap">
                                                <svg width="24" height="24" focusable="false"><path d="M5 5h14c.6 0 1 .4 1 1s-.4 1-1 1H5a1 1 0 1 1 0-2Zm0 4h8c.6 0 1 .4 1 1s-.4 1-1 1H5a1 1 0 1 1 0-2Zm0 8h8c.6 0 1 .4 1 1s-.4 1-1 1H5a1 1 0 0 1 0-2Zm0-4h14c.6 0 1 .4 1 1s-.4 1-1 1H5a1 1 0 0 1 0-2Z" fill-rule="evenodd"></path></svg>
                                            </span>
                                        </button>
                                        <button aria-label="Align center" title="Align center" type="button" tabindex="-1" class="tox-tbtn" aria-disabled="false" aria-pressed="false" style="width: 34px;">
                                            <span class="tox-icon tox-tbtn__icon-wrap">
                                                <svg width="24" height="24" focusable="false"><path d="M5 5h14c.6 0 1 .4 1 1s-.4 1-1 1H5a1 1 0 1 1 0-2Zm3 4h8c.6 0 1 .4 1 1s-.4 1-1 1H8a1 1 0 1 1 0-2Zm0 8h8c.6 0 1 .4 1 1s-.4 1-1 1H8a1 1 0 0 1 0-2Zm-3-4h14c.6 0 1 .4 1 1s-.4 1-1 1H5a1 1 0 0 1 0-2Z" fill-rule="evenodd"></path></svg>
                                            </span>
                                        </button>
                                        <button aria-label="Align right" title="Align right" type="button" tabindex="-1" class="tox-tbtn" aria-disabled="false" aria-pressed="false" style="width: 34px;">
                                            <span class="tox-icon tox-tbtn__icon-wrap">
                                                <svg width="24" height="24" focusable="false"><path d="M5 5h14c.6 0 1 .4 1 1s-.4 1-1 1H5a1 1 0 1 1 0-2Zm6 4h8c.6 0 1 .4 1 1s-.4 1-1 1h-8a1 1 0 0 1 0-2Zm0 8h8c.6 0 1 .4 1 1s-.4 1-1 1h-8a1 1 0 0 1 0-2Zm-6-4h14c.6 0 1 .4 1 1s-.4 1-1 1H5a1 1 0 0 1 0-2Z" fill-rule="evenodd"></path></svg>
                                            </span>
                                        </button>
                                        <button aria-label="Justify" title="Justify" type="button" tabindex="-1" class="tox-tbtn" aria-disabled="false" aria-pressed="false" style="width: 34px;">
                                            <span class="tox-icon tox-tbtn__icon-wrap">
                                                <svg width="24" height="24" focusable="false"><path d="M5 5h14c.6 0 1 .4 1 1s-.4 1-1 1H5a1 1 0 1 1 0-2Zm0 4h14c.6 0 1 .4 1 1s-.4 1-1 1H5a1 1 0 1 1 0-2Zm0 4h14c.6 0 1 .4 1 1s-.4 1-1 1H5a1 1 0 0 1 0-2Zm0 4h14c.6 0 1 .4 1 1s-.4 1-1 1H5a1 1 0 0 1 0-2Z" fill-rule="evenodd"></path></svg>
                                            </span>
                                        </button>
                                    </div>
                                    <div title="" role="toolbar" data-alloy-tabstop="true" tabindex="-1" class="tox-toolbar__group">
                                        <div aria-pressed="false" aria-label="Bullet list" title="Bullet list" role="button" aria-haspopup="true" tabindex="-1" unselectable="on" class="tox-split-button" style="user-select: none;" aria-disabled="false" aria-expanded="false" aria-describedby="aria_3671907801491713124470087">
                                            <span role="presentation" class="tox-tbtn" aria-disabled="false" style="width: 34px;">
                                                <span class="tox-icon tox-tbtn__icon-wrap">
                                                    <svg width="24" height="24" focusable="false"><path d="M11 5h8c.6 0 1 .4 1 1s-.4 1-1 1h-8a1 1 0 0 1 0-2Zm0 6h8c.6 0 1 .4 1 1s-.4 1-1 1h-8a1 1 0 0 1 0-2Zm0 6h8c.6 0 1 .4 1 1s-.4 1-1 1h-8a1 1 0 0 1 0-2ZM4.5 6c0-.4.1-.8.4-1 .3-.4.7-.5 1.1-.5.4 0 .8.1 1 .4.4.3.5.7.5 1.1 0 .4-.1.8-.4 1-.3.4-.7.5-1.1.5-.4 0-.8-.1-1-.4-.4-.3-.5-.7-.5-1.1Zm0 6c0-.4.1-.8.4-1 .3-.4.7-.5 1.1-.5.4 0 .8.1 1 .4.4.3.5.7.5 1.1 0 .4-.1.8-.4 1-.3.4-.7.5-1.1.5-.4 0-.8-.1-1-.4-.4-.3-.5-.7-.5-1.1Zm0 6c0-.4.1-.8.4-1 .3-.4.7-.5 1.1-.5.4 0 .8.1 1 .4.4.3.5.7.5 1.1 0 .4-.1.8-.4 1-.3.4-.7.5-1.1.5-.4 0-.8-.1-1-.4-.4-.3-.5-.7-.5-1.1Z" fill-rule="evenodd"></path></svg>
                                                </span>
                                            </span>
                                            <span role="presentation" class="tox-tbtn tox-split-button__chevron" aria-disabled="false">
                                                <svg width="10" height="10" focusable="false"><path d="M8.7 2.2c.3-.3.8-.3 1 0 .4.4.4.9 0 1.2L5.7 7.8c-.3.3-.9.3-1.2 0L.2 3.4a.8.8 0 0 1 0-1.2c.3-.3.8-.3 1.1 0L5 6l3.7-3.8Z" fill-rule="nonzero"></path></svg>
                                            </span>
                                            <span aria-hidden="true" style="display: none;" id="aria_3671907801491713124470087">To open the popup, press Shift+Enter
                                            </span>
                                        </div>
                                        <div aria-pressed="false" aria-label="Numbered list" title="Numbered list" role="button" aria-haspopup="true" tabindex="-1" unselectable="on" class="tox-split-button" style="user-select: none;" aria-disabled="false" aria-expanded="false" aria-describedby="aria_1730645381501713124470088">
                                            <span role="presentation" class="tox-tbtn" aria-disabled="false" style="width: 34px;">
                                                <span class="tox-icon tox-tbtn__icon-wrap">
                                                    <svg width="24" height="24" focusable="false"><path d="M10 17h8c.6 0 1 .4 1 1s-.4 1-1 1h-8a1 1 0 0 1 0-2Zm0-6h8c.6 0 1 .4 1 1s-.4 1-1 1h-8a1 1 0 0 1 0-2Zm0-6h8c.6 0 1 .4 1 1s-.4 1-1 1h-8a1 1 0 1 1 0-2ZM6 4v3.5c0 .3-.2.5-.5.5a.5.5 0 0 1-.5-.5V5h-.5a.5.5 0 0 1 0-1H6Zm-1 8.8.2.2h1.3c.3 0 .5.2.5.5s-.2.5-.5.5H4.9a1 1 0 0 1-.9-1V13c0-.4.3-.8.6-1l1.2-.4.2-.3a.2.2 0 0 0-.2-.2H4.5a.5.5 0 0 1-.5-.5c0-.3.2-.5.5-.5h1.6c.5 0 .9.4.9 1v.1c0 .4-.3.8-.6 1l-1.2.4-.2.3ZM7 17v2c0 .6-.4 1-1 1H4.5a.5.5 0 0 1 0-1h1.2c.2 0 .3-.1.3-.3 0-.2-.1-.3-.3-.3H4.4a.4.4 0 1 1 0-.8h1.3c.2 0 .3-.1.3-.3 0-.2-.1-.3-.3-.3H4.5a.5.5 0 1 1 0-1H6c.6 0 1 .4 1 1Z" fill-rule="evenodd"></path></svg>
                                                </span>
                                            </span>
                                            <span role="presentation" class="tox-tbtn tox-split-button__chevron" aria-disabled="false">
                                                <svg width="10" height="10" focusable="false"><path d="M8.7 2.2c.3-.3.8-.3 1 0 .4.4.4.9 0 1.2L5.7 7.8c-.3.3-.9.3-1.2 0L.2 3.4a.8.8 0 0 1 0-1.2c.3-.3.8-.3 1.1 0L5 6l3.7-3.8Z" fill-rule="nonzero"></path></svg>
                                            </span>
                                            <span aria-hidden="true" style="display: none;" id="aria_1730645381501713124470088">
                                                To open the popup, press Shift+Enter
                                            </span>
                                        </div>
                                        <button aria-label="Decrease indent" title="Decrease indent" type="button" tabindex="-1" class="tox-tbtn tox-tbtn--disabled" aria-disabled="true" style="width: 34px;">
                                            <span class="tox-icon tox-tbtn__icon-wrap">
                                                <svg width="24" height="24" focusable="false"><path d="M7 5h12c.6 0 1 .4 1 1s-.4 1-1 1H7a1 1 0 1 1 0-2Zm5 4h7c.6 0 1 .4 1 1s-.4 1-1 1h-7a1 1 0 0 1 0-2Zm0 4h7c.6 0 1 .4 1 1s-.4 1-1 1h-7a1 1 0 0 1 0-2Zm-5 4h12a1 1 0 0 1 0 2H7a1 1 0 0 1 0-2Zm1.6-3.8a1 1 0 0 1-1.2 1.6l-3-2a1 1 0 0 1 0-1.6l3-2a1 1 0 0 1 1.2 1.6L6.8 12l1.8 1.2Z" fill-rule="evenodd"></path></svg>
                                            </span>
                                        </button>
                                        <button aria-label="Increase indent" title="Increase indent" type="button" tabindex="-1" class="tox-tbtn" aria-disabled="false" style="width: 34px;">
                                            <span class="tox-icon tox-tbtn__icon-wrap">
                                                <svg width="24" height="24" focusable="false"><path d="M7 5h12c.6 0 1 .4 1 1s-.4 1-1 1H7a1 1 0 1 1 0-2Zm5 4h7c.6 0 1 .4 1 1s-.4 1-1 1h-7a1 1 0 0 1 0-2Zm0 4h7c.6 0 1 .4 1 1s-.4 1-1 1h-7a1 1 0 0 1 0-2Zm-5 4h12a1 1 0 0 1 0 2H7a1 1 0 0 1 0-2Zm-2.6-3.8L6.2 12l-1.8-1.2a1 1 0 0 1 1.2-1.6l3 2a1 1 0 0 1 0 1.6l-3 2a1 1 0 1 1-1.2-1.6Z" fill-rule="evenodd"></path></svg>
                                            </span>
                                        </button>
                                    </div>
                                    <div title="" role="toolbar" data-alloy-tabstop="true" tabindex="-1" class="tox-toolbar__group">
                                        <button aria-label="Clear formatting" title="Clear formatting" type="button" tabindex="-1" class="tox-tbtn" aria-disabled="false" style="width: 34px;">
                                            <span class="tox-icon tox-tbtn__icon-wrap">
                                                <svg width="24" height="24" focusable="false"><path d="M13.2 6a1 1 0 0 1 0 .2l-2.6 10a1 1 0 0 1-1 .8h-.2a.8.8 0 0 1-.8-1l2.6-10H8a1 1 0 1 1 0-2h9a1 1 0 0 1 0 2h-3.8ZM5 18h7a1 1 0 0 1 0 2H5a1 1 0 0 1 0-2Zm13 1.5L16.5 18 15 19.5a.7.7 0 0 1-1-1l1.5-1.5-1.5-1.5a.7.7 0 0 1 1-1l1.5 1.5 1.5-1.5a.7.7 0 0 1 1 1L17.5 17l1.5 1.5a.7.7 0 0 1-1 1Z" fill-rule="evenodd"></path></svg>
                                            </span>
                                        </button>
                                        <button aria-label="Source code" title="Source code" type="button" tabindex="-1" class="tox-tbtn" aria-disabled="false" style="width: 34px;">
                                            <span class="tox-icon tox-tbtn__icon-wrap">
                                                <svg width="24" height="24" focusable="false"><g fill-rule="nonzero"><path d="M9.8 15.7c.3.3.3.8 0 1-.3.4-.9.4-1.2 0l-4.4-4.1a.8.8 0 0 1 0-1.2l4.4-4.2c.3-.3.9-.3 1.2 0 .3.3.3.8 0 1.1L6 12l3.8 3.7ZM14.2 15.7c-.3.3-.3.8 0 1 .4.4.9.4 1.2 0l4.4-4.1c.3-.3.3-.9 0-1.2l-4.4-4.2a.8.8 0 0 0-1.2 0c-.3.3-.3.8 0 1.1L18 12l-3.8 3.7Z"></path></g></svg>
                                            </span>
                                        </button>
                                    </div>
                                </div>
                            </div>
                            <div class="tox-anchorbar">
                            </div>
                        </div>
                        <div class="tox-sidebar-wrap">
                            <div class="tox-edit-area">
                                <iframe id="message_ifr" frameborder="0" allowtransparency="true" title="Rich Text Area" class="tox-edit-area__iframe">
                                </iframe>
                            </div>
                            <div role="presentation" class="tox-sidebar">
                            <div data-alloy-tabstop="true" tabindex="-1" class="tox-sidebar__slider tox-sidebar--sliding-closed" style="width: 0px;">
                            <div class="tox-sidebar__pane-container"></div></div></div></div></div><div aria-hidden="true" class="tox-view-wrap" style="display: none;">
                            <div class="tox-view-wrap__slot-container">
                        </div>
                    </div>
                    <div aria-hidden="true" class="tox-throbber" style="display: none;">
                    </div>
                </div>
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
//      selector: '#message',
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
//    tinyMCE.init(options);

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
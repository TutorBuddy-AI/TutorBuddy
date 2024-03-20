function closeBlock(blockClass) {
    var blocks = document.querySelectorAll(blockClass);
    blocks.forEach(function(block) {
        if (block) {
            block.style.transition = 'opacity 0.5s ease-in-out';
            block.style.opacity = '0';
            block.style.pointerEvents = 'none';
            setTimeout(() => {
                block.style.display = 'none';
            }, 500);
        }
    });
}


let subProfilesExists = false;
let subDialogsExists = false;
let subStatisticExists = false;
let subNewsletterExists = false;
let subAddNewsletterExists = false;
let subAddMessageExists = false;


function closeSubSidebar() {
    const subSidebar = document.querySelector('.sub-sidebar');
    const statistic_block = document.querySelector('.statistic-block');
    const newsletter_block = document.querySelector('.newsletter-block');
    const add_newsletter_block = document.querySelector('.add-newsletter-block');
    const newsletter_info_block = document.querySelector('.newsletter-info-block');
    const add_message_block = document.querySelector('.add-message-block');

    if (subSidebar) {
        subSidebar.remove();
    }
    if (statistic_block) {
        statistic_block.remove();
    }
    if (newsletter_block) {
        newsletter_block.remove();
    }
    if (add_newsletter_block) {
        add_newsletter_block.remove();
    }
    if (add_message_block) {
        add_message_block.remove();
    }
    subProfilesExists = false;
    subDialogsExists = false;
    subStatisticExists = false;
    subNewsletterExists = false;
    subAddNewsletterExists = false;
    subAddMessageExists = false;
}


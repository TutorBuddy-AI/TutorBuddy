async function openSubProfile(tgId) {
    const profileModelContent = document.getElementById('profileModelContent');
    if (profileModelContent) {
        profileModelContent.innerHTML = `<div class="offcanvas-body profile-offcanvas p-0">
    <div class="team-cover">
        <img src="./static/dist/images/background_chat_profile.jpg" alt="" class="img-fluid">
    </div>
    <div class="p-1 pb-4 pt-0">
        <div class="team-settings">
            <div class="row g-0">
                <div class="col">
                    <div class="btn nav-btn">
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                    </div>
                </div>
                <div class="col-auto">
                    <div class="user-chat-nav d-flex">
                        <button type="button" class="btn nav-btn favourite-btn active">
                            <i class="ri-star-fill"></i>
                        </button>

                        <div class="dropdown">
                            <a class="btn nav-btn" href="javascript:void(0);" data-bs-toggle="dropdown" aria-expanded="false">
                                <i class="ri-more-2-fill"></i>
                            </a>
                            <ul class="dropdown-menu dropdown-menu-end">
                                <li><a class="dropdown-item" href="javascript:void(0);"><i class="ri-inbox-archive-line align-bottom text-muted me-2"></i>Archive</a></li>
                                <li><a class="dropdown-item" href="javascript:void(0);"><i class="ri-mic-off-line align-bottom text-muted me-2"></i>Muted</a></li>
                                <li><a class="dropdown-item" href="javascript:void(0);"><i class="ri-delete-bin-5-line align-bottom text-muted me-2"></i>Delete</a></li>
                            </ul>
                        </div>
                    </div>

                </div>
            </div>
        </div>
        <!--end col-->
    </div>
    <div class="p-3 text-center">
        <img src="./static/dist/images/user_chat.png" alt="" class="avatar-lg img-thumbnail rounded-circle mx-auto profile-img">
        <div class="mt-3">
            <h5 class="fs-16 mb-1"><a href="javascript:void(0);" class="link-primary username"><div id="FirstNameLastName"></div></a></h5>
            <p class="text-muted" id="createdat"></p>
        </div>

        <div class="d-flex gap-2 justify-content-center">
            <button type="button" class="btn avatar-xs p-0" data-bs-toggle="tooltip" data-bs-placement="top" aria-label="Message" data-bs-original-title="Message">
                <span class="avatar-title rounded bg-light text-body">
                    <i class="ri-question-answer-line"></i>
                </span>
            </button>

            <button type="button" class="btn avatar-xs p-0" data-bs-toggle="tooltip" data-bs-placement="top" aria-label="Favourite" data-bs-original-title="Favourite">
                <span class="avatar-title rounded bg-light text-body">
                    <i class="ri-star-line"></i>
                </span>
            </button>

            <button type="button" class="btn avatar-xs p-0" data-bs-toggle="tooltip" data-bs-placement="top" aria-label="Phone" data-bs-original-title="Phone">
                <span class="avatar-title rounded bg-light text-body">
                    <i class="ri-phone-line"></i>
                </span>
            </button>

            <div class="dropdown">
                <button class="btn avatar-xs p-0" type="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <span class="avatar-title bg-light text-body rounded">
                        <i class="ri-more-fill"></i>
                    </span>
                </button>

                <ul class="dropdown-menu dropdown-menu-end">
                    <li><a class="dropdown-item" href="javascript:void(0);"><i class="ri-inbox-archive-line align-bottom text-muted me-2"></i>Archive</a></li>
                    <li><a class="dropdown-item" href="javascript:void(0);"><i class="ri-mic-off-line align-bottom text-muted me-2"></i>Muted</a></li>
                    <li><a class="dropdown-item" href="javascript:void(0);"><i class="ri-delete-bin-5-line align-bottom text-muted me-2"></i>Delete</a></li>
                </ul>
            </div>
        </div>
    </div>

    <div class="border-top border-top-dashed p-3">
        <h5 class="fs-15 mb-3">Personal Details</h5>
        <div class="mb-3">
            <p class="text-muted text-uppercase fw-medium fs-12 mb-1">User name</p>
            <h6><div id="userName"></div></h6>
        </div>
        <div class="mb-3">
            <p class="text-muted text-uppercase fw-medium fs-12 mb-1">Native Language</p>
            <h6><div id="nativelang"></div></h6>
        </div>
        <div>
            <p class="text-muted text-uppercase fw-medium fs-12 mb-1">Teach Language</p>
            <h6><div id="teachlang"></div></h6>
        </div>
        <div>
            <p class="text-muted text-uppercase fw-medium fs-12 mb-1">Topics</p>
            <h6><div id="topic"></div></h6>
        </div>
        <div>
            <p class="text-muted text-uppercase fw-medium fs-12 mb-1">Goal</p>
            <h6><div id="goal"></div></h6>
        </div>
        <div>
            <p class="text-muted text-uppercase fw-medium fs-12 mb-1">English Level</p>
            <h6><div id="englishlevel"></div></h6>
        </div>
    </div>
</div>`;

 
    await new Promise(resolve => setTimeout(resolve, 0));

    try {
        const response = await fetch(`./get_info_user/${tgId}`);
        const data = await response.json();

        const firstName = data.tg_firstName || '';
        const lastName = data.tg_lastName || '';

        const firstNameLastNameElement = document.getElementById('FirstNameLastName');
        if (firstNameLastNameElement) {
            firstNameLastNameElement.textContent = `${firstName} ${lastName}`;
        }

        const userNameElement = document.getElementById('userName');
        if (userNameElement) {
            userNameElement.textContent = data.call_name || 'Call name not provided';
        }

        const nativelangElement = document.getElementById('nativelang');
        if (nativelangElement) {
            nativelangElement.textContent = data.native_lang || 'Native language not provided';
        }

        const teachlangElement = document.getElementById('teachlang');
        if (teachlangElement) {
            teachlangElement.textContent = data.teach_lang || 'Teach language not provided';
        }

        const createdatElement = document.getElementById('createdat');
        if (createdatElement) {
            createdatElement.innerHTML = `created at<br>${data.created_at || 'Date created not provided'}`;
        }
        

        const topicElement = document.getElementById('topic');
        if (topicElement) {
            topicElement.textContent = data.topic || 'Topics not provided';
        }

        const goalElement = document.getElementById('goal');
        if (goalElement) {
            goalElement.textContent = data.goal || 'Goal not provided';
        }

        const englishlevelElement = document.getElementById('englishlevel');
        if (englishlevelElement) {
            englishlevelElement.textContent = data.english_level || 'English level not provided';
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
} else {

}
}
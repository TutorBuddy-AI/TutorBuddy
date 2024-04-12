async function openSubProfiles() {
    closeSubSidebar();
    if (!subProfilesExists) {
        const subSidebar = document.createElement('div');
        subSidebar.className = 'sub-sidebar';

        try {
            const response = await fetch('/get_users');

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const users = await response.json();

            const titleContainer = document.createElement('div');
            titleContainer.className = 'title-container';

            const titleElement = document.createElement('h2');
            titleElement.textContent = 'Profiles';
            titleElement.style.fontWeight = 'bold';
            titleElement.style.marginLeft = '10px';

            titleContainer.appendChild(titleElement);

            const searchInput = document.createElement('input');
            searchInput.type = 'text';
            searchInput.placeholder = 'Search by tg_username';
            searchInput.addEventListener('input', () => handleSearch(users, searchInput.value));

            titleContainer.appendChild(searchInput);
            subSidebar.appendChild(titleContainer);

            const userListContainer = document.createElement('div');
            userListContainer.className = 'user-list-container';

            users.forEach(user => {
                const userBlock = document.createElement('div');
                userBlock.className = 'user-block';

                const avatarElement = document.createElement('img');
                avatarElement.src = 'static/img/user_photo.webp';
                avatarElement.alt = 'Avatar';
                avatarElement.className = 'avatar';
                userBlock.appendChild(avatarElement);

                const userInfo = document.createElement('div');
                userInfo.className = 'user-info';

                const nameElement = document.createElement('p');
                nameElement.textContent = `${user.tg_firstName} ${user.tg_lastName}`;
                userInfo.appendChild(nameElement);

                userBlock.appendChild(userInfo);
                userListContainer.appendChild(userBlock);

                userBlock.addEventListener('click', async () => {
                    try {
                        const tg_id = user.tg_id;
                        const user_data_Response = await fetch(`/get_info_user/${tg_id}`);

                        if (!user_data_Response.ok) {
                            throw new Error(`HTTP error! Status: ${user_data_Response.status}`);
                        }

                        const user_data = await user_data_Response.json();
                        displayProfiles(user_data);
                    } catch (error) {
                        console.error('Error fetching user profile:', error);
                    }
                });
            });

            subSidebar.appendChild(userListContainer);
            document.body.appendChild(subSidebar);
            subProfilesExists = true;
            closeBlock('.dialog-block');
            closeBlock('.profile-block');
            closeBlock('.statistic-block');
            closeBlock('.newsletter-info-block');
            closeBlock('.add-message-block');
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
}
// --------------------------------------------------------------------------------------
function handleSearch(users, searchTerm) {
    const filteredUsers = users.filter(user => user.tg_username.includes(searchTerm));

    const userListContainer = document.querySelector('.user-list-container');
    userListContainer.innerHTML = '';

    filteredUsers.forEach(user => {
        const userBlock = document.createElement('div');
        userBlock.className = 'user-block';

        const avatarElement = document.createElement('img');
        avatarElement.src = 'static/img/user_photo.webp';
        avatarElement.alt = 'Avatar';
        avatarElement.className = 'avatar';
        userBlock.appendChild(avatarElement);

        const userInfo = document.createElement('div');
        userInfo.className = 'user-info';

        const nameElement = document.createElement('p');
        nameElement.textContent = `${user.tg_firstName} ${user.tg_lastName}`;
        userInfo.appendChild(nameElement);

        userBlock.appendChild(userInfo);
        userListContainer.appendChild(userBlock);

        userBlock.addEventListener('click', async () => {
            try {
                const tg_id = user.tg_id;
                const user_data_Response = await fetch(`/get_info_user/${tg_id}`);

                if (!user_data_Response.ok) {
                    throw new Error(`HTTP error! Status: ${user_data_Response.status}`);
                }

                const user_data = await user_data_Response.json();
                displayProfiles(user_data);
            } catch (error) {
//                console.error('Error fetching user profile:', error);
            }
        });
    });
}


async function displayProfiles(user) {
    const profileBlock = document.createElement('div');
    profileBlock.className = 'profile-block';

    const mainInfoSection = createSection('Main Information', 'main-info');
    const goalSection = createSection('Goal and Theme', 'goal-section');
    const englishInfoSection = createSection('English Information', 'english-info-section');
    const createdAtSection = createSection('Account Creation Time', 'created-at-section');

    populateSection(mainInfoSection, user, ['id', 'tg_id', 'call_name', 'speaker', 'tg_firstName', 'tg_lastName', 'tg_language', 'tg_username']);
    populateSection(goalSection, user, ['goal', 'topic', 'additional_topic']);
    populateSection(englishInfoSection, user, ['english_level', 'native_lang', 'teach_lang']);
    populateSection(createdAtSection, user, ['created_at'], true);

    profileBlock.appendChild(mainInfoSection);
    profileBlock.appendChild(createDivider());
    profileBlock.appendChild(goalSection);
    profileBlock.appendChild(createDivider());
    profileBlock.appendChild(englishInfoSection);
    profileBlock.appendChild(createDivider());
    profileBlock.appendChild(createdAtSection);

    const previousProfileBlock = document.querySelector('.profile-block');
    if (previousProfileBlock) {
        previousProfileBlock.remove();
    }

    document.body.appendChild(profileBlock);

    try {
        const tg_id = user.tg_id;
        const user_mistake_Response = await fetch(`/get_message_hint_user/${tg_id}`);

        if (!user_mistake_Response.ok) {
            throw new Error(`HTTP error! Status: ${user_mistake_Response.status}`);
        }

        const user_mistake = await user_mistake_Response.json();
        if (user_mistake.message) {
            displayMistake(user_mistake.message);
        }
    } catch (error) {
//        console.error('Error fetching user mistake:', error);
    }
}



function createDivider() {
    const divider = document.createElement('div');
    divider.className = 'divider';
    return divider;
}

function createSection(sectionName, className) {
    const section = document.createElement('div');
    section.className = 'profile-section';

    if (className) {
        section.classList.add(className);
    }

    const titleElement = document.createElement('h3');
    titleElement.textContent = sectionName;
    section.appendChild(titleElement);

    const contentContainer = document.createElement('div');
    contentContainer.className = 'content-container';
    section.appendChild(contentContainer);

    return section;
}


function populateSection(section, user, fields, hideLabel = false) {
    const contentContainer = section.querySelector('.content-container');

    fields.forEach(fieldName => {
        if (fieldName === 'additional_topic' && !user[fieldName]) {
            return;
        }

        const value = user[fieldName];

        if (value === undefined) {
            return;
        }

        const keyElement = document.createElement('p');
        const valueElement = document.createElement('p');

        if (!hideLabel) {
            const boldKey = document.createElement('strong');
            boldKey.textContent = `${fieldName.replace(/_/g, ' ')}: `;
            keyElement.appendChild(boldKey);
            contentContainer.appendChild(keyElement);
        }

        contentContainer.appendChild(document.createTextNode(' '));

        const italicValue = document.createElement('em');
        italicValue.textContent = value;
        valueElement.appendChild(italicValue);

        if (fieldName === 'english_level') {
            italicValue.textContent = convertEnglishLevel(value);
        }

        contentContainer.appendChild(valueElement);
    });
}


function displayMistake(errorMessage) {
    const mistakeBlock = document.createElement('div');
    mistakeBlock.className = 'mistakeBlock';

    const titleMistake = document.createElement('h2');
    titleMistake.textContent = 'Mistakes';
    titleMistake.style.fontWeight = 'bold';
    titleMistake.style.marginLeft = '10px';

    const errorMessageElement = document.createElement('p');
    errorMessageElement.textContent = errorMessage;

    mistakeBlock.appendChild(titleMistake);
    mistakeBlock.appendChild(errorMessageElement);

    document.body.appendChild(mistakeBlock);
}


// English level converter
function convertEnglishLevel(value) {
    const levelDict = {
        '1': 'I can use simple words and basic phrases',
        '2': 'I can only have simple conversations',
        '3': 'I can talk about various subjects',
        '4': 'I express myself fluently in any situation',
    };

    return levelDict[value] || value;
}
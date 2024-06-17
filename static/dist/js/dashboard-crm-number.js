async function fetchStatistics() {
    try {
        const baseUrl = getBaseUrl();
        const apiUrl = `${baseUrl}/get_statistic`;
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }
        const data = await response.json();
        updateStatistics(data);
    } catch (error) {
    }
}
function updateStatistics(data) {
    const counterValues = document.querySelectorAll('.counter-value');

    counterValues[0].textContent = data.count_users || 0;
    counterValues[0].setAttribute('data-target', data.count_users || 0);

    counterValues[1].textContent = 0;
    counterValues[1].setAttribute('data-target', 0);

    counterValues[2].textContent = data.count_messages || 0;
    counterValues[2].setAttribute('data-target', data.count_messages || 0);
}

fetchStatistics();
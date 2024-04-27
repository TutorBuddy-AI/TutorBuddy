async function openSubStatistic() {
    closeSubSidebar();
    if (!subStatisticExists) {
        const subSidebar = document.createElement('div');
        subSidebar.className = 'statistic-block';

        try {
            const response = await fetch('./get_statistic');

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const statistics = await response.json();

            const statisticsContainer = document.createElement('div');
            statisticsContainer.className = 'statistic-card-container';
            statisticsContainer.style.display = 'flex';

            const pieChartCanvas = document.createElement('canvas');
            pieChartCanvas.id = 'pieChart';
            pieChartCanvas.width = '450';
            pieChartCanvas.height = '450';

            // Карточка для круговой диаграммы
            const pieChartCard = document.createElement('div');
            pieChartCard.className = 'statistic-card';
            const pieChartTitle = document.createElement('h2');
            pieChartTitle.textContent = 'Statistics of Choice';
            pieChartCard.appendChild(pieChartTitle);

            const pieChartContainer = document.createElement('div');
            pieChartContainer.style.textAlign = 'center';
            pieChartContainer.style.display = 'flex';
            pieChartContainer.appendChild(pieChartCanvas);
            pieChartCard.appendChild(pieChartContainer);
            statisticsContainer.appendChild(pieChartCard);

            // Карточка для диаграммы тем
            const topicChartCard = document.createElement('div');
            topicChartCard.className = 'statistic-card';
            const topicChartTitle = document.createElement('h2');
            topicChartTitle.textContent = 'Statistics of topic';
            topicChartCard.appendChild(topicChartTitle);

            const barChartCanvas = document.createElement('canvas');
            barChartCanvas.id = 'barChart';
            barChartCanvas.width = '450';
            barChartCanvas.height = '450';
            topicChartCard.appendChild(barChartCanvas);
            statisticsContainer.appendChild(topicChartCard);

            // Карточка для общей статистики
            const generalStatisticsCard = document.createElement('div');
            generalStatisticsCard.className = 'statistic-card';
            generalStatisticsCard.innerHTML = `
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <h1>General Statistics</h1>
                    <h3>Count Users: ${statistics.count_users}</h3>
                    <h3>Count Messages: ${statistics.count_messages}</h3>
                </div>
            `;
            statisticsContainer.appendChild(generalStatisticsCard);

            subSidebar.appendChild(statisticsContainer);
            document.body.appendChild(subSidebar);

            new Chart(pieChartCanvas.getContext('2d'), {
                type: 'pie',
                data: {
                    labels: ['Choice Nastya', 'Choice Bot'],
                    datasets: [{
                        data: [statistics.count_choice_nastya, statistics.count_choice_bot],
                        backgroundColor: ['#FF6384', '#36A2EB'],
                    }],
                },
                options: {
                    responsive: false,
                    maintainAspectRatio: false,
                },
            });

            // Создаем диаграмму тем
            new Chart(document.getElementById('barChart').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: Object.keys(statistics.count_topic || {}),
                    datasets: [{
                        data: Object.values(statistics.count_topic || {}),
                        backgroundColor: '#4CAF50',
                    }],
                },
                options: {
                    responsive: false,
                    maintainAspectRatio: false,
                },
            });

            subStatisticExists = true;
            closeBlock('.dialog-block');
            closeBlock('.profile-block');
            closeBlock('.newsletter-info-block');
            closeBlock('.add-message-block');

        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
}

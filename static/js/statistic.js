async function openSubStatistic() {
    closeSubSidebar();
    if (!subStatisticExists) {
        const subSidebar = document.createElement('div');
        subSidebar.className = 'statistic-block';

        try {
            const response = await fetch('/get_statistic');

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const statistics = await response.json();

            const statisticsContainer = document.createElement('div');
            statisticsContainer.style.display = 'flex';
            statisticsContainer.style.flexDirection = 'row';
            statisticsContainer.style.alignItems = 'center';

            const pieChartContainer = document.createElement('div');
            pieChartContainer.style.textAlign = 'center';
            pieChartContainer.style.display = 'flex';

            pieChartContainer.innerHTML = `
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <h1>Count Users: ${statistics.count_users}</h1>
                    <h1>Count Messages: ${statistics.count_messages}</h1>
                </div>
            `;

            const pieChartCanvas = document.createElement('canvas');
            pieChartCanvas.id = 'pieChart';
            pieChartCanvas.width = '450';
            pieChartCanvas.height = '450';

            pieChartContainer.appendChild(pieChartCanvas);
            statisticsContainer.appendChild(pieChartContainer);

            const barChartCanvas = document.createElement('canvas');
            barChartCanvas.id = 'barChart';
            barChartCanvas.width = '450';
            barChartCanvas.height = '450';

            statisticsContainer.appendChild(barChartCanvas);

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

        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
}

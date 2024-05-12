              <div class="col-lg-6">
                <div class="card">
                  <div class="card-body">
                    <h3 class="card-title">Traffic summary</h3>
                    <div id="chart-mentions" class="chart-lg" style="min-height: 240px;">
                    </div>
                  </div>
                </div>
              </div>

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

async function drawTraffic() {
    window.ApexCharts && (new ApexCharts(document.getElementById('chart-mentions'), {
        chart: {
            type: "bar",
            fontFamily: 'inherit',
            height: 240,
            parentHeightOffset: 0,
            toolbar: {
                show: false,
            },
            animations: {
                enabled: false
            },
            stacked: true,
        },
        plotOptions: {
            bar: {
                columnWidth: '50%',
            }
        },
        dataLabels: {
            enabled: false,
        },
        fill: {
            opacity: 1,
        },
        series: [{
            name: "Web",
            data: [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 2, 12, 5, 8, 22, 6, 8, 6, 4, 1, 8, 24, 29, 51, 40, 47, 23, 26, 50, 26, 41, 22, 46, 47, 81, 46, 6]
        },{
            name: "Social",
            data: [2, 5, 4, 3, 3, 1, 4, 7, 5, 1, 2, 5, 3, 2, 6, 7, 7, 1, 5, 5, 2, 12, 4, 6, 18, 3, 5, 2, 13, 15, 20, 47, 18, 15, 11, 10, 0]
        },{
            name: "Other",
            data: [2, 9, 1, 7, 8, 3, 6, 5, 5, 4, 6, 4, 1, 9, 3, 6, 7, 5, 2, 8, 4, 9, 1, 2, 6, 7, 5, 1, 8, 3, 2, 3, 4, 9, 7, 1, 6]
        }],
        tooltip: {
            theme: 'dark'
        },
        grid: {
            padding: {
                top: -20,
                right: 0,
                left: -4,
                bottom: -4
            },
            strokeDashArray: 4,
            xaxis: {
                lines: {
                    show: true
                }
            },
        },
        xaxis: {
            labels: {
                padding: 0,
            },
            tooltip: {
                enabled: false
            },
            axisBorder: {
                show: false,
            },
            type: 'datetime',
        },
        yaxis: {
            labels: {
                padding: 4
            },
        },
        labels: [
            '2020-06-20', '2020-06-21', '2020-06-22', '2020-06-23', '2020-06-24', '2020-06-25', '2020-06-26', '2020-06-27', '2020-06-28', '2020-06-29', '2020-06-30', '2020-07-01', '2020-07-02', '2020-07-03', '2020-07-04', '2020-07-05', '2020-07-06', '2020-07-07', '2020-07-08', '2020-07-09', '2020-07-10', '2020-07-11', '2020-07-12', '2020-07-13', '2020-07-14', '2020-07-15', '2020-07-16', '2020-07-17', '2020-07-18', '2020-07-19', '2020-07-20', '2020-07-21', '2020-07-22', '2020-07-23', '2020-07-24', '2020-07-25', '2020-07-26'
        ],
        colors: [xdialer.getColor("primary"), xdialer.getColor("primary", 0.8), xdialer.getColor("green", 0.8)],
        legend: {
            show: false,
        },
    })).render();
}

async function drawActiveUsers() {
    window.ApexCharts && (new ApexCharts(document.getElementById('chart-active-users'), {
        chart: {
            type: "bar",
            fontFamily: 'inherit',
            height: 40.0,
            sparkline: {
                enabled: true
            },
            animations: {
                enabled: false
            },
        },
        plotOptions: {
            bar: {
                columnWidth: '50%',
            }
        },
        dataLabels: {
            enabled: false,
        },
        fill: {
            opacity: 1,
        },
        series: [{
            name: "Profits",
            data: [37, 35, 44, 28, 36, 24, 65, 31, 37, 39, 62, 51, 35, 41, 35, 27, 93, 53, 61, 27, 54, 43, 19, 46, 39, 62, 51, 35, 41, 67]
        }],
        tooltip: {
            theme: 'dark'
        },
        grid: {
            strokeDashArray: 4,
        },
        xaxis: {
            labels: {
                padding: 0,
            },
            tooltip: {
                enabled: false
            },
            axisBorder: {
                show: false,
            },
            type: 'datetime',
        },
        yaxis: {
            labels: {
                padding: 4
            },
        },
        labels: [
            '2020-06-20', '2020-06-21', '2020-06-22', '2020-06-23', '2020-06-24', '2020-06-25', '2020-06-26', '2020-06-27', '2020-06-28', '2020-06-29', '2020-06-30', '2020-07-01', '2020-07-02', '2020-07-03', '2020-07-04', '2020-07-05', '2020-07-06', '2020-07-07', '2020-07-08', '2020-07-09', '2020-07-10', '2020-07-11', '2020-07-12', '2020-07-13', '2020-07-14', '2020-07-15', '2020-07-16', '2020-07-17', '2020-07-18', '2020-07-19'
        ],
        colors: [xdialer.getColor("primary")],
        legend: {
            show: false,
        },
    })).render();
}

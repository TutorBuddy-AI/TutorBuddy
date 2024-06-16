document.addEventListener('DOMContentLoaded', async function() {
    try {
        const response = await fetch('https://admin.tutorbuddyai.tech/test/get_statistic');
        if (!response.ok) {
            return;
        }
        const data = await response.json();
        const topics = data.count_topic;
        
        const seriesData = Object.entries(topics).map(([topic, count]) => ({ name: topic, data: [count] }));

        var options_topic = {
            series: seriesData,
            chart: {
                type: "bar",
                height: 341,
                toolbar: {
                    show: false
                }
            },
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: "65%"
                }
            },
            stroke: {
                show: true,
                width: 5,
                colors: ["transparent"]
            },
            xaxis: {
                categories: [""],
                axisTicks: {
                    show: false,
                    borderType: "solid",
                    color: "#78909C",
                    height: 6,
                    offsetX: 0,
                    offsetY: 0
                },
                title: {
                    text: "Total Topic Value",
                    offsetX: 0,
                    offsetY: -30,
                    style: {
                        color: "#78909C",
                        fontSize: "12px",
                        fontWeight: 400
                    }
                }
            },
            yaxis: {
                labels: {
                    formatter: function(e) {
                        return e 
                    }
                },
                tickAmount: 4,
                min: 0
            },
            fill: {
                opacity: 1
            },
            legend: {
                show: true,
                position: "bottom",
                horizontalAlign: "center",
                fontWeight: 500,
                offsetX: 0,
                offsetY: -14,
                itemMargin: {
                    horizontal: 8,
                    vertical: 0
                },
                markers: {
                    width: 10,
                    height: 10
                }
            }, 
            tooltip: {
                theme: 'dark',
                style: {
                    background: '#333',
                    color: '#FFF',
                },
            },
        };

        var options_count_messages = {
            series: [{
                name: "Revenue",
                data: [20, 25, 30, 35, 40, 55, 70, 110, 150, 180, 210, 250]
            }, {
                name: "Expenses",
                data: [12, 17, 45, 42, 24, 35, 42, 75, 102, 108, 156, 199]
            }],
            chart: {
                height: 325,
                type: "area",
                toolbar: false 
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: "smooth",
                width: 2
            },
            xaxis: {
                categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            },
            yaxis: {
                labels: {
                    formatter: function(e) {
                        return "$" + e + "k"
                    }
                },
                tickAmount: 5,
                min: 0,
                max: 260
            },
            colors: ["#FF5733", "#3366FF"],
            fill: {
                opacity: .06,
                colors: ["#FF5733", "#3366FF"],
                type: "solid"
            },
            tooltip: {
                theme: 'dark',
                style: {
                    background: '#333',
                    color: '#FFF',
                },
            },
        };

        var chart_topic = new ApexCharts(document.querySelector("#all-topics-chart"), options_topic);
        // var chart_count_messages = new ApexCharts(document.querySelector("#all-messages-chart"), options_count_messages);
        chart_topic.render();
        chart_count_messages.render();
        
    } catch (error) {

    }
});

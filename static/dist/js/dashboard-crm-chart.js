document.addEventListener('DOMContentLoaded', async function() {
    try {
        const response = await fetch('./get_statistic');
        if (!response.ok) {
            return;
        }
        const data = await response.json();
        const topics = data.count_topic;
        const goals = data.count_goal;
        const dailyMessages = data.count_messages_days
        const maxCount = Math.max(data.count_messages_days.counts)
        
        const seriesTopics = Object.entries(topics).map(([topic, count]) => ({ name: topic, data: [count] }));
        const seriesGoals = Object.entries(goals).map(([goal, count]) => ({ name: goal, data: [count] }));


        var options_topic = {
            series: seriesTopics,
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
                    text: "Topic Value",
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

        var options_goals = {
            series: seriesGoals,
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
                    text: "Goal Value",
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
                name: "Messages count",
                data: dailyMessages.counts
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
                curve: "straight",
                width: 2
            },
            xaxis: {
                categories: dailyMessages.days
            },
            yaxis: {
                tickAmount: 5,
                min: 0,
                max: maxCount * 1.2
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
        var chart_count_messages = new ApexCharts(document.querySelector("#all-messages-chart"), options_count_messages);
        var chart_goals = new ApexCharts(document.querySelector("#all-goals-chart"), options_goals);
        chart_topic.render();
        chart_goals.render();
        chart_count_messages.render();
        
    } catch (error) {

    }
});

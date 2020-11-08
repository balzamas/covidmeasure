      function drawLineChart(avg, avg_peak, deaths_all, deaths_covid, deaths_all_peak, country, code, avg_desc, avg_peak_desc)
      {
        week_avg = parseFloat(avg) * 7
        week_avg_peak = parseFloat(avg_peak) * 7

        var dataset_cases = new Array()
        var dataset_positivity = new Array()
        var dataset_deaths = new Array()
        var label_array = new Array()

        var dataset_data_cases = new Array()
        var dataset_data_deaths = new Array()
        var dataset_data_positivity = new Array()

        var dataset_data_total = new Array()
        var dataset_data_peakyear = new Array()
        var dataset_data_avg = new Array()
        var dataset_data_peak = new Array()

        for (const property in deaths_covid) {

                label_array.push("Week " + property)

                dataset_data_deaths.push(deaths_covid[property]);
                dataset_data_total.push(deaths_all[property]);
                dataset_data_peakyear.push(deaths_all_peak[property]);
                dataset_data_avg.push(week_avg);
                dataset_data_peak.push(week_avg_peak);
        }


        color = '#ff6600'
        dataset_deaths.push({"label": "Covid 2020", fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, data: dataset_data_deaths})

            color = '#0000ff'
            dataset_deaths.push({"label": "2020", fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, data: dataset_data_total})
            color = '#00ffff'
            dataset_deaths.push({"label": "2015", fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, data: dataset_data_peakyear})
            color = '#00ff00'
            dataset_deaths.push({"label": avg_desc, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, data: dataset_data_avg})
            color = '#ff0000'
            dataset_deaths.push({"label": avg_peak_desc, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, data: dataset_data_peak})

            config_death = {
                type: 'line',
                    elements: {
                        point:{
                            radius: 0
                        }
                    },
                data: {
                    labels: label_array,
                    datasets: dataset_deaths
                },
                options: {
                    legend:{display: true,labels:{fontSize:20}},
                    responsive: true,
                    title: {
                        display: true,
                        text: country +' // Deaths per week',
                        fontSize: 25

                    },
                    tooltips: {
                        mode: 'index',
                        intersect: false,
                    },
                    hover: {
                        mode: 'nearest',
                        intersect: true
                    },
                    scales: {
                        x: {
                            display: true,
                            scaleLabel: {
                                display: true,
                                labelString: 'Day'
                            }
                        },
                        y: {
                            display: true,
                            scaleLabel: {
                                display: true,
                                labelString: country + ' // Covid deaths per week'
                            }
                        }
                    },
               //     annotation: {
				//	 annotations: annotations
				//}

                 }
            }

   			    var ctx = document.getElementById(code + 'deathChart').getContext('2d');
			    window.myLineDeath = new Chart(ctx, config_death);



      }

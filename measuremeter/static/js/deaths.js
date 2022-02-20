      function drawLineChart(avg_peak, avg_15_19, deaths_all, deaths_covid20, deaths_all_peak, avg_and_covid, country, code, avg_desc, avg_peak_desc, peak_year)
      {
        week_avg_peak = Math.round(parseFloat(avg_peak.replace(",", ".")) * 7)

        var dataset_deaths = new Array()
        var label_array = new Array()

        var dataset_data_cases = new Array()
        var dataset_data_deaths20 = new Array()
        var dataset_data_positivity = new Array()

        var dataset_data_total = new Array()
        var dataset_data_peakyear = new Array()
        var dataset_data_avg_15_19 = new Array()
        var dataset_data_peak = new Array()
        var dataset_data_avg_and_covid = new Array()

        for (const property in deaths_covid20) {

                console.log(property)

                if (property > 105)
                {
                    property22 = property-105
                    label_array.push("Week " + property22 + "/22")
                }
                else if (property > 53)
                {
                    property21 = property-53
                    label_array.push("Week " + property21 + "/21")
                }
                else
                {
                     label_array.push("Week " + property + "/20")
                }


                dataset_data_deaths20.push(deaths_covid20[property]);
                dataset_data_avg_and_covid.push(avg_and_covid[property]);
                dataset_data_total.push(deaths_all[property]);
                dataset_data_peakyear.push(deaths_all_peak[property]);
                dataset_data_avg_15_19.push(avg_15_19[property]);
                dataset_data_peak.push(week_avg_peak);
        }


        color = '#ff6600'
        dataset_deaths.push({"label": "Covid", lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, data: dataset_data_deaths20})


            color = '#0000ff'
            dataset_deaths.push({"label": "2020/21", lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, data: dataset_data_total})
            color = '#00ffff'
            dataset_deaths.push({"label": peak_year, lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, data: dataset_data_peakyear})
            color = '#00ff00'
            dataset_deaths.push({"label": "AVG 15-19", lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, data: dataset_data_avg_15_19})
            color = '#ff0000'
            dataset_deaths.push({"label": avg_peak_desc, lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, data: dataset_data_peak})
            color = '#faec93'
            dataset_deaths.push({"label": avg_desc + " + Covid", borderDash: [10,5], lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, data: dataset_data_avg_and_covid})

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
                    maintainAspectRatio: false,
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

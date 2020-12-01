      function drawLineChart(deaths, deaths_avg, canton, code)
      {
        var dataset_deaths = new Array()
        var label_array = new Array()

        var dataset_data_deaths = new Array()
        var dataset_data_deaths_avg = new Array()


        console.log(deaths)
        console.log(deaths_avg)
        console.log("..................")

        obj_deaths = deaths.split("[")[1].split("]")[0]
        obj_deaths_avg = deaths_avg.split("[")[1].split("]")[0]


        for (const property in obj_deaths.split(",")) {

                label_array.push("Woche " + (parseInt(property) + 1))

                dataset_data_deaths.push(obj_deaths.split(",")[property]);
                dataset_data_deaths_avg.push(parseFloat(obj_deaths_avg.split(",")[property].replace('Decimal(&#x27;','').replace('&#x27;','')));
        }

        console.log(dataset_data_deaths)
        console.log(dataset_data_deaths_avg)


        color = '#ff6600'
        dataset_deaths.push({"label": "2020", lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, data: dataset_data_deaths})
        color = '#0000ff'
        dataset_deaths.push({"label": "Durchschnitt 15-19", lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, data: dataset_data_deaths_avg})

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
                        text: canton +' // Todesfälle pro Woche',
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
                                labelString: canton + ' // Todesfälle pro Woche'
                            }
                        },
                        yAxes: [{
                           ticks: {
                            beginAtZero: true
                            }
                        }]
                    },
               //     annotation: {
				//	 annotations: annotations
				//}

                 }
            }

   			    var ctx = document.getElementById(code + 'deathChart').getContext('2d');
			    window.myLineDeath = new Chart(ctx, config_death);



      }

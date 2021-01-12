      function drawLineChart(deaths, deaths_avg, deaths15, deaths19, canton, code)
      {
        var dataset_deaths = new Array()
        var label_array = new Array()

        var dataset_data_deaths = new Array()
        var dataset_data_deaths_temp = new Array()
        var dataset_data_deaths_avg = new Array()
        var dataset_data_deaths15 = new Array()
        var dataset_data_deaths19 = new Array()

        obj_deaths = deaths.split("[")[1].split("]")[0]
        obj_deaths_avg = deaths_avg.split("[")[1].split("]")[0]
        obj_deaths15 = deaths15.split("[")[1].split("]")[0]
        obj_deaths19 = deaths19.split("[")[1].split("]")[0]


        temp_start =  obj_deaths.split(",").length - 2
        for (const property in obj_deaths.split(",")) {

                label_array.push("Woche " + (parseInt(property) + 1))

                if ((parseInt(property) + 1) > temp_start)
                {
                    dataset_data_deaths.push(null);
                    dataset_data_deaths_temp.push(obj_deaths.split(",")[property])
                }
                else if ((parseInt(property) + 1) == temp_start)
                {
                    dataset_data_deaths.push(obj_deaths.split(",")[property]);
                    dataset_data_deaths_temp.push(obj_deaths.split(",")[property])
                }
                else
                {
                    dataset_data_deaths.push(obj_deaths.split(",")[property]);
                    dataset_data_deaths_temp.push(null)
                }
                dataset_data_deaths_avg.push(parseFloat(obj_deaths_avg.split(",")[property].replace('Decimal(&#x27;','').replace('&#x27;','')));
                dataset_data_deaths15.push(obj_deaths15.split(",")[property]);
                dataset_data_deaths19.push(obj_deaths19.split(",")[property]);
        }


        color = '#ff6600'
        dataset_deaths.push({"label": "2020", lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, data: dataset_data_deaths})
        dataset_deaths.push({"label": "2020", borderDash: [3,3],lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, data: dataset_data_deaths_temp})
        color = '#0000ff'
        dataset_deaths.push({"label": "Ø 15-19", lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, data: dataset_data_deaths_avg})
        color = '#faec93'
        dataset_deaths.push({"label": "2019", borderDash: [10,5], lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, data: dataset_data_deaths19})
        color = '#93fa9c'
        dataset_deaths.push({"label": "2015", borderDash: [10,5], lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, data: dataset_data_deaths15})

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

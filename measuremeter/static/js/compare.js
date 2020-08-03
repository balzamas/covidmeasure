		var timeFormat = 'MM/DD/YYYY HH:mm';


var config
var MONTHS
      $(window).on('load', function() {
       startdate = new Date(2020, 6, 24);
       enddate = new Date(2020,7,30);

       LoadData("8,25",startdate,enddate);
        	var ctx = document.getElementById('compareChart').getContext('2d');
			window.myLine = new Chart(ctx, config);
		});

      function formatDate(d)
        {
            var month = d.getMonth()+1;
            var day = d.getDate();

            var date = d.getFullYear() + '-' +
                (month<10 ? '0' : '') + month + '-' +
                (day<10 ? '0' : '') + day;
            return date;
        }

	 function LoadData(countries, startdate, endate)
      {


         lastdate_x = formatDate(endate);
         firstdate_x = formatDate(startdate);

          var data = $.ajax({
          url: "/measuremeterdata/casesdeaths/?country="+countries+"&date_after=2020-07-01&date_before="+lastdate_x,
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

        ctry_count = countries.split(',').length;
        var row = new Array()
        old_date = new Date(2020, 1, 1);

        country_pk = -1
        country_elements = new Array()
        countries_data = new Array()
        countries_groups = new Array()

        var dataset = new Array()
        var dataset_data = new Array()

        console.log(jsonData)

        $.each(jsonData, function(id, line) {
           console.log(line['date'])
           if (country_pk != line["country"]["pk"])
           {
              console.log("change")
              dataset.push({"label": line['country']['name'], data: dataset_data})
              console.log("changed")
              country_pk = line["country"]["pk"]
           }
            dataset_data.push({"x": line['date'], "y": line['cases_per_mio_seven'] })
        });

        console.log("generated")
        		config2 = {
			type: 'line',
			data: {
				labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
				datasets: dataset
			},
			options: {
				responsive: true,
				title: {
					display: true,
					text: 'Chart.js Line Chart'
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
							labelString: 'Month'
						}
					},
					y: {
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Value'
						}
					}
				}
			}
		};

        console.log (config2)

        MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
		var config = {
			type: 'line',
			data: {
				datasets: [{
					label: 'Dataset with string point data',
					backgroundColor: '#FF0000',
					borderColor: '#FF0000',
					fill: false,
					data: [{
						x: '2020-07-01',
						y: 45
					}, {
						x: '2020-07-02',
						y: 67
					}, {
						x: '2020-07-03',
						y: 88
					}, {
						x: '2020-07-04',
						y: 45
					}],
				}, {
					label: 'Dataset with date object point data',
					backgroundColor: '#FF0000',
					borderColor: '#FF0000',
					fill: false,
					data: [{
						x: '2020-07-01',
						y: 36
					}, {
						x: '2020-07-02',
						y: 54
					}, {
						x: '2020-07-03',
						y: 44
					}, {
						x: '2020-07-04',
						y: 60
					}]
				}]
			},
			options: {
				responsive: true,
				title: {
					display: true,
					text: 'Chart.js Time Point Data'
				},
				scales: {
					x: {
						type: 'time',
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Date'
						},
						ticks: {
							major: {
								enabled: true
							},
							font: function(context) {
								if (context.tick && context.tick.major) {
									return {
										style: 'bold',
										color: '#FF0000'
									};
								}

							}
						}
					},
					y: {
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'value'
						}
					}
				}
			}
		};
		console.log("coonfig")
		console.log(config)
      };


		var config;
		var config_death;
		var config_positivity;
		var config_tendency;

let Colors = ["#0000ff",
"#00ffff",
"#ff0000",
"#ffff00",
"#000000",
"#a9a9a9",
"#8b0000",
"#e9967a",
"#9400d3",
"#bdb76b",
"#556b2f",
"#ff00ff",
"#ffd700",
"#4b0082",
"#f0e68c",
"#add8e6",
"#e0ffff",
"#90ee90",
"#d3d3d3",
"#ffb6c1",
"#ffffe0",
"#00ff00",
"#ff00ff",
"#800000",
"#000080",
"#808000",
"#ffc0cb",
"#f0ffff",
"#800080",
"#c0c0c0",
"#00008b",
"#008b8b",
"#006400",
"#ffa500",
"#ff8c00",
"#8b008b",
"#9932cc",
"#f5f5dc",
"#a52a2a",
"#008000",

];

moment.updateLocale('en', {
  week: {
    dow : 1, // Monday is the first day of the week.
  }
});


Colors.random = function() {
    var result;
    var count = 0;
    for (var prop in this.names)
        if (Math.random() < 1/++count)
           result = prop;
    return result;
};

        function addDays(date, days) {
          var result = new Date(date);
          result.setDate(result.getDate() + days);
          return result;
        }

      function formatDate(d)
        {
            var month = d.getMonth()+1;
            var day = d.getDate();

            var date = d.getFullYear() + '-' +
                (month<10 ? '0' : '') + month + '-' +
                (day<10 ? '0' : '') + day;
            return date;
        }

        function getRandom(arr, n) {
            var result = new Array(n),
                len = arr.length,
                taken = new Array(len);
            if (n > len)
                throw new RangeError("getRandom: more elements taken than available");
            while (n--) {
                var x = Math.floor(Math.random() * len);
                result[n] = arr[x in taken ? taken[x] : x];
                taken[x] = --len in taken ? taken[len] : len;
            }
            return result;
        }

          function copyToClipboard() {
          var copyText = window.location.host + "/compare/" + $('#countries_dd').dropdown('get value') + "&" + $('#measuretypes_dd').dropdown('get value');
          navigator.clipboard.writeText(copyText);
        }

    function LoadCountries()
    {
                 //-----------------------------Load countries----------------------

          var dataCountries = $.ajax({
          url: "/measuremeterdata/countries/",
          dataType: "json",
          async: false
          }).responseText;

          var jsonCountries = JSON.parse(dataCountries);

          countries = []
          countries_html=''

          $.each(jsonCountries, function(id, line) {
               countries.push({
                    name: '<font size="5em"><i class="'+line['code'] +' flag"/>'+line['name']+'</font>',
                    value: line['pk']
                  });
          });

          $('#countries_dd')
              .dropdown({
                values:countries
              })
            ;
    }

    function LoadMeasureTypes()
    {
                  //-----------------------------Load MeasureTypes----------------------

          var dataMeasuresTypes = $.ajax({
          url: "/measuremeterdata/measuretypes/",
          dataType: "json",
          async: false
          }).responseText;

          var jsonMeasuresTypes = JSON.parse(dataMeasuresTypes);

          var optionsMeasuresTypes='';
          //optionsMeasuresTypes += '<div class="form-check"><input type="checkbox" class="form-check-input" name="checkbox-all" id="checkbox-all" value="all" />';
          //optionsMeasuresTypes += '<label class="form-check-label" for="checkbox-all">All</label></div>';

          var category = -1;

          measuretypes = []

          $.each(jsonMeasuresTypes, function(id, line) {
                 measuretypes.push({
                    name: '<font size="5em">'+line['name']+'</font>',
                    value: line['pk']
                  });
          });

          $('#measuretypes_dd')
              .dropdown({
                values:measuretypes
              });

            $('#param').hide();
    }

	 function LoadData(countries, measures, real_startdate, real_enddate)
      {
        startdate = formatDate(real_startdate);
        enddate = formatDate(real_enddate);

          var data = $.ajax({
          url: "/measuremeterdata/casesdeaths/?country="+countries+"&date_after="+startdate.replace('-', '\-')+"&date_before="+enddate.replace('-', '\-'),
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

        ctry_count = countries.split(',').length;
        var row = new Array()
        old_date = new Date(2020, 1, 1);

        country_pk = -1
        turn = 0

        var dataset = new Array()
        var dataset_data = new Array()

        var dataset_death = new Array()
        var dataset_death_data = new Array()

        var dataset_positivity = new Array()
        var dataset_positivity_data = new Array()

        var dataset_death_total = new Array()
        var dataset_death_total_data = new Array()

        var dataset_tendency = new Array()
        var dataset_tendency_data = new Array()

        var label_array = new Array()

        for (var d = real_startdate; d <= real_enddate; d.setDate(d.getDate() + 1)) {
            label_array.push(formatDate(new Date(d)));
        }

        has_total_death = false;

        $.each(jsonData, function(id, line) {

           if (country_pk != line["country"]["pk"] && country_pk != -1)
           {
              color = Colors[turn];
              turn += 1
              if (turn==41)
              {
                turn = 0
              }
              dataset.push({"label": country_name, fill: false, backgroundColor: color, borderColor: color, data: dataset_data})
              dataset_death.push({"label": country_code.toUpperCase() + " Covid", fill: false, backgroundColor: color, borderColor: color, data: dataset_death_data})
              dataset_tendency.push({"label": country_code.toUpperCase(), fill: false, backgroundColor: color, borderColor: color, data: dataset_tendency_data})

              if (has_total_death)
              {
                dataset_death.push({"label": country_code.toUpperCase() + " All", fill: false, backgroundColor: color, borderColor: color, data: dataset_death_total_data})
               }
              dataset_positivity.push({"label": country_code.toUpperCase(), fill: false, backgroundColor: color, borderColor: color, data: dataset_positivity_data})

              dataset_data = new Array()
              dataset_death_data = new Array()
              dataset_death_total_data = new Array()
              dataset_positivity_data = new Array()
              dataset_tendency_data = new Array()

              has_total_death = false
           }
            country_pk = line["country"]["pk"]
            country_name = line['country']['name']
            country_code = line['country']['code']
            dataset_data.push(line['cases_past14days'])
            dataset_positivity_data.push(line['positivity'])
            dataset_tendency_data.push(line['development7to7'])
            dataset_death_data.push(line['deaths_past14days'])
            //if (line['deaths_total_per100k'] > 0)
            //{
            //    dataset_death_total_data.push(line['deaths_total_per100k'])
            //    has_total_death = true
            //}
            //}

        });

        color = Colors[turn];
        dataset.push({"label": country_name, fill: false, backgroundColor: color, borderColor: color, data: dataset_data})
        dataset_death.push({"label": country_code.toUpperCase() + " Covid", fill: false, backgroundColor: color, borderColor: color, data: dataset_death_data})
        if (has_total_death)
              {
              dataset_death.push({"label": country_code.toUpperCase() + " All", fill: false, backgroundColor: color, borderColor: color, data: dataset_death_total_data})
              }
        dataset_positivity.push({"label": country_code.toUpperCase(), fill: false, backgroundColor: color, borderColor: color, data: dataset_positivity_data})
        dataset_tendency.push({"label": country_code.toUpperCase(), fill: false, backgroundColor: color, borderColor: color, data: dataset_tendency_data})

        annotations = LoadMeasure(countries, measures, startdate, enddate)

            config = {
                type: 'line',

                data: {
                    labels: label_array,
                    datasets: dataset
                },
                options: {
                    legend:{display: true,labels:{fontSize:20}},
                    responsive: true,
                    title: {
                        display: true,
                        text: 'Incidence per 100k/past 14 days',
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
                         xAxes: [{
                         isoWeekday: true,
                         type: 'time',
                         unitStepSize: 1,
                         time: {
                           displayFormats: {
                             'week': 'MMM DD ddd'
                           },
                           unit: 'week',
                         },

                        }],
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
                                labelString: 'Cases/1 Mio Pop'
                            }
                        }
                    },
      annotation: {
        events: ["click","mouseover"],
        annotations: annotations



          }
                },

            };

            config_death = {
                type: 'line',

                data: {
                    labels: label_array,
                    datasets: dataset_death
                },
                options: {
                    legend:{display: true,labels:{fontSize:20}},
                    responsive: true,
                    title: {
                        display: true,
                        text: 'Reported Covid-Deaths per 100k/past 14 days',
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
                         xAxes: [{
                         isoWeekday: true,
                         type: 'time',
                         unitStepSize: 1,
                         time: {
                           displayFormats: {
                             'week': 'MMM DD ddd'
                           },
                           unit: 'week',
                         },

                        }],
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
                                labelString: 'Deaths/100k Pop'
                            }
                        }
                    },
                },

            };

            config_positivity = {
                type: 'line',

                data: {
                    labels: label_array,
                    datasets: dataset_positivity
                },
                options: {
                    legend:{display: true,labels:{fontSize:20}},
                    responsive: true,
                    title: {
                        display: true,
                        text: 'Positive rate (Tests), past 7 days',
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
                         xAxes: [{
                         isoWeekday: true,
                         type: 'time',
                         unitStepSize: 1,
                         time: {
                           displayFormats: {
                             'week': 'MMM DD ddd'
                           },
                           unit: 'week',
                         },

                        }],
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
                                labelString: 'Positive rate (Tests), past 7 days'
                            }
                        }
                    },
                    annotation:{
                        annotations:
                        [                        {
						type: 'line',
						mode: 'horizontal',
						scaleID: 'y-axis-0',
						value: 5,
						borderColor: 'red',
						borderWidth: 2,
						label: {
							backgroundColor: 'red',
							content: "5%",
							fontSize: 19,
							enabled: true
					    	},
						}]

					}

                },

            };

            config_tendency = {
                type: 'line',

                data: {
                    labels: label_array,
                    datasets: dataset_tendency
                },
                options: {
                    legend:{display: true,labels:{fontSize:20}},
                    responsive: true,
                    title: {
                        display: true,
                        text: 'Development past week/week before (%)',
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
                         xAxes: [{
                         isoWeekday: true,
                         type: 'time',
                         unitStepSize: 1,
                         time: {
                           displayFormats: {
                             'week': 'MMM DD ddd'
                           },
                           unit: 'week',
                         },

                        }],
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
                                labelString: 'Cases/1 Mio Pop'
                            }
                        }
                    },
                    plugins: {
                        zoom: {
                            // Container for pan options
                            pan: {
                                // Boolean to enable panning
                                enabled: true,

                                // Panning directions. Remove the appropriate direction to disable
                                // Eg. 'y' would only allow panning in the y direction
                                mode: 'y'
                            },

                            // Container for zoom options
                            zoom: {
                                // Boolean to enable zooming
                                enabled: true,

                                // Zooming directions. Remove the appropriate direction to disable
                                // Eg. 'y' would only allow zooming in the y direction
                                mode: 'y',
                            }
                        }
        },
      annotation: {
        events: ["click","mouseover"],
        annotations: annotations



          }
                },

            };

		};

		window.onload = function() {
		    $("#load_data").click(function(){
                if(window.myLine && window.myLine !== null){
                   window.myLine.destroy();
                }
                if(window.myLineDeath && window.myLineDeath !== null){
                   window.myLineDeath.destroy();
                }
                if(window.myLinePositivity && window.myLinePositivity !== null){
                   window.myLinePositivity.destroy();
                }

                if(window.myLineTendency && window.myLineTendency !== null){
                   window.myLineTendency.destroy();
                }

                var datefrom = document.getElementById("datefrom").value;
                var dateto = document.getElementById("dateto").value;

                var parts =datefrom.split('-');
                var datefrom_real = new Date(parts[0], parts[1] - 1, parts[2]);

                var parts2 =dateto.split('-');
                var dateto_real = new Date(parts2[0], parts2[1] - 1, parts2[2]);


                LoadData($('#countries_dd').dropdown('get value'),$('#measuretypes_dd').dropdown('get value'),datefrom_real,dateto_real);
    			window.myLine = new Chart(ctx, config);
    			window.myLineDeath = new Chart(ctx_death, config_death);
    			window.myLinePositivity = new Chart(ctx_positivity, config_positivity);
    			window.myLineTendency = new Chart(ctx_tendency, config_tendency);

            });

		    LoadMeasureTypes();
		    LoadCountries();

            real_enddate = new Date();
            real_startdate = addDays(real_enddate, -60)

            document.getElementById("datefrom").value = formatDate(real_startdate)
            document.getElementById("dateto").value = formatDate(real_enddate)

            if ($('#param').text().length > 0)
            {
                params = $('#param').text().split("&")



                cntries = params[0].split(",")
                msures = params[1].split(",")

                $('#countries_dd').dropdown('set selected', cntries)
                $('#measuretypes_dd').dropdown('set selected', msures)
                LoadData(params[0], params[1],real_startdate,real_enddate);
            }
            else
            {

                $('#countries_dd').dropdown('set selected', ['1','3','6','12','13','14','33','35'])
                $('#measuretypes_dd').dropdown('set selected', ['8','2','26'])
                LoadData("1,3,6,12,13,14,33,35", "8,2,26",real_startdate,real_enddate);
            }






			var ctx = document.getElementById('compareChart').getContext('2d');
			window.myLine = new Chart(ctx, config);

			var ctx_death = document.getElementById('compareChartDeaths').getContext('2d');
			window.myLineDeath = new Chart(ctx_death, config_death);

			var ctx_positivity = document.getElementById('compareChartPositivity').getContext('2d');
			window.myLinePositivity = new Chart(ctx_positivity, config_positivity);

			var ctx_tendency = document.getElementById('compareChartTendency').getContext('2d');
			window.myLineTendency = new Chart(ctx_tendency, config_tendency);

			$("#btnCopyLink").click(async function(){
                copyToClipboard();
            });
		};



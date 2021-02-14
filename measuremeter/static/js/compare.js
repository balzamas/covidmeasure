		var config;
		var config_death;
		var config_positivity;
		var config_tendency;
		var jsonData_cases;

    moment.updateLocale('en', {
      week: {
        dow : 1, // Monday is the first day of the week.
      }
    });

	function getColor(d, levels) {
	    if (levels == 2)
	    {
      		return  d > 1   ? '#FE0000' :
				d > 0   ? '#FED341' :
				d > -1   ? '#00ff80' :
						  '#dfdcdc';
	    }
	    else if (levels == 3)
	    {
      		return  d > 2   ? '#FE0000' :
		        d > 1   ? '#ff7c1b' :
				d > 0   ? '#FED341' :
				d > -1   ? '#00ff80' :
						  '#dfdcdc';
	    }
	    else if (levels == 4)
	    {
            return  d > 3   ? '#FE0000' :
                    d > 2   ? '#fa8173' :
                    d > 1   ? '#fecc2f' :
                    d > 0   ? '#fee79b' :
                    d > -1   ? '#00ff80' :
                              '#dfdcdc';
	    }

	}



    function LoadCountryMeasures(countries)
    {
        current_content='<table class="ui collapsing celled table">'
        current_content+='<tr style="height:50px"><th>All measures compared</th><th style="text-align:center;width: 100px">Max.</th>'

        var country_data = $.ajax({
          url: "/measuremeterdata/countries/?pk="+countries,
          dataType: "json",
          async: false
          }).responseText;
          var country_jsonData = JSON.parse(country_data);

           $.each(country_jsonData, function(id, line) {
             current_content += '<th style="text-align:center;width: 100px"><a href="http://www.covidlaws.net/country/'+line.code +'"><i class="'+line.code+' flag"></i><b>' + line.code + '</b></a></th>'
           });

           current_content += '</tr>'

           current_content += '<tr><td><b>Stringency Index</b></td><td></td>'
                        $.each(country_jsonData, function(id, line_cntry) {
                             current_content += '<td id=stringency_'+ line_cntry.pk +' style="text-align:center"></td>'
                        });
           current_content += '</tr>'

          var dataMeasuresTypes = $.ajax({
          url: "/measuremeterdata/oxfordmeasuretypes/",
          dataType: "json",
          async: false
          }).responseText;

          var jsonMeasuresTypes = JSON.parse(dataMeasuresTypes);
           $.each(jsonMeasuresTypes, function(id, line) {
             max = 0
             if (line.text_level4)
                max = 4
             else if (line.text_level3)
                max = 3
             else if (line.text_level2)
                max = 2
             else if (line.text_level1)
                max = 1




             current_content += '<tr><td>' + line.name + '</td><td style="text-align:center">' + max +'</td>'
                        $.each(country_jsonData, function(id, line_cntry) {
                             current_content += '<td id='+ line.pk +'_'+ line_cntry.pk +' style="text-align:center"></td>'
                        });
             current_content += '</tr>'
           });

           current_content += '</table>'

          document.getElementById('measures').innerHTML = current_content

          console.log(jsonData_cases)
        //  $.each(jsonData_cases, function(id, line) {


        //  }


            var d = new Date();
            today = formatDate(d);


          var data = $.ajax({
          url: "/measuremeterdata/measures/?country="+countries+"&start="+today.replace('-', '\-')+"&end="+today.replace('-', '\-'),
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

           $.each(jsonData, function(id, line) {
                         max = 0
                         if (line.type.text_level4)
                            max = 4
                         else if (line.type.text_level3)
                            max = 3
                         else if (line.type.text_level2)
                            max = 2
                         else if (line.type.text_level1)
                            max = 1

                        color = getColor(line.level, max)

                        value = line.level
                        if (line.isregional)
                            {
                                value += "*"
                            }

                       document.getElementById(line.type.pk +'_' +  line.country.pk).innerHTML = value
                       document.getElementById(line.type.pk +'_' +  line.country.pk).style.backgroundColor = color
                });
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
          url: "/measuremeterdata/oxfordmeasuretypes/",
          dataType: "json",
          async: false
          }).responseText;

          var jsonMeasuresTypes = JSON.parse(dataMeasuresTypes);

          var optionsMeasuresTypes='';
          //optionsMeasuresTypes += '<div class="form-check"><input type="checkbox" class="form-check-input" name="checkbox-all" id="checkbox-all" value="all" />';
          //optionsMeasuresTypes += '<label class="form-check-label" for="checkbox-all">All</label></div>';

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
          jsonData_cases = JSON.parse(data);

        ctry_count = countries.split(',').length;
        var row = new Array()
        old_date = new Date(2020, 1, 1);

        country_pk = -1
        turn = 0

        var dataset = new Array()
        var dataset_data = new Array()

        var dataset_death = new Array()
        var dataset_death_data = new Array()

        var dataset_r0 = new Array()
        var dataset_r0_data = new Array()

        var dataset_positivity = new Array()
        var dataset_positivity_data = new Array()

        var dataset_tests = new Array()
        var dataset_tests_data = new Array()

        var dataset_death_total = new Array()
        var dataset_death_total_data = new Array()

        var dataset_tendency = new Array()
        var dataset_tendency_data = new Array()

        var label_array = new Array()

        for (var d = real_startdate; d <= real_enddate; d.setDate(d.getDate() + 1)) {
            label_array.push(formatDate(new Date(d)));
        }

        has_total_death = false;
        border_width = 4

        stringency = null

        $.each(jsonData_cases, function(id, line) {

           if (country_pk != line["country"]["pk"] && country_pk != -1)
           {
              color = Colors[turn];
              turn += 1
              if (turn==41)
              {
                turn = 0
              }
              dataset.push({"label": country_name, fill: false, lineTension: 0, pointRadius: 0.1, backgroundColor: color, borderColor: color, borderWidth: border_width, data: dataset_data})
              dataset_death.push({"label": country_code.toUpperCase() + " Covid", lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, borderWidth: border_width, data: dataset_death_data})
              dataset_tendency.push({"label": country_code.toUpperCase(), lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, borderWidth: border_width, data: dataset_tendency_data})

              if (has_total_death)
              {
                dataset_death.push({"label": country_code.toUpperCase() + " All", lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, borderWidth: border_width, data: dataset_death_total_data})
               }
              dataset_positivity.push({"label": country_code.toUpperCase(), lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, borderWidth: border_width, data: dataset_positivity_data})
              dataset_tests.push({"label": country_code.toUpperCase(), lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, borderWidth: border_width, data: dataset_tests_data})
              dataset_r0.push({"label": country_code.toUpperCase(), lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, borderWidth: border_width, data: dataset_r0_data})

              dataset_data = new Array()
              dataset_death_data = new Array()
              dataset_death_total_data = new Array()
              dataset_positivity_data = new Array()
              dataset_tests_data = new Array()
              dataset_r0_data = new Array()
              dataset_tendency_data = new Array()

              console.log(stringency)
              document.getElementById('stringency_' +  country_pk).innerHTML = Number(stringency).toFixed(2)
              stringency = null

              has_total_death = false
           }


            if (line['stringency_index'])
            {
                stringency = line['stringency_index']
            }
            country_pk = line["country"]["pk"]
            country_name = line['country']['name']
            country_code = line['country']['code']
            dataset_data.push(line['cases_past7days'])
            dataset_positivity_data.push(line['positivity'])
            dataset_tests_data.push(line['tests_smoothed_per_thousand'])
            dataset_r0_data.push(line['r0median'])
            dataset_tendency_data.push(line['development7to7'])
            dataset_death_data.push(line['deaths_past7days'])
            //if (line['deaths_total_per100k'] > 0)
            //{
            //    dataset_death_total_data.push(line['deaths_total_per100k'])
            //    has_total_death = true
            //}
            //}

        });

        color = Colors[turn];
        dataset.push({"label": country_name, lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, borderWidth: border_width, data: dataset_data})
        dataset_death.push({"label": country_code.toUpperCase() + " Covid", lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, borderWidth: border_width, data: dataset_death_data})
        if (has_total_death)
              {
              dataset_death.push({"label": country_code.toUpperCase() + " All", lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, borderWidth: border_width, data: dataset_death_total_data})
              }
        dataset_positivity.push({"label": country_code.toUpperCase(), lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, borderWidth: border_width, data: dataset_positivity_data})
        dataset_tests.push({"label": country_code.toUpperCase(), lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, borderWidth: border_width, data: dataset_tests_data})
        dataset_r0.push({"label": country_code.toUpperCase(), lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, borderWidth: border_width, data: dataset_r0_data})
        dataset_tendency.push({"label": country_code.toUpperCase(), lineTension: 0, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, borderWidth: border_width, data: dataset_tendency_data})
        document.getElementById('stringency_' +  country_pk).innerHTML = Number(stringency).toFixed(2)

        annotations = LoadMeasure(countries, measures, startdate, enddate)
        annotations_zero = $.extend( true, [], annotations );
        annotations_one = $.extend( true, [], annotations );

        annotations_zero.unshift({
						type: 'line',
						mode: 'horizontal',
						scaleID: 'y-axis-0',
						value: 0,
						borderColor: 'green',
						borderWidth: 2,
						})

        annotations_one.unshift({
						type: 'line',
						mode: 'horizontal',
						scaleID: 'y-axis-0',
						value: 1,
						borderColor: 'green',
						borderWidth: 2,
						})


            config = {
                type: 'line',

                data: {
                    labels: label_array,
                    datasets: dataset
                },
                options: {
                    elements: {
                        point:{
                            radius: 0
                        }
                    },
                    legend:{display: true,labels:{fontSize:20}},
                    responsive: true,
                    maintainAspectRatio: false,

                    title: {
                        display: true,
                        text: 'Incidence per 100k/past 7 days',
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
                        },
                        yAxes: [{
                           ticks: {
                            beginAtZero: true
                            }
                        }]
                    },
      annotation: {
        events: ["click","mouseover"],
        annotations: annotations



          }
                },

            };

            config_death = {
                type: 'line',
                    elements: {
                        point:{
                            radius: 0
                        }
                    },
                data: {
                    labels: label_array,
                    datasets: dataset_death
                },
                options: {
                    legend:{display: true,labels:{fontSize:20}},
                    responsive: true,
                    maintainAspectRatio: false,
                    title: {
                        display: true,
                        text: 'Reported Covid-Deaths per 100k/past 7 days',
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
                        },
                        yAxes: [{
                           ticks: {
                            beginAtZero: true
                            }
                        }]
                    },
                },

            };

            config_r0 = {
                type: 'line',
                    elements: {
                        point:{
                            radius: 0
                        }
                    },
                data: {
                    labels: label_array,
                    datasets: dataset_r0
                },
                options: {
                    legend:{display: true,labels:{fontSize:20}},
                    responsive: true,
                    maintainAspectRatio: false,

                    title: {
                        display: true,
                        text: 'Re -  Effective reproductive number (mean)',
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
                                labelString: 'Re -  Effective reproductive number (mean)'
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
        annotations: annotations_one



          }
                },

            };


            config_positivity = {
                type: 'line',
                    elements: {
                        point:{
                            radius: 0
                        }
                    },
                data: {
                    labels: label_array,
                    datasets: dataset_positivity
                },
                options: {
                    legend:{display: true,labels:{fontSize:20}},
                    responsive: true,
                    maintainAspectRatio: false,
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
                        },
                        yAxes: [{
                           ticks: {
                            beginAtZero: true
                            }
                        }]
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

            config_tests = {
                type: 'line',
                    elements: {
                        point:{
                            radius: 0
                        }
                    },
                data: {
                    labels: label_array,
                    datasets: dataset_tests
                },
                options: {
                    legend:{display: true,labels:{fontSize:20}},
                    responsive: true,
                    maintainAspectRatio: false,
                    title: {
                        display: true,
                        text: 'Tests per 1000 population (Smoothed)',
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
                                labelString: 'Tests per 1000 population (Smoothed)'
                            }
                        },
                        yAxes: [{
                           ticks: {
                            beginAtZero: true
                            }
                        }]
                    },
                },

            };

            config_tendency = {
                type: 'line',
                    elements: {
                        point:{
                            radius: 0
                        }
                    },
                data: {
                    labels: label_array,
                    datasets: dataset_tendency
                },
                options: {
                    legend:{display: true,labels:{fontSize:20}},
                    responsive: true,
                    maintainAspectRatio: false,
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
                        },
                        yAxes: [{
                           ticks: {
                            max: 100,
                            min: -50
                            }
                        }]
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
        annotations: annotations_zero



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

                if(window.myLineTests && window.myLineTests !== null){
                   window.myLineTests.destroy();
                }



                if(window.myLineR0 && window.myLineR0 !== null){
                   window.myLineR0.destroy();
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


                LoadCountryMeasures($('#countries_dd').dropdown('get value'))
                LoadData($('#countries_dd').dropdown('get value'),$('#measuretypes_dd').dropdown('get value'),datefrom_real,dateto_real);
    			window.myLine = new Chart(ctx, config);
    			window.myLineDeath = new Chart(ctx_death, config_death);
    			window.myLinePositivity = new Chart(ctx_positivity, config_positivity);
    			window.myLineTests = new Chart(ctx_tests, config_tests);
    			window.myLineR0 = new Chart(ctx_r0, config_r0);
    			window.myLineTendency = new Chart(ctx_tendency, config_tendency);

            });

            $("#save_incidence").click(function(){
                            save_image("compareChart")
            });

            $("#save_tendency").click(function(){
                            save_image("compareChartTendency")
            });

            $("#save_death").click(function(){
                            save_image("compareChartDeaths")
            });

            $("#save_positivity").click(function(){
                            save_image("compareChartPositivity")
            });

            $("#save_tests").click(function(){
                            save_image("compareChartTests")
            });

            $("#save_r0").click(function(){
                            save_image("compareChartR0")
            });

		    LoadMeasureTypes();
		    LoadCountries();

            if ($('#param').text().length > 0)
            {
                params = $('#param').text().split("&")

                cntries = params[0].split(",")
                msures = params[1].split(",")
                datefrom = new Date(params[2])
                dateto = new Date(params[3])

                document.getElementById("datefrom").value = formatDate(datefrom)
                document.getElementById("dateto").value = formatDate(dateto)

                $('#countries_dd').dropdown('set selected', cntries)
                $('#measuretypes_dd').dropdown('set selected', msures)
                LoadCountryMeasures(params[0])
                LoadData(params[0], params[1],datefrom,dateto);

            }
            else
            {
                real_enddate = new Date();
                real_startdate = addDays(real_enddate, -60)

                document.getElementById("datefrom").value = formatDate(real_startdate)
                document.getElementById("dateto").value = formatDate(real_enddate)

                $('#countries_dd').dropdown('set selected', ['1','6','13','14','33','34','35'])
                $('#measuretypes_dd').dropdown('set selected', ['1','5','2'])
                LoadCountryMeasures($('#countries_dd').dropdown('get value'))
                LoadData("1,6,13,14,33,34,35", "1,5,2",real_startdate,real_enddate);

            }

            Chart.plugins.register({
                afterRender: function(c) {
                    var ctx = c.chart.ctx;
                    ctx.save();
                    // This line is apparently essential to getting the
                    // fill to go behind the drawn graph, not on top of it.
                    // Technique is taken from:
                    // https://stackoverflow.com/a/50126796/165164
                    ctx.globalCompositeOperation = 'destination-over';
                    ctx.fillStyle = 'white';
                    ctx.fillRect(0, 0, c.chart.width, c.chart.height);
                    ctx.restore();
                }
            });

			var ctx = document.getElementById('compareChart').getContext('2d');
			window.myLine = new Chart(ctx, config);

			var ctx_death = document.getElementById('compareChartDeaths').getContext('2d');
			window.myLineDeath = new Chart(ctx_death, config_death);

			var ctx_positivity = document.getElementById('compareChartPositivity').getContext('2d');
			window.myLinePositivity = new Chart(ctx_positivity, config_positivity);

			var ctx_tests = document.getElementById('compareChartTests').getContext('2d');
			window.myLineTests = new Chart(ctx_tests, config_tests);

			var ctx_r0 = document.getElementById('compareChartR0').getContext('2d');
			window.myLineR0 = new Chart(ctx_r0, config_r0);

			var ctx_tendency = document.getElementById('compareChartTendency').getContext('2d');
			window.myLineTendency = new Chart(ctx_tendency, config_tendency);

			$("#btnCopyLink").click(async function(){
                copyToClipboard("/compare/" + $('#countries_dd').dropdown('get value') + "&" + $('#measuretypes_dd').dropdown('get value')+ "&" + document.getElementById("datefrom").value + "&" + document.getElementById("dateto").value);
            });
		};



		var timeFormat = 'MM/DD/YYYY HH:mm';
		var config;

	randomScalingFactor = function() {
		return Math.floor(Math.random() * 10);
	};

		function newDate(days) {
			return moment().add(days, 'd').toDate();
		}

		function newDateString(days) {
			return moment().add(days, 'd').format();
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

            if ($('#param').text().length > 0)
            {
//                var datesft = drawTimeline(mode, $('#param').text(), $('#measuretypes_dd').dropdown('get value'));
//                console.log(datesft)
//                drawChartCasesTimeline($('#param').text(),datesft[0], datesft[1])

            }
            else
            {
                rnd_country = Math.floor(Math.random() * 43) + 1;
                rnd_country2 = Math.floor(Math.random() * 43) + 1;
                rnd_country3 = Math.floor(Math.random() * 43) + 1;

                countries=rnd_country.toString()+","+rnd_country2.toString()+","+rnd_country3.toString();

               measure_list = [1,26,8,11,16,2,21,28];
               measure_list_filtered = getRandom(measure_list,5);

               measuretypes=measure_list_filtered[0].toString()+","+measure_list_filtered[1].toString()+","+measure_list_filtered[2].toString()+","+measure_list_filtered[3].toString()+","+measure_list_filtered[4].toString();

//                var datesft = drawTimeline(mode, countries, measuretypes);
//                 console.log(datesft)
//                drawLineChartperPop(countries, datesft[0], datesft[1]);
            }
    }

	 function LoadData(countries, startdate, endate)
      {
          var data = $.ajax({
          url: "/measuremeterdata/casesdeaths/?country="+countries+"&date_after="+startdate.replace('-', '\-')+"&date_before="+endate.replace('-', '\-'),
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

        ctry_count = countries.split(',').length;
        var row = new Array()
        old_date = new Date(2020, 1, 1);

        country_pk = -1

        var dataset = new Array()
        var dataset_data = new Array()
        var label_array = new Array()

        date_isfilled = false

        $.each(jsonData, function(id, line) {

           if (country_pk != line["country"]["pk"] && country_pk != -1)
           {
              color = '#'+(Math.random()*0xFFFFFF<<0).toString(16)
              dataset.push({"label": country_name, fill: false, backgroundColor: color, borderColor: color, data: dataset_data})
              dataset_data = new Array()
              date_isfilled = true;
           }
            country_pk = line["country"]["pk"]
            country_name = line['country']['name']
            dataset_data.push(line['cases_per_mio_seven'])
            if (!date_isfilled)
            {
                label_array.push(line['date'])
            }
        });

        color = '#'+(Math.random()*0xFFFFFF<<0).toString(16)
        dataset.push({"label": country_name, fill: false, backgroundColor: color, borderColor: color, data: dataset_data})

            config = {
                type: 'line',
                data: {
                    labels: label_array,
                    datasets: dataset
                },
                options: {
                    responsive: true,
                    title: {
                        display: true,
                        text: 'Cases/1 Mio Pop'
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
                                labelString: 'Cases/1 Mio Pop'
                            }
                        }
                    },
      annotation: {
        events: ["click","mouseover"],
        annotations: [
          {
            drawTime: "afterDatasetsDraw",
            id: "hline",
            type: "line",
            mode: "vertical",
            scaleID: "x-axis-0",
            value: '2020-04-15',
            borderColor: "black",
            borderWidth: 5,
            label: {
              backgroundColor: "red",
              content: '<i class=ch flag/>',
              rotation: 90,
              enabled: true
            },
            onClick: function(e) {
              // The annotation is is bound to the `this` variable
              console.log("Annotation", e.type, this);

            },
            onMouseover: function(e) {
              // The annotation is is bound to the `this` variable
              console.log("Annotation", e.type, this);
            }
           },
          ]
          }
                },
                plugins: {
                    annotation: {
                        // Defines when the annotations are drawn.
                        // This allows positioning of the annotation relative to the other
                        // elements of the graph.
                        //
                        // Should be one of: afterDraw, afterDatasetsDraw, beforeDatasetsDraw
                        // See http://www.chartjs.org/docs/#advanced-usage-creating-plugins
                        drawTime: 'afterDatasetsDraw', // (default)

                        // Mouse events to enable on each annotation.
                        // Should be an array of one or more browser-supported mouse events
                        // See https://developer.mozilla.org/en-US/docs/Web/Events
                        events: ['click, mouseover'],

                        // Double-click speed in ms used to distinguish single-clicks from
                        // double-clicks whenever you need to capture both. When listening for
                        // both click and dblclick, click events will be delayed by this
                        // amount.
                        dblClickSpeed: 350, // ms (default)

                        // Array of annotation configuration objects
                        // See below for detailed descriptions of the annotation options
                        annotations: [{
                            drawTime: 'afterDraw', // overrides annotation.drawTime if set
                            id: 'a-line-1', // optional
                            type: 'line',
                            mode: 'horizontal',
                            scaleID: 'y-axis-0',
                            value: '1',
                            borderColor: 'red',
                            borderWidth: 2,

                            // Fires when the user clicks this annotation on the chart
                            // (be sure to enable the event in the events array below).
                            onClick: function(e) {
                                // `this` is bound to the annotation element
                            },
                            onMouseover: function(e) {
                                // `this` is bound to the annotation element
                            },                        }]
                    }
                }
            };

		};

		window.onload = function() {
		    $("#load_data").click(function(){
                console.log("Klicki")
                window.myLine.destroy();
                var datefrom = document.getElementById("datefrom").value;
                var dateto = document.getElementById("dateto").value;

                LoadData($('#countries_dd').dropdown('get value'),datefrom,dateto);
    			window.myLine = new Chart(ctx, config);
            });

		    LoadMeasureTypes();
		    LoadCountries();
		    startdate = "2020-04-01";
            enddate = "2020-05-01";

            LoadData("8,25,36",startdate,enddate);
			var ctx = document.getElementById('compareChart').getContext('2d');
			window.myLine = new Chart(ctx, config);
		};



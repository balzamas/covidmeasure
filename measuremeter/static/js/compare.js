
		var config;
		var config_death;

let Colors = ["#0000ff",
"#00ffff",
"#ff0000",
"#ffff00",
"#008000",
"#00ffff",
"#ffc0cb",
"#f0ffff",
"#f5f5dc",
"#000000",
"#a52a2a",
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
"#800080",
"#800080",
"#c0c0c0",
"#00008b",
"#008b8b",
"#006400",
"#ffa500",
"#ff8c00",
"#8b008b",
"#9932cc",

];

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

     function FormatPopUp(line)
     {
                            str_level = '<i class="green '+line["type"]["icon"] +'" data-tooltip="None"></i>'
                            status = "None"

                            if (line['level'] == 1)
                            {
                                status = line["type"]["tooltip_partial"]
                                str_level =  '<i class="yellow '+line["type"]["icon"] +'" data-tooltip="'+line["type"]["tooltip_partial"]+'"></i>'
                            }
                            else if (line['level'] == 2)
                            {
                                status = line["type"]["tooltip_nonpartial"]
                                str_level =  '<i class="red '+line["type"]["icon"] +'" data-tooltip="'+line["type"]["tooltip_nonpartial"]+'"></i>'
                            }

                            endtime = "Undefined"
                            if (line['end'] != null)
                            {
                                endtime = line['end'];
                            }


                            htmlLine = '<p><i class="'+line['country']['code'] +' flag"/>'+ line['country']['name'] + "  "+ str_level+ '<br>Level: '+line["type"]["name"] +'<br>Measure:'+status+'<br>End: '+endtime+"<br>"+line["comment"]+"</p>";

         return htmlLine;
     }

     function LoadMeasure(countries, measuretypes, startdate, enddate)
     {

           if (countries == undefined)
             {
               //Startup: set random country
               rnd_country = Math.floor(Math.random() * 43) + 1;
               rnd_country2 = Math.floor(Math.random() * 43) + 1;
               rnd_country3 = Math.floor(Math.random() * 43) + 1;

               countries=rnd_country.toString()+","+rnd_country2.toString()+","+rnd_country3.toString();
             }


          var data = $.ajax({
          url: "/measuremeterdata/measures/?country="+countries+"&type="+measuretypes,
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

        annotations_prepare = new Array()
        annotations = new Array()

        $.each(jsonData, function(id, line) {
            if (line['start'] != null)
            {
                doesexist = false;
                let obj = annotations_prepare.find((o, i) => {
                    if (o.value === line['start']) {
                        if (o.label.includes(line["country"]["code"]))
                        {
                           codes = annotations_prepare[i]["label"]
                        }
                        else
                        {
                           codes = annotations_prepare[i]["label"] + ", " + line["country"]["code"]
                        }

                        popUp = annotations_prepare[i]["popup"] + "<br>" + FormatPopUp(line);

                        annotations_prepare[i] = { label: codes, value: line['start'], popup: popUp };
                        doesexist = true;
                        return true; // stop searching
                    }
                });

                if (!doesexist)
                {
                    annotations_prepare.push(
                        {
                            value: line['start'],
                            label: line["country"]["code"],
                            popup: FormatPopUp(line)
                        }
                    );
                }
            }
            });

            annotations_prepare.forEach(function(element)
                {
                    annotations.push(
                        {
                            drawTime: "afterDatasetsDraw",
                            type: "line",
                            mode: "vertical",
                            scaleID: "x-axis-0",
                            value: element.value,
                            borderColor: "black",
                            borderWidth: 2,
                            label: {
                                backgroundColor: "#5d5d5d",
                                content: element.label,
                                rotation: 270,
                                enabled: true,
                                fontSize: 19
                            },

                        onClick: function(e) {
                        // The annotation is is bound to the `this` variable
                            $("#dialog").html('<div style="margin-left: 10;margin-top: 10;margin-right: 10;margin-bottom: 10;max-height: 800;">' + element.popup + '</div>');
                            $('#dialog').dialog({
                              title: "Introduced measures " + element.value,
                              open: function (event, ui) {
                                    $('.ui-widget-overlay').bind('click', function () {
                                    $("#dialog").dialog('close');
                                    });
                                }
                            }).dialog('open');
                        },
                        }

                    )
                }
            )

        return annotations
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

        var dataset_death_total = new Array()
        var dataset_death_total_data = new Array()

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
              if (has_total_death)
              {
                dataset_death.push({"label": country_code.toUpperCase() + " All", fill: false, backgroundColor: color, borderColor: color, data: dataset_death_total_data})
               }
              dataset_data = new Array()
              dataset_death_data = new Array()
              dataset_death_total_data = new Array()
              has_total_death = false
           }
            country_pk = line["country"]["pk"]
            country_name = line['country']['name']
            country_code = line['country']['code']
            dataset_data.push(line['cases_past14days'])
            dataset_death_data.push(line['deaths_per100k'])
            if (line['deaths_total_per100k'] > 0)
            {
                dataset_death_total_data.push(line['deaths_total_per100k'])
                has_total_death = true
            }

        });

        color = Colors[turn];
        dataset.push({"label": country_name, fill: false, backgroundColor: color, borderColor: color, data: dataset_data})
        dataset_death.push({"label": country_code.toUpperCase() + " Covid", fill: false, backgroundColor: color, borderColor: color, data: dataset_death_data})
        if (has_total_death)
              {
              dataset_death.push({"label": country_code.toUpperCase() + " All", fill: false, backgroundColor: color, borderColor: color, data: dataset_death_total_data})
              }

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
                        text: 'Deaths per 100k',
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
                                labelString: 'Deaths/100k Pop'
                            }
                        }
                    },
                },

            };

		};

		window.onload = function() {
		    $("#load_data").click(function(){
                window.myLine.destroy();
                var datefrom = document.getElementById("datefrom").value;
                var dateto = document.getElementById("dateto").value;

                var parts =datefrom.split('-');
                var datefrom_real = new Date(parts[0], parts[1] - 1, parts[2]);

                var parts2 =dateto.split('-');
                var dateto_real = new Date(parts2[0], parts2[1] - 1, parts2[2]);


                LoadData($('#countries_dd').dropdown('get value'),$('#measuretypes_dd').dropdown('get value'),datefrom_real,dateto_real);
    			window.myLine = new Chart(ctx, config);
    			window.myLine = new Chart(ctx_death, config_death);
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
                $('#countries_dd').dropdown('set selected', ['1','3','6'])
                $('#measuretypes_dd').dropdown('set selected', ['8','26'])
                LoadData("1,3,6", "8,26",real_startdate,real_enddate);
            }






			var ctx = document.getElementById('compareChart').getContext('2d');
			window.myLine = new Chart(ctx, config);

			var ctx_death = document.getElementById('compareChartDeaths').getContext('2d');
			window.myLine = new Chart(ctx_death, config_death);

			$("#btnCopyLink").click(async function(){
                copyToClipboard();
            });
		};




		var config;

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

     function FormatPopUp(line)
     {
                            str_level = 'None'
                            if (line['level'] = 1)
                            {
                                str_level =  line["type"]["tooltip_partial"]
                            }
                            else if (line['level'] = 1)
                            {
                                str_level =  line["type"]["tooltip_nonpartial"]
                            }

                            endtime = "Undefined"
                            if (line['end'] != null)
                            {
                                endtime = line['end'];
                            }

                            htmlLine = '<p><i class="'+line['country']['code'] +' flag"/>'+ line['country']['name'] + '<br>'+line["type"]["name"] + '<br>' + str_level +'<br>End: '+endtime+"<br>"+line["comment"]+"</p>";

         return htmlLine;
     }

     function LoadMeasure(countries, measuretypes, startdate, endate)
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
                                backgroundColor: "red",
                                content: element.label,
                                rotation: 90,
                                enabled: true,
                                fontSize: 20
                            },

                        onClick: function(e) {
                        // The annotation is is bound to the `this` variable
                            $("#dialog").html('<div style="margin-left: 10;margin-top: 10;margin-right: 10;margin-bottom: 10;">' + element.popup + '</div>');
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

	 function LoadData(countries, measures, startdate, endate)
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

        annotations = LoadMeasure(countries, measures, startdate, endate)

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
                        text: 'Reported new cases per day/per 1Mio inhabitants // Rolling average (last 7 days).',
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

		};

		window.onload = function() {
		    $("#load_data").click(function(){
                window.myLine.destroy();
                var datefrom = document.getElementById("datefrom").value;
                var dateto = document.getElementById("dateto").value;

                console.log($('#measuretypes_dd').dropdown('get value'))

                LoadData($('#countries_dd').dropdown('get value'),$('#measuretypes_dd').dropdown('get value'),datefrom,dateto);
    			window.myLine = new Chart(ctx, config);
            });

		    LoadMeasureTypes();
		    LoadCountries();

            real_enddate = new Date();
            real_startdate = addDays(real_enddate, -60)

            console.log(real_enddate)
            document.getElementById("datefrom").value = formatDate(real_startdate)
            document.getElementById("dateto").value = formatDate(real_enddate)

		    startdate = formatDate(real_startdate);
            enddate = formatDate(real_enddate);

            $('#countries_dd').dropdown('set selected', ['1','3','6'])
            $('#measuretypes_dd').dropdown('set selected', ['8','26'])

            LoadData("1,3,6", "8,26",startdate,enddate);
			var ctx = document.getElementById('compareChart').getContext('2d');
			window.myLine = new Chart(ctx, config);
		};



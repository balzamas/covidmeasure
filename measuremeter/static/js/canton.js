var config;
var data

    moment.updateLocale('en', {
      week: {
        dow : 1, // Monday is the first day of the week.
      }
    });

     function FormatPopUp(line, last_line)
     {
        var tendency = "&#11014;"

        if (last_line)
        {

            if (last_line['canton']['pk'] == line['canton']['pk'] && last_line['type']['pk'] == line['type']['pk'])
            {
               if (last_line['level'] > line['level'])
               {
                tendency = "&#11015;"
               }
               else if (last_line['level'] == line['level'])
               {
                tendency = "&#10145;"
               }
               else if (last_line['level'] < line['level'])
               {
                tendency = "&#11014;"
               }
               }

        }
                            str_level = '<i class="green '+line["type"]["icon"] +'" data-tooltip="None"></i>'

                            if (line['level'] == 1)
                            {
                                str_level =  '<i class="yellow '+line["type"]["icon"] +'" data-tooltip="'+line["type"]["tooltip_partial"]+'"></i>'
                            }
                            else if (line['level'] == 2)
                            {
                                str_level =  '<i class="orange '+line["type"]["icon"] +'" data-tooltip="'+line["type"]["tooltip_nonpartial"]+'"></i>'
                            }
                            else if (line['level'] == 3)
                            {
                                str_level =  '<i class="red '+line["type"]["icon"] +'" data-tooltip="'+line["type"]["tooltip_nonpartial"]+'"></i>'
                            }
                            else if (line['level'] == 4)
                            {
                                str_level =  '<i class="red '+line["type"]["icon"] +'" data-tooltip="'+line["type"]["tooltip_nonpartial"]+'"></i>'
                            }

                            endtime = "Undefined"
                            if (line['end'] != null)
                            {
                                endtime = line['end'];
                            }

                            source_link = ''
                            if (line["sources"] != '')
                            {
                                source_link = "<a href='" + line["sources"]+ "' target='_blank'>Source</a>"
                            }


                            htmlLine = '<p>'+ line['canton']['name'] + "  "+ str_level+ tendency+"<br>"+line["type"]["name"] +'<br>Level: '+ (line['level'] +1) +', End: '+endtime+"<br>"+line["comment"]+source_link+"</p>";

         return htmlLine;
     }
    function LoadCantons()
    {
                 //-----------------------------Load countries----------------------

          var dataCountries = $.ajax({
          url: "/measuremeterdata/chcantons/",
          dataType: "json",
          async: false
          }).responseText;

          var jsonCountries = JSON.parse(dataCountries);

          countries = []
          countries_html=''

          $.each(jsonCountries, function(id, line) {
               countries.push({
                    name: '<font size="5em">'+line['name']+'</font>',
                    value: line['pk']
                  });
          });

          $('#cantons_dd')
              .dropdown({
                values:countries
              })
            ;
    }

    function LoadMeasureTypes()
    {
                  //-----------------------------Load MeasureTypes----------------------

          var dataMeasuresTypes = $.ajax({
          url: "/measuremeterdata/chmeasuretypes_intern/",
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

    function prep_annotations(jsonData, annotations_prepare)
    {
            var last_line

         $.each(jsonData, function(id, line) {
            if (line['start'] != null)
            {
                doesexist = false;
                let obj = annotations_prepare.find((o, i) => {
                    if (o.value === line['start']) {
                        if (o.label.includes(line["canton"]["code"]))
                        {
                           codes = annotations_prepare[i]["label"]
                        }
                        else
                        {
                           codes = annotations_prepare[i]["label"] + ", " + line["canton"]["code"] + ""
                        }

                        popUp = annotations_prepare[i]["popup"] + "<br>" + FormatPopUp(line, last_line);

                        annotations_prepare[i] = { label: codes, value: line['start'], popup: popUp };
                        doesexist = true;
                        return true; // stop searching
                    }
                });

                if (!doesexist)
                {
                    measure_count = 0
                   annotations_prepare.push(
                        {
                            value: line['start'],
                            label: line["canton"]["code"],
                            popup: FormatPopUp(line, last_line)
                        }
                    );
                }
                last_line = line;


            }
            });
            return annotations_prepare
    }

     function LoadMeasureGraph(startdate, enddate, gr_cantons, gr_measuretypes)
     {
          if (gr_cantons == undefined)
          {
            gr_cantons = ""
          }


          if (gr_measuretypes == undefined)
          {
            gr_measuretypes = ""
          }

        annotations_prepare = new Array()

          var data = $.ajax({
          url: "/measuremeterdata/chmeasures_intern/?canton="+gr_cantons+"&type="+gr_measuretypes,
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

          annotations_prepare = prep_annotations(jsonData, annotations_prepare)

          var data = $.ajax({

          url: "/measuremeterdata/chmeasures_intern/?canton=173&type=",
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

          annotations_prepare = prep_annotations(jsonData, annotations_prepare)



            annotations = new Array()

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
                            $("#dialog").html('<div style="margin-left: 10;margin-top: 10;margin-right: 10;margin-bottom: 10;max-height: 600">' + element.popup + '</div>');
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

	 function LoadDataGraph(real_startdate, real_enddate, cantons, measures)
      {

        if (cantons == undefined)
          {
            cantons = ""
          }
        startdate = formatDate(real_startdate);
        enddate = formatDate(real_enddate);

        var data = $.ajax({
          url: "/measuremeterdata/chcases/?date_after="+startdate.replace('-', '\-')+"&date_before="+enddate.replace('-', '\-')+"&canton="+cantons+"&level=0",
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

        var row = new Array()
        old_date = new Date(2020, 1, 1);

        canton_pk = -1

        var dataset = new Array()
        var dataset_data = new Array()
        var dataset_tendency = new Array()
        var dataset_tendency_data = new Array()

        var label_array = new Array()

        for (var d = real_startdate; d <= real_enddate; d.setDate(d.getDate() + 1)) {
            label_array.push(formatDate(new Date(d)));
        }

        turn = 0
        border_width = 4

        $.each(jsonData, function(id, line) {

           if (canton_pk != line["canton"]["pk"] && canton_pk != -1)
           {
              color = Colors[turn];
              turn += 1
              dataset.push({"label": canton_name, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, borderWidth: border_width, data: dataset_data})
              dataset_tendency.push({"label": canton_name, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, borderWidth: border_width, data: dataset_tendency_data})
              dataset_data = new Array()
              dataset_tendency_data = new Array()

           }
            canton_pk = line["canton"]["pk"]
            canton_name = line['canton']['code'].toUpperCase();
            dataset_data.push(line['incidence_past7days'])
            dataset_tendency_data.push(line['development7to7'])


        });

              color = Colors[turn];
        dataset.push({"label": canton_name, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, borderWidth: border_width, data: dataset_data})
        dataset_tendency.push({"label": canton_name, fill: false, pointRadius: 0.1, backgroundColor: color, borderColor: color, borderWidth: border_width, data: dataset_tendency_data})

        annotations = LoadMeasureGraph(startdate, enddate, cantons, measures)

            config = {
                type: 'line',
                    elements: {
                        point:{
                            radius: 0
                        }
                    },
                data: {
                    labels: label_array,
                    datasets: dataset
                },
                options: {

                    legend:{display: true,labels:{fontSize:20}},
                    responsive: true,
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
                                labelString: 'Incidence per 100k/past 7 days'
                            }
                        }
                    },

      annotation: {
        events: ["click","mouseover"],
        annotations: annotations



          }
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
                    title: {
                        display: true,
                        text: ['Development past week/week before (%)'],
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
                            },
                        },
                        y: {
                            display: true,
                            scaleLabel: {
                                display: true,
                                labelString: 'Development past week/week before (%)'
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



      function LoadCantonData()
      {
          var data = $.ajax({
          url: "/measuremeterdata/chcantons/",
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

          LoadMeasures();
      }

      function LoadMeasures()
      {
            var d = new Date();
            today = formatDate(d);


          data = $.ajax({
          url: "/measuremeterdata/chmeasures_intern/?start="+today.replace('-', '\-')+"&end="+today.replace('-', '\-'),
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

            var current_content = ''

            current_content +=`<div class="ui link cards">`
           $.each(jsonData, function(id, line) {
                    var tooltip = line['type']['tooltip_level1']
                    var color_symbol = 'orange'

                    if (line['level'] == 1 )
                    {
                        tooltip = line['type']['tooltip_level2']
                        color_symbol = 'red'
                    }
                    else if (line['level'] == 2 )
                    {
                        tooltip = line['type']['tooltip_level3']
                        color_symbol = 'black'
                    }

                    var start_str = line['start']
                    if (line['start'] == null)
                    {
                         start_str = 'undefined'
                    }

                    var end_str = line['end']
                    if (line['end'] == null)
                    {
                         end_str = 'undefined'
                    }

                    var details='';
                    if (line['comment'] != '')
                    {
                    details = `                        <div class="ui accordion">
                          <div class="active title">
                            <i class="dropdown icon"></i>
                            Details
                          </div>
                          <div class="active content">
                                                `+ line['comment'] +`
                          </div>
                          </div>`
                          }

                   current_content +=` <div class="card" style="min-width:420px">
                    <div class="content">
                      <div class="header"><font size='5em'>`+ line['canton']['name']  +`</font></div>
                      <div class="meta">
                        <a><i class="ban big icon" style='color:`+ color_symbol +`'></i><font size='5em'>&nbsp;`+ line['type']['name'] +`</font></a>
                      </div>
                      <div class="description" >
                        <font size='5em'>`+ details +`</font>
                      </div>
                    </div>
                    <div class="extra content">

                      <span class="right floated">
                        `+ end_str +`
                      </span>
                      <span>
                        <i class="calendar alternate outline icon"></i>
                        `+ start_str +`
                      </span>
                      <span> until </span>
                      <span><br><font size='1rem'>Last updated: `+ line['updated'] +`</font></span>

                    </div></div>`



                });

           current_content += '</div>'

          document.getElementById('current').innerHTML = current_content

      }

      $(window).on('load', function() {
      		    $("#load_data").click(function(){
                if(window.myLine && window.myLine !== null){
                   window.myLine.destroy();
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


                LoadDataGraph(datefrom_real,dateto_real,$('#cantons_dd').dropdown('get value'),$('#measuretypes_dd').dropdown('get value'));
    			window.myLine = new Chart(ctx, config);
    			window.myLineTendency = new Chart(ctxTendency, config_tendency);

            });

            $("#save_incidence").click(function(){
                            save_image("compareChart")
            });

            $("#save_tendency").click(function(){
                            save_image("compareTendency")
            });

            $('#dimmer').dimmer('show');

            $('.ui.accordion')
                 .accordion()
            ;

            $('#param').hide();

            real_enddate = new Date();
            real_startdate = new Date(2020,7,8)

            document.getElementById("datefrom").value = formatDate(real_startdate)
            document.getElementById("dateto").value = formatDate(real_enddate)



            LoadMeasureTypes();
            LoadCantons()

            //LoadCantonData();

			//drawTimeline(2);


            $('#cantons_dd').dropdown('set selected', ['37','35','43'])

            LoadDataGraph(real_startdate,real_enddate,$('#cantons_dd').dropdown('get value'),$('#measuretypes_dd').dropdown('get value'));
			var ctx = document.getElementById('compareChart').getContext('2d');
			window.myLine = new Chart(ctx, config);

			var ctxTendency = document.getElementById('compareTendency').getContext('2d');
			window.myLineTendency = new Chart(ctxTendency, config_tendency);

			$('#dimmer').dimmer('hide');

      });

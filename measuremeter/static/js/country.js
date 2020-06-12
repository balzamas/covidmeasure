      function LoadCountryData(country_id)
      {
          var data = $.ajax({
          url: "/measuremeterdata/countries/?pk="+country_id,
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

          LoadMeasures(country_id);


          document.getElementById('worldometer').innerHTML = '<p><a href= "' + jsonData[0].link_worldometer + '" target="_blank">Link World-o-meter</a></p>';
          document.getElementById('gov').innerHTML = '<p><a href="' + jsonData[0].link_gov + '" target="_blank">Link Government</a></p>' ;
          if (Number(jsonData[0].average_death_per_day)>0)
          {
            $('#avg_desc').show();
            $('#avg_peak_desc').show();
            $('#source_death').show();
            $('#deaths_description').show();
            document.getElementById('avg_desc').innerHTML = "<p>Deaths Average: " + jsonData[0].avg_desc +"</p>";
            document.getElementById('avg_peak_desc').innerHTML = "<p>Deaths Peak: " + jsonData[0].avg_peak_desc+"</p>";
            document.getElementById('source_death').innerHTML = "<p>Source total deaths: <a href='" + jsonData[0].source_death +"'> Link</a></p>";

          }
          else
          {
            $('#avg_desc').hide();
            $('#avg_peak_desc').hide();
            $('#source_death').hide();
            $('#deaths_description').hide();
           }
          return [jsonData[0].average_death_per_day, jsonData[0].average_death_per_day_peak];
      }

      function LoadMeasures(country_id)
      {
            var d = new Date();
            today = formatDate(d);


          var data = $.ajax({
          url: "/measuremeterdata/measures/?country="+country_id.toString()+"&start="+today.replace('-', '\-')+"&end="+today.replace('-', '\-'),
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

            var current_content = ''

            current_content +=`<div class="ui link cards">`
           $.each(jsonData, function(id, line) {
                if (line['level'] > 0)
                {
                    var tooltip = ''
                    var color_symbol = 'white'
                    if (line['level'] == 1 )
                    {
                        tooltip = line['type']['tooltip_partial']
                        color_symbol = 'orange'
                    }
                    else if (line['level'] == 2 )
                    {
                        tooltip = line['type']['tooltip_nonpartial']
                        color_symbol = 'red'
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
                      <div class="header"><font size='5em'>`+ line['type']['name'] +`</font></div>
                      <div class="meta">
                        <a><i class="ban big icon" style='color:`+ color_symbol +`'></i><font size='5em'>&nbsp;`+ tooltip +`</font></a>
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


                }
                });

           current_content += '</div>'

          document.getElementById('current').innerHTML = current_content

      }

      function drawLineChart(country, avg_values, startdate, endate)
      {
          var container = document.getElementById('lineChartCases');
          var containerDeaths = document.getElementById('lineChartDeaths');

          lastdate_x = formatDate(endate);
          firstdate_x = formatDate(startdate);

          var data = $.ajax({
          url: "/measuremeterdata/casesdeaths/?country="+country+"&date_after="+firstdate_x+"&date_before="+lastdate_x,
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

         var diffTime = Math.abs(lastdate - firstdate);
         var diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
         dayscount = 0

         rowsCases = new Array();
         rowsDeaths = new Array();


        $.each(jsonData, function(id, line) {
            dayscount += 1;

            rowsCases.push({"group": 0, "x": line['date'], "y": line['cases']});

              if (Number(avg_values[0] > 0))
              {
                rowsDeaths.push({"group":0, "x": line['date'], "y": line['deaths'] });
                rowsDeaths.push({"group":1, "x": line['date'], "y": line['deathstotal'] });
                rowsDeaths.push({"group":2, "x": line['date'], "y": Number(avg_values[0]) });
                rowsDeaths.push({"group":3, "x": line['date'], "y": Number(avg_values[1]) });
              }
              else
              {
                rowsDeaths.push({"group":0, "x": line['date'], "y": line['deaths'] })
              }
        });

              var names = ['SquareShaded', 'Bargraph', 'Blank', 'CircleShaded'];
                var groups = new vis.DataSet();
                groups.add({
                    id: 0,
                    content: names[0],
                    className: 'custom-style1',
                    options: {
                        drawPoints: {
                            style: 'square' // square, circle
                        },
                        shaded: {
                            orientation: 'bottom' // top, bottom
                        }
                    }});

                groups.add({
                    id: 1,
                    content: names[1],
                    className: 'custom-style2',
                    options: {
                        style:'bar',
                        drawPoints: {style: 'circle',
                            size: 10
                        }
                    }});

                groups.add({
                    id: 2,
                    content: names[2],
                    options: {
                        yAxisOrientation: 'right', // right, left
                        drawPoints: false
                    }
                });

                groups.add({
                    id: 3,
                    content: names[3],
                    className: 'custom-style3',
                    options: {
                        yAxisOrientation: 'right', // right, left
                        drawPoints: {
                            style: 'circle' // square, circle
                        },
                        shaded: {
                            orientation: 'top' // top, bottom
                        }
                    }});

          var dataset = new vis.DataSet(rowsCases);
          var options = {
          };
          var graph2d = new vis.Graph2d(container, dataset, options);

          var datasetDeaths = new vis.DataSet(rowsDeaths);
          var graph2dDeaths = new vis.Graph2d(containerDeaths, datasetDeaths, options);

      }

      function LoadPanelsFiltered()
      {
            if ($('#countries_dd').dropdown('get value') != null)
            {
                avg_values = LoadCountryData($('#countries_dd').dropdown('get value'));
                var datesft = drawTimeline(1,$('#countries_dd').dropdown('get value'));
                drawLineChart($('#countries_dd').dropdown('get value'),avg_values, datesft[0], datesft[1]);
             }
      }

      $(window).on('load', function() {
         $("#countries_dd").change(function() {
               LoadPanelsFiltered()
            });

            $('.ui.accordion')
                 .accordion()
            ;

            $('#param').hide();

            if ($('#param').text() != '')
            {
                $('#countries_dd').dropdown('set selected',$('#param').text());
            }
            else
            {
                var rnd_country = Math.floor(Math.random() * 43) + 1;

                $('#countries_dd').dropdown('set selected',rnd_country);
            }
      });

      function LoadCountryData(country_id)
      {
          var data = $.ajax({
          url: "/measuremeterdata/countries/?pk="+country_id,
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

          LoadMeasures(country_id);


          document.getElementById('worldometer').innerHTML = '<a href= "' + jsonData[0].link_worldometer + '" target="_blank">Link World-o-meter</a>';
          document.getElementById('gov').innerHTML = '<a href="' + jsonData[0].link_gov + '" target="_blank">Link Government</a>' ;
          if (Number(jsonData[0].average_death_per_day)>0)
          {
            $('#avg_desc').show();
            $('#avg_peak_desc').show();
            $('#source_death').show();
            $('#deaths_description').show();
            document.getElementById('avg_desc').innerHTML = "Deaths Average: " + jsonData[0].avg_desc;
            document.getElementById('avg_peak_desc').innerHTML = "Deaths Peak: " + jsonData[0].avg_peak_desc;
            document.getElementById('source_death').innerHTML = "Source total deaths: <a href='" + jsonData[0].source_death +"'> Link</a>";

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

            current_content +=`<div class="ui link large cards">`
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

                   current_content +=` <div class="card">
                    <div class="content">
                      <div class="header">`+ line['type']['name'] +`</div>
                      <div class="meta">
                        <a><i class="ban icon" style='color:`+ color_symbol +`'></i>&nbsp;`+ tooltip +`</a>
                      </div>
                      <div class="description" >
                        `+ details +`
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

      function LoadPanelsFiltered()
      {
            if ($('#countries_dd').dropdown('get value') != null)
            {
                avg_values = LoadCountryData($('#countries_dd').dropdown('get value'));
                drawChartByCountries($('#countries_dd').dropdown('get value'));
                drawChartCases($('#countries_dd').dropdown('get value'),avg_values);

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

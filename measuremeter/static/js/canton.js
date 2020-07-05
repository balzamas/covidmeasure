      function LoadCantonData(canton_id)
      {
          var data = $.ajax({
          url: "/measuremeterdata/chcantons/?pk="+canton_id,
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

          LoadMeasures(canton_id);
      }

      function LoadMeasures(canton_id)
      {
            var d = new Date();
            today = formatDate(d);


          var data = $.ajax({
          url: "/measuremeterdata/chmeasures/?start="+today.replace('-', '\-')+"&end="+today.replace('-', '\-'),
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



      function LoadPanelsFiltered()
      {
                avg_values = LoadCantonData($('#cantons_dd').dropdown('get value'));
                var datesft = drawTimeline(2,$('#cantons_dd').dropdown('get value'));
               // drawLineChart($('#cantons_dd').dropdown('get value'),avg_values, datesft[0], datesft[1]);
      }

      $(window).on('load', function() {

            $('.ui.accordion')
                 .accordion()
            ;

            $('#param').hide();

            LoadPanelsFiltered();

            // CSSMap;
            $("#map-switzerland").CSSMap({
              "size": 850,
              "mapStyle": "blue",
              "tooltips": "floating-top-center",
              "responsive": "auto"
            });
            // END OF THE CSSMap;
      });

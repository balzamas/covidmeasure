      function LoadCountryData(country_id)
      {
          var data = $.ajax({
          url: "/measuremeterdata/countries/?pk="+country_id,
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

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

      function LoadPanelsFiltered()
      {
            if ($('#countries_dd').dropdown('get value') != null)
            {
                avg_values = LoadCountryData($('#countries_dd').dropdown('get value'));
                drawChartByCountries($('#countries_dd').dropdown('get value'));
                drawChartCases($('#countries_dd').dropdown('get value'),avg_values);

             }
      }

      $( document ).ready(function() {
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
      });

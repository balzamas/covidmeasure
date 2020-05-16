


      function LoadPanelsFiltered()
      {
            drawChartByCountries($('#countries_dd').dropdown('get value'));
            drawChartCases($('#countries_dd').dropdown('get value'));
      }



      $( document ).ready(function() {
         $("#countries_dd").change(function() {
               LoadPanelsFiltered()
            });

            $('#param').hide();

            if ($('#param').text() != '')
            {

                $('#countries_dd').dropdown('set selected',$('#param').text());
                 google.charts.setOnLoadCallback(drawChartByCountries($('#param').text()));
                 google.charts.setOnLoadCallback(drawChartCases($('#param').text()));
            }
            else
            {
                 google.charts.setOnLoadCallback(drawChartByCountries);

            }


      });

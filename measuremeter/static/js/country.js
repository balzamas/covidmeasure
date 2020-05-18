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
            }
            else
            {
                 $('#countries_dd').dropdown('set selected',1);
            }


      });

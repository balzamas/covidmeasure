      function LoadCountryData(country_id)
      {
          var data = $.ajax({
          url: "/measuremeterdata/countries/?country="+country_id,
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

          document.getElementById('worldometer').innerHTML = '<a href= "' + jsonData[0].link_worldometer + '" target="_blank">Link World-o-meter</a>';
          document.getElementById('gov').innerHTML = '<a href="' + jsonData[0].link_gov + '" target="_blank">Link Government</a>' ;
      }

      function LoadPanelsFiltered()
      {
            if ($('#countries_dd').dropdown('get value') != null)
            {
                drawChartByCountries($('#countries_dd').dropdown('get value'));
                drawChartCases($('#countries_dd').dropdown('get value'));
                LoadCountryData($('#countries_dd').dropdown('get value'));
             }
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

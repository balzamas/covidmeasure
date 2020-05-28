

      function LoadPanelsFiltered()
      {
            drawChartByCountries($('#countries_dd').dropdown('get value'), $('#measuretypes_dd').dropdown('get value'));
            drawChartByMeasures($('#countries_dd').dropdown('get value'), $('#measuretypes_dd').dropdown('get value'));
      }

      function switchPanels() {
          var x = document.getElementById("bycountry");
          if (x.style.display === "none") {
            x.style.display = "block";
            $('#loadtext').html("by measure");

          } else {
            x.style.display = "none";
            $('#loadtext').html("by country");
          }
          var y = document.getElementById("bymeasure");
          if (y.style.display === "none") {
            y.style.display = "block";
          } else {
            y.style.display = "none";
          }

          LoadPanelsFiltered();
        }

        function copyToClipboard() {
          var copyText = window.location.host + "/timeline/" + $('#countries_dd').dropdown('get value');
          navigator.clipboard.writeText(copyText);
        }

      $(window).on('load', function() {
          //document.getElementById("dateselect").valueAsDate = new Date();

          $("#load_data").click(function(){
            LoadPanelsFiltered();
          });

          $("#change_mode").click(function(){
            switchPanels();
          });


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
                    name: line['name'],
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
                console.log($('#param').text())
                drawChartByMeasures($('#param').text(), $('#measuretypes_dd').dropdown('get value'));
            }
            else
            {
                rnd_country = Math.floor(Math.random() * 43) + 1;
                rnd_country2 = Math.floor(Math.random() * 43) + 1;
                rnd_country3 = Math.floor(Math.random() * 43) + 1;

                countries=rnd_country.toString()+","+rnd_country2.toString()+","+rnd_country3.toString();
                drawChartByMeasures(countries, $('#measuretypes_dd').dropdown('get value'));
            }

          $("#btnCopyLink").click(async function(){
                copyToClipboard();
          });


      });




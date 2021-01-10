     var mode = 1;

      function LoadPanelsFiltered()
      {
            var datesft = drawTimeline(mode,$('#countries_dd').dropdown('get value'), $('#measuretypes_dd').dropdown('get value'));
      }

      function switchPanels() {
          if (mode == 1)
          {
                 mode = 2;
                $('#loadtext').html("by country");
           }
           else
           {
               mode = 1;
               $('#loadtext').html("by measure");
           }
          LoadPanelsFiltered();
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
                console.log("hahahahah11");
                console.log($('#param').text())
                console.log(mode)
                var datesft = drawTimeline(mode, $('#param').text(), $('#measuretypes_dd').dropdown('get value'));
                console.log(datesft)
                drawChartCasesTimeline($('#param').text(),datesft[0], datesft[1])

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

                var datesft = drawTimeline(mode, countries, measuretypes);
            }

          $("#btnCopyLink").click(async function(){
                copyToClipboard("/timeline/" + $('#countries_dd').dropdown('get value'));
          });


      });




      google.charts.load("current", {packages:["timeline"]});
      google.charts.setOnLoadCallback(drawChart);

      /* Set the width of the side navigation to 250px */
      function openNav() {
        document.getElementById("mySidenav").style.width = "500px";
      }

      /* Set the width of the side navigation to 0 */
      function closeNav() {
        document.getElementById("mySidenav").style.width = "0";
      }

      function LoadPanelsFiltered()
      {
            var countries = ""
            $.each($("input[name='country']:checked"), function(){
                countries = countries + $(this).val() +",";
            });

            var types = ""
            $.each($("input[name='type']:checked"), function(){
                types = types + $(this).val() +",";
            });

            drawChart(countries, types);
      }

      function switchPanels() {
          var x = document.getElementById("bycountry");
          if (x.style.display === "none") {
            x.style.display = "block";
          } else {
            x.style.display = "none";
          }
          var y = document.getElementById("bymeasure");
          if (y.style.display === "none") {
            y.style.display = "block";
          } else {
            y.style.display = "none";
          }

          LoadPanelsFiltered();


        }

      function convertMiliseconds(miliseconds, format) {
        var days, hours, minutes, seconds, total_hours, total_minutes, total_seconds;

        total_seconds = parseInt(Math.floor(miliseconds / 1000));
        total_minutes = parseInt(Math.floor(total_seconds / 60));
        total_hours = parseInt(Math.floor(total_minutes / 60));
        days = parseInt(Math.floor(total_hours / 24));

        seconds = parseInt(total_seconds % 60);
        minutes = parseInt(total_minutes % 60);
        hours = parseInt(total_hours % 24);

        switch(format) {
        case 's':
          return total_seconds;
        case 'm':
          return total_minutes;
        case 'h':
          return total_hours;
        case 'd':
          return days;
        default:
          return { d: days, h: hours, m: minutes, s: seconds };
        }
      };


      $( document ).ready(function() {
          //document.getElementById("dateselect").valueAsDate = new Date();

          $("#btnSubmit").click(function(){
            LoadPanelsFiltered();
          });

          $("#btnSubmitMap").click(function(){
                var measuretype = $("#measurechooser").children("option:selected").val();
                var seldate = document.getElementById("dateselect").value;
                loadMapData(measuretype,seldate);
          });

          //-----------------------------Load countries----------------------

          var dataCountries = $.ajax({
          url: window.location.href + "../measuremeterdata/countries/",
          dataType: "json",
          async: false
          }).responseText;

          var jsonCountries = JSON.parse(dataCountries);

          var optionsCountries='';
          optionsCountries += '<div class="form-check"><input type="checkbox" class="form-check-input" name="checkbox-all" id="checkbox-all-country" value="all"  />';
          optionsCountries += '<label class="form-check-label" for="checkbox-all">All</label></div>';

          $.each(jsonCountries, function(id, line) {
               optionsCountries += '<div class="form-check form-check-inline"><input type="checkbox" class="form-check-input" name="country" id="checkbox-' + id + '" value="' + line['pk'] + '"  />';
               optionsCountries += '<label class="form-check-label" for="checkbox-' + id + '">' + line['name'] + '</label></div>&nbsp;';
          });
          $('#countries').append(optionsCountries);

          //-----------------------------Load MeasureTypes----------------------

          var dataMeasuresTypes = $.ajax({
          url: window.location.href + "../measuremeterdata/measuretypes/",
          dataType: "json",
          async: false
          }).responseText;

          var jsonMeasuresTypes = JSON.parse(dataMeasuresTypes);

          var optionsMeasuresTypes='';
          //optionsMeasuresTypes += '<div class="form-check"><input type="checkbox" class="form-check-input" name="checkbox-all" id="checkbox-all" value="all" />';
          //optionsMeasuresTypes += '<label class="form-check-label" for="checkbox-all">All</label></div>';

          var category = -1;

          var select = document.getElementById("measurechooser");

          $.each(jsonMeasuresTypes, function(id, line) {
              if (line['category']['pk'] != category)
              {
                category = line['category']['pk'];
                optionsMeasuresTypes += '<b><div class="form-check"><input type="checkbox" class="form-check-input" name="category" id="category" value="' + category + '" />';
                optionsMeasuresTypes += '<label class="form-check-label" for="checkbox-' + category + '">' + line['category']['name'] + '</label></div></b>';


              }
               optionsMeasuresTypes += '<div class="form-check form-check-inline"><input type="checkbox" class="form-check-input" name="type" id="' + category + '" value="' + line['pk'] + '"  />';
               optionsMeasuresTypes += '<label class="form-check-label" for="checkbox-' + id + '">' + line['name'] + '</label></div>&nbsp;';

             //   var el = document.createElement("option");
             //   el.textContent = line['name'];
             //   el.value = line['pk'];
             //   select.appendChild(el);
          });
          $('#measurestypes').append(optionsMeasuresTypes);

          //-----------------------------CheckBox logix-------------------------------------

          $("#checkbox-all-country").click(function() {
              if($(this).is(":checked"))
              {
                  $.each($("input[name='country']"), function(){
                      $(this).prop("checked", true);
                  });
              }
              else
              {
                  $.each($("input[name='country']"), function(){
                      $(this).prop("checked", false);
                  });
              }
          });

           $.each($("input[name='category']"), function(){
                $(this).click(function() {
                  if($(this).is(":checked"))
                  {
                    $.each($("input[id="+$(this).val()+"]"), function(){
                        $(this).prop("checked", true);
                    });
                  }
                  else
                  {
                    $.each($("input[id="+$(this).val()+"]"), function(){
                        $(this).prop("checked", false);
                    });
                  }
                });
            });
      });



     //-----------------------------DrawChart-------------------------------------


      function drawChart(countries, measuretypes) {

         if (countries == undefined)
         {
           countries="";
         }
         if (measuretypes == undefined)
         {
           measuretypes="";
         }
         console.log(countries + " " + measuretypes);
          var data = $.ajax({
          url: window.location.href + "../measuremeterdata/measures/?country="+countries+"&type="+measuretypes,
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

        var containerCountry = document.getElementById('datachartCountry');
        var chartCountry = new google.visualization.Timeline(containerCountry);
        var dataTableCountry = new google.visualization.DataTable();

        dataTableCountry.addColumn({ type: 'string', id: 'Country' });
        dataTableCountry.addColumn({ type: 'string', id: 'Measure' });
        dataTableCountry.addColumn({ type: 'string', role:'tooltip'});
        dataTableCountry.addColumn({ type: 'string', role: 'style' });
        dataTableCountry.addColumn({ type: 'date', id: 'Start' });
        dataTableCountry.addColumn({ type: 'date', id: 'End' });

        var ColorClosed = ["#90d192", '#91e3e0', '#eba9e3', '#b4b9ed', '#e6c4a1', '#e6a1a4', '#a8e6d6'];
        var ColorPartial = ["#b7e8b9", '#bce6e4', '#f2d3ee', '#cfd1e8', '#ebd9c7', '#e6bec0', '#c7ebe2'];

        //Get first and last date
        var firstdate = new Date(2020, 5, 1);
        var lastdate = new Date(2020, 5, 1);

        $.each(jsonData, function(id, line) {
          if (line['start'] != null)
          {
            var start_strfl = line['start'].split("-")
            var start_datefl = new Date(start_strfl[0], start_strfl[1]-1, start_strfl[2])
          }

          if (line['end'] != null)
          {
            var end_strfl = line['end'].split("-")
            var end_datefl = new Date(end_strfl[0], end_strfl[1]-1, end_strfl[2])
          }

          if (start_datefl < firstdate)
          {
            firstdate = start_datefl;
          }

          if (end_datefl > lastdate)
          {
            lastdate = end_datefl;
          }
        });

        $.each(jsonData, function(id, line) {
          var type = line['type']['name'].toString();

          if (line['start'] != null)
          {
            var start_str = line['start'].split("-")
            var start_date = new Date(start_str[0], start_str[1]-1, start_str[2])
          }
          else
          {
            var start_date = firstdate;
          }

          if (line['end'] != null)
          {
            var end_str = line['end'].split("-")
            var end_date = new Date(end_str[0], end_str[1]-1, end_str[2])
            var end_date_str = line['end']
          }
          else
          {
            var end_date = lastdate;
            type = type + "*";
            var end_date_str = 'undefined'
          }



          //Set up tooltip
          days = convertMiliseconds(end_date - start_date,'d')+1;
          var tooltip = '<div style="margin-left: 5;margin-top: 5;margin-bottom: 5;margin-right: 5;width: 300">'
          tooltip += "<p><b>"+type+"</b></p>";
          if (line['none'] == false)
          {
            tooltip += "<p>"+ line['start'] + " - " + end_date_str + " // Duration: " + days + " days</p>";
          }
          tooltip += "<hr>";
          tooltip += line['comment'].toString();
          tooltip += '</div>';

          if (line['partial'] == true)
          {
            type += " " +  line['type']['tooltip_partial'];
            color = ColorPartial[line['type']['category']['pk']];
          }
          else
          {
            color = ColorClosed[line['type']['category']['pk']];
            if (line['none'] != true)
           {
             type += " " + line['type']['tooltip_nonpartial'];
           }
          }

          if (line['none'] == true)
          {
            type += " (none)";
            color='#FFFFFF';
          }

          var source = "Source: " + line['sources'].toString()

          dataTableCountry.addRows([[line['country']['name'].toString(),type,tooltip,color, start_date,end_date]])
});
        chartCountry.draw(dataTableCountry);

         console.log(countries + " " + measuretypes);
          var dataMeasure = $.ajax({
          url: window.location.href + "../measuremeterdata/measuresbymeasure/?country="+countries+"&type="+measuretypes,
          dataType: "json",
          async: false
          }).responseText;
          var jsonDataMeasure = JSON.parse(dataMeasure);

        var containerMeasure = document.getElementById('datachartMeasure');
        var chartMeasure = new google.visualization.Timeline(containerMeasure);
        var dataTableMeasure = new google.visualization.DataTable();

        dataTableMeasure.addColumn({ type: 'string', id: 'Country' });
        dataTableMeasure.addColumn({ type: 'string', id: 'Measure' });
        dataTableMeasure.addColumn({ type: 'string', role:'tooltip'});
        dataTableMeasure.addColumn({ type: 'string', role: 'style' });
        dataTableMeasure.addColumn({ type: 'date', id: 'Start' });
        dataTableMeasure.addColumn({ type: 'date', id: 'End' });

        var ColorClosed = ["#90d192", '#91e3e0', '#eba9e3', '#b4b9ed', '#e6c4a1', '#e6a1a4', '#a8e6d6'];
        var ColorPartial = ["#b7e8b9", '#bce6e4', '#f2d3ee', '#cfd1e8', '#ebd9c7', '#e6bec0', '#c7ebe2'];

        $.each(jsonDataMeasure, function(id, line) {
          var type = line['type']['name'].toString();
          country = line['country']['name'].toString();

          if (line['start'] != null)
          {
            var start_str = line['start'].split("-")
            var start_date = new Date(start_str[0], start_str[1]-1, start_str[2])
          }
          else
          {
            var start_date = firstdate;
          }


          if (line['end'] != null)
          {
            var end_str = line['end'].split("-")
            var end_date = new Date(end_str[0], end_str[1]-1, end_str[2])
            var end_date_str = line['end']
          }
          else
          {
            var end_date = lastdate;
            country = country + "*";
            var end_date_str = 'undefined'
          }

          if (line['partial'] == true)
          {
             country += " " +  line['type']['tooltip_partial'];
             color = ColorPartial[line['type']['category']['pk']];
          }
          else
          {
              if (line['none'] != true)
             {
                country += " " + line['type']['tooltip_nonpartial'];
             }
            color = ColorClosed[line['type']['category']['pk']];
          }

          if (line['none'] == true)
          {
            country += " (none)";
            color='#FFFFFF';
          }

          //Set up tooltip
          days = convertMiliseconds(end_date - start_date,'d')+1;
          var tooltip = '<div style="margin-left: 5;margin-top: 5;margin-bottom: 5;margin-right: 5;width: 300">'
          tooltip += "<p><b>"+type+"</b></p>";
          if (line['none'] == false)
          {
            tooltip += "<p>"+ line['start'] + " - " + end_date_str + " // Duration: " + days + " days</p>";
          }
          tooltip += "<hr>";
          tooltip += line['comment'].toString();
          tooltip += '</div>';

          var source = "Source: " + line['sources'].toString()

          dataTableMeasure.addRows([[type,country,tooltip,color,start_date,end_date]]);


});
          var options = {
            timeline: { avoidOverlappingGridLines: true}
          };

        chartMeasure.draw(dataTableMeasure, options);

      }

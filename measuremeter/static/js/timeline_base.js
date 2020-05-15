      google.charts.load("current", {packages:["timeline"]});
        google.charts.load('current', {'packages':['corechart']});





      var ColorClosed = ["#90d192", '#91e3e0', '#eba9e3', '#b4b9ed', '#e6c4a1', '#e6a1a4', '#a8e6d6'];
      var ColorPartial = ["#b7e8b9", '#bce6e4', '#f2d3ee', '#cfd1e8', '#ebd9c7', '#e6bec0', '#c7ebe2'];

     //-----------------------------DrawChart-------------------------------------

      function getStartEndDate(jsonData) {
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

            return [firstdate, lastdate];
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

      function drawChartCases(country, datefrom, dateto) {

          var data = $.ajax({
          url: "/measuremeterdata/casesdeaths/?country="+country+"&date_after="+datefrom+"&date_before="+dateto,
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

        var cases = new google.visualization.LineChart(document.getElementById('datachartCases'));

        var containerCases = document.getElementById('datachartCases');
        var chartCases = new google.visualization.Timeline(containerCases);
        var dataTableCases = new google.visualization.DataTable();

        dataTableCases.addColumn({ type: 'string', id: 'Country' });
        dataTableCases.addColumn({ type: 'int', id: 'Country2' });
        dataTableCases.addColumn({ type: 'int', id: 'Country3' });


        $.each(jsonData, function(id, line) {
            dataTableCases.addRows("aa",33,33);


        });
                var data = google.visualization.arrayToDataTable([
                  ['Year', 'Sales', 'Expenses'],
                  ['2004',  1000,      400],
                  ['2005',  1170,      460],
                  ['2006',  660,       1120],
                  ['2007',  1030,      540]
                ]);

                var options = {
                  title: 'Company Performance',
                  curveType: 'function',
                  legend: { position: 'bottom' }
                };
                cases.draw(dataTableCases, options);
      }



      function drawChartByCountries(countries, measuretypes) {

         console.log("Country:");
         console.log(countries);
         if (countries == undefined)
         {
          //Startup: set random country
          rnd_country = Math.floor(Math.random() * 43) + 1;  // returns a random integer from 1 to 10
           countries=rnd_country.toString();
         }
         if (measuretypes == undefined)
         {
           measuretypes="";
         }
          var data = $.ajax({
          url: "/measuremeterdata/measures/?country="+countries+"&type="+measuretypes,
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

            var startend_dates=getStartEndDate(jsonData)
            var firstdate = startend_dates[0]
            var lastdate = startend_dates[1]

        $.each(jsonData, function(id, line) {


          var type = line['type']['name'].toString();

          if (line['start'] != null)
          {
            var start_str = line['start'].split("-")
            var start_date = new Date(start_str[0], start_str[1]-1, start_str[2])
            var start_date_str = line['start'];
          }
          else
          {
            var start_date = firstdate;
            var start_date_str = ""
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

          if (line['isregional'] == true)
          {
            type = type + "#";
          }

          //Set up tooltip
          days = convertMiliseconds(end_date - start_date,'d')+1;
          var tooltip = '<div style="margin-left: 5;margin-top: 5;margin-bottom: 5;margin-right: 5;width: 300">'
          tooltip += "<p><b>"+type+"</b></p>";

          if (line['end'] != null || line['start'] != null)
          {
            tooltip += "<p>"+ start_date_str + " - " + end_date_str
            if (line['end'] != null && line['start'] != null)
            {
               tooltip += " // Duration: " + days + " days</p>"
            }
          }
          tooltip += "<hr>";
          tooltip += line['comment'].toString();
          tooltip += '</div>';

          if (line['level'] == 1)
          {
            type += " " +  line['type']['tooltip_partial'];
            color = ColorPartial[line['type']['category']['pk']];
          }
          else
          {
            color = ColorClosed[line['type']['category']['pk']];
            if (line['level'] > 0)
           {
             type += " " + line['type']['tooltip_nonpartial'];
           }
          }

          if (line['level'] == 0)
          {
            type += " (none)";
            color='#FFFFFF';
          }

          var source = "Source: " + line['sources'].toString()

          dataTableCountry.addRows([[line['country']['name'].toString(),type,tooltip,color, start_date,end_date]])
});
        chartCountry.draw(dataTableCountry);
      }


      function drawChartByMeasures(countries, measuretypes) {

         if (countries == undefined)
         {
          //Startup: set random country
          rnd_country = Math.floor(Math.random() * 43) + 1;  // returns a random integer from 1 to 10
           countries=rnd_country.toString();
         }
         if (measuretypes == undefined)
         {
           measuretypes="";
         }
          var dataMeasure = $.ajax({
          url: "/measuremeterdata/measuresbymeasure/?country="+countries+"&type="+measuretypes,
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

        var startend_dates=getStartEndDate(jsonDataMeasure)
        var firstdate = startend_dates[0]
        var lastdate = startend_dates[1]


        $.each(jsonDataMeasure, function(id, line) {
          var type = line['type']['name'].toString();
          country = line['country']['name'].toString();

          if (line['start'] != null)
          {
            var start_str = line['start'].split("-")
            var start_date = new Date(start_str[0], start_str[1]-1, start_str[2])
            var start_date_str = line['start'];
          }
          else
          {
            var start_date = firstdate;
            var start_date_str = ""
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

           if (line['isregional'] == true)
          {
            country = country + "#";
          }

          if (line['level'] == 1)
          {
             country += " " +  line['type']['tooltip_partial'];
             color = ColorPartial[line['type']['category']['pk']];
          }
          else
          {
              if (line['level'] != 0)
             {
                country += " " + line['type']['tooltip_nonpartial'];
             }
            color = ColorClosed[line['type']['category']['pk']];
          }



          if (line['level'] == 0)
          {
            country += " (none)";
            color='#FFFFFF';
          }

          //Set up tooltip
          days = convertMiliseconds(end_date - start_date,'d')+1;

          var tooltip = '<div style="margin-left: 5;margin-top: 5;margin-bottom: 5;margin-right: 5;width: 300">'
          tooltip += "<p><b>"+type+"</b></p>";

          if (line['end'] != null || line['start'] != null)
          {
            tooltip += "<p>"+ start_date_str + " - " + end_date_str;
            if (line['end'] != null && line['start'] != null)
            {
               tooltip += " // Duration: " + days + " days</p>"
            }
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

      $( document ).ready(function() {
          //-----------------------------Load countries----------------------

          var dataCountries = $.ajax({
          url: "/measuremeterdata/countries/",
          dataType: "json",
          async: false
          }).responseText;

          var jsonCountries = JSON.parse(dataCountries);

          countries = []
          countries_html=''

          $.each(jsonCountries, function(id, line) {
               countries.push({
                    name: '<i class="'+line['code'] +' flag"/>'+line['name'],
                    value: line['pk']
                  });
          });

          $('#countries_dd')
              .dropdown({
                values:countries
              })
            ;
      });

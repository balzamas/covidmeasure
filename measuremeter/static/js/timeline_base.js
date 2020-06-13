      var ColorClosed = ["#90d192", '#91e3e0', '#eba9e3', '#b4b9ed', '#e6c4a1', '#e6a1a4', '#a8e6d6'];
      var ColorPartial = ["#b7e8b9", '#bce6e4', '#f2d3ee', '#cfd1e8', '#ebd9c7', '#e6bec0', '#c7ebe2'];

      var firstdate = new Date(2020, 5, 1);
      var lastdate = new Date(2020, 5, 1);

        function addDays(date, days) {
          var result = new Date(date);
          result.setDate(result.getDate() + days);
          return result;
        }

     //-----------------------------DrawChart-------------------------------------

      function getStartEndDate(jsonData) {
            //Get first and last date
            firstdate = new Date(2020, 5, 1);
            lastdate = new Date();
            lastdate = addDays(lastdate, 7)

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

              if (start_datefl >= lastdate)
              {
                lastdate = addDays(start_datefl,7);
              }

              if (end_datefl >= lastdate)
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

      function formatDate(d)
        {
            var month = d.getMonth()+1;
            var day = d.getDate();

            var date = d.getFullYear() + '-' +
                (month<10 ? '0' : '') + month + '-' +
                (day<10 ? '0' : '') + day;
            return date;
        }

        function drawTimeline(mode, countries, measuretypes) {
            document.getElementById('timeline').innerHTML = "";
            var container = document.getElementById('timeline');

           if (countries == undefined)
             {
               //Startup: set random country
               rnd_country = Math.floor(Math.random() * 43) + 1;
               rnd_country2 = Math.floor(Math.random() * 43) + 1;
               rnd_country3 = Math.floor(Math.random() * 43) + 1;

               countries=rnd_country.toString()+","+rnd_country2.toString()+","+rnd_country3.toString();
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

        var startend_dates=getStartEndDate(jsonData);
        firstdate = startend_dates[0];
        lastdate = startend_dates[1];

        groups_data = new Array();
        items_data = new Array();
        groups_elements = new Array();

        var count = 0;
        var type_pk = -1;
        var class_type = 'white';


        $.each(jsonData, function(id, line) {

              if (mode == 1)
              {
                  if (type_pk != line["type"]["pk"])
                      {
                         if (!groups_elements.includes(line["type"]["pk"]))
                         {
                           groups_elements.push(line["type"]["pk"]);
                           groups_data.push({"id": line["type"]["pk"], "content": line['type']['name'], subgroupOrder: 'subgroupOrder'});
                          }
                      }
              }
              else
              {
                  if (type_pk != line["country"]["pk"])
                      {
                         if (!groups_elements.includes(line["country"]["pk"]))
                         {
                           groups_elements.push(line["country"]["pk"]);
                           groups_data.push({"id": line["country"]["pk"], "content": line['country']['name'], "stackSubgroups": true,"subgroupOrder":"subgroup"});
                          }
                      }
              }

              var type = line['type']['name'].toString();
              var country = line['country']['name'].toString();

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
                country = country + "*";
                var end_date_str = 'undefined'
              }

              if (line['isregional'] == true)
              {
                type = type + "#";
                country = country + "#";
              }

              //Set up tooltip
              days = convertMiliseconds(end_date - start_date,'d')+1;
              var tooltip = "<p><b>"+type+"</b></p>";

              if (line['end'] != null || line['start'] != null)
              {
                tooltip += "<p>"+ start_date_str + " - " + end_date_str
                if (line['end'] != null && line['start'] != null)
                {
                   tooltip += " <br>Duration: " + days + " days</p>"
                }
              }
              tooltip += line['comment'].toString()+'';

              if (line['level'] == 1)
              {
                type += " " +  line['type']['tooltip_partial'];
                country += " " +  line['type']['tooltip_partial'];
                class_type = 'green'
              }
              else
              {
                class_type = 'orange';
                if (line['level'] > 0)
               {
                 type += " " + line['type']['tooltip_nonpartial'];
                 country += " " + line['type']['tooltip_nonpartial'];
               }
              }

              if (line['level'] == 0)
              {
                type += " (none)";
                country += " (none)";
                class_type='white';
              }

              var source = "Source: " + line['sources'].toString()



               if (mode == 1)
               {
                items_data.push({"id": count, "content": country, "group": line['type']['pk'], "start": start_date, "end": end_date, 'className': class_type, "title": tooltip, "subgroup": line['country']['pk']});
               }
               else
               {
                items_data.push({"id": count, "content": type, "group": line['country']['pk'], "start": start_date, "end": end_date, 'className': class_type, "title": tooltip, "subgroup": line['type']['pk']});
               }

              count += 1;

             //  {id: 1, group: 0, content: 'item 1', start: '2013-04-20', title: 'aaaaa<br>bbbbbb'},

              //dataTableCountry.addRows([[line['country']['name'].toString(),type,tooltip,color, start_date,end_date]])
            });

              var groups = new vis.DataSet(groups_data);

              // Create a DataSet (allows two way data-binding)
              var items = new vis.DataSet(items_data);

              // Configuration for the Timeline
              var options = {
                stack: false,
                stackSubgroups: true
              };

              // Create a Timeline
              var timeline = new vis.Timeline(container, items, groups, options);
                timeline.setOptions(options);
                timeline.setGroups(groups);
            return [firstdate, lastdate];
        }

      function drawLineChart(country, avg_values, startdate, endate)
      {
          var container = document.getElementById('lineChartCases');
          var containerDeaths = document.getElementById('lineChartDeaths');

          lastdate_x = formatDate(endate);
          firstdate_x = formatDate(startdate);

          var data = $.ajax({
          url: "/measuremeterdata/casesdeaths/?country="+country+"&date_after="+firstdate_x+"&date_before="+lastdate_x,
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

         var diffTime = Math.abs(lastdate - firstdate);
         var diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
         dayscount = 0

         rowsCases = new Array();
         rowsDeaths = new Array();


        $.each(jsonData, function(id, line) {
            dayscount += 1;

            rowsCases.push({"group": "Cases", "x": line['date'], "y": line['cases']});

              if (Number(avg_values[0] > 0))
              {
                rowsDeaths.push({"group":"Deaths Corona", "x": line['date'], "y": line['deaths'] });
                rowsDeaths.push({"group":"Deaths Total", "x": line['date'], "y": line['deathstotal'] });
                rowsDeaths.push({"group":"Deaths Average", "x": line['date'], "y": Number(avg_values[0]) });
                rowsDeaths.push({"group":"Deaths Average Peak", "x": line['date'], "y": Number(avg_values[1]) });
              }
              else
              {
                rowsDeaths.push({"group":"Deaths Corona", "x": line['date'], "y": line['deaths'] })
              }
        });


                var groups = new vis.DataSet();
                groups.add({
                    id: "Deaths Average",
                    content: "Deaths Average",
                        });

                groups.add({
                    id: "Deaths Average Peak",
                    content: "Deaths Average Peak",
                  });

                groups.add({
                    id: "Deaths Total",
                    content: "Deaths Total",
                });

                groups.add({
                    id: "Deaths Corona",
                    content: "Deaths Corona",
                    });

          var dataset = new vis.DataSet(rowsCases);
          var options = {
              defaultGroup: "Country ",
          };
          var optionsDeath =
          {
             legend: {left:{position:"top-left"}},
          }
          var graph2d = new vis.Graph2d(container, dataset, options);

          var datasetDeaths = new vis.DataSet(rowsDeaths);
          var graph2dDeaths = new vis.Graph2d(containerDeaths, datasetDeaths, groups, optionsDeath);
          graph2dDeaths.setGroups(groups)

      }

        function drawLineChartperPop(countries, startdate, endate)
        {
          var containergraph = document.getElementById('lineChartCasesPerPop');

          lastdate_x = formatDate(endate);
          firstdate_x = formatDate(startdate);

          var data = $.ajax({
          url: "/measuremeterdata/casesdeaths/?country="+countries+"&date_after="+firstdate_x+"&date_before="+lastdate_x,
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

         var diffTime = Math.abs(lastdate - firstdate);
         var diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
         dayscount = 0

         rowsCases = new Array();

        var diffTime = Math.abs(lastdate - firstdate);
        var diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        dayscount = 0
        ctry_count = countries.split(',').length;
        var row = new Array()
        old_date = new Date(2020, 1, 1);

        country_pk = -1
        country_elements = new Array()
        countries_data = new Array()
        countries_groups = new Array()
        var groupsgraph = new vis.DataSet();

        $.each(jsonData, function(id, line) {
                  if (country_pk != line["country"]["pk"])
                      {
                         if (!country_elements.includes(line["country"]["pk"]))
                         {
                           country_elements.push(line["country"]["pk"]);
                           groupsgraph.add({"id": line['country']['name'], "content": line['country']['name']});
                           country_pk = line["country"]["pk"]
                          }
                      }
            countries_data.push({"group":line['country']['name'], "x": line['date'], "y": line['cases_per_mio_seven'] })
        });

          var datasetgraph = new vis.DataSet(countries_data);
          var optionsgraph = {
                defaultGroup: "Country ",

                legend: {left:{position:"top-left"}},
          };
          var graph2dline = new vis.Graph2d(containergraph, datasetgraph, groupsgraph, optionsgraph);
          graph2dline.setGroups(groupsgraph)
        }


      $(window).on('load', function() {
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
                    name: '<font size="5em"><i class="'+line['code'] +' flag"/>'+line['name']+'</font>',
                    value: line['pk']
                  });
          });

          $('#countries_dd')
              .dropdown({
                values:countries
              })
            ;
      });

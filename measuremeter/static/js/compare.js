var config
var MONTHS
      $(window).on('load', function() {
       startdate = new Date(2020, 3, 24);
       enddate = new Date(2020,7,30);

       LoadData(4,startdate,enddate);
        	var ctx = document.getElementById('compareChart').getContext('2d');
			window.myLine = new Chart(ctx, config);
		});

      function formatDate(d)
        {
            var month = d.getMonth()+1;
            var day = d.getDate();

            var date = d.getFullYear() + '-' +
                (month<10 ? '0' : '') + month + '-' +
                (day<10 ? '0' : '') + day;
            return date;
        }

	 function LoadData(countries, startdate, endate)
      {

         lastdate_x = formatDate(endate);
          firstdate_x = formatDate(startdate);

          var data = $.ajax({
          url: "/measuremeterdata/casesdeaths/?country="+countries+"&date_after=2020-01-01&date_before="+lastdate_x,
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
                drawPoints: false,
                start: firstdate,
                end: lastdate

          };
          var graph2dline = new vis.Graph2d(containergraph, datasetgraph, groupsgraph, optionsgraph);
          graph2dline.setGroups(groupsgraph)

          populateExternalLegend(groupsgraph, "legendperpop", graph2dline)






        MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
		config = {
			type: 'line',
			data: {
				labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
				datasets: [{
					label: 'My First dataset',
					data: [
						10,12,57,43,22,56,78,12,33,56,
					],
					fill: false,
				}, {
					label: 'My Second dataset',
					fill: false,
					data: [
						90,76,44,3,23,22,11,23,23,34,55
					],
				}]
			},
			options: {
				responsive: true,
				title: {
					display: true,
					text: 'Chart.js Line Chart'
				},
				tooltips: {
					mode: 'index',
					intersect: false,
				},
				hover: {
					mode: 'nearest',
					intersect: true
				},
				scales: {
					x: {
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Month'
						}
					},
					y: {
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Value'
						}
					}
				}
			}
		};
      };

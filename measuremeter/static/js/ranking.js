var data
var mapDistricts
var geojson
var legend
var info
function applyCountryBorder(map, countryname) {
  jQuery
    .ajax({
      type: "GET",
      dataType: "json",
      url:
        "https://nominatim.openstreetmap.org/search?country=" +
        countryname.trim() +
        "&polygon_geojson=1&format=json"
    })
    .then(function(data) {
      /*const latLngs = L.GeoJSON.coordsToLatLngs(data[0].geojson.coordinates,2)
      L.polyline(latLngs, {
        color: "green",
        weight: 14,
        opacity: 1
      }).addTo(map);*/

      L.geoJSON(data[0].geojson, {
        color: "cyan",
        weight: 8,
        opacity: 1,
        fillOpacity: 0.0
      }).addTo(map);
    });
}

    function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }

    function LoadRanking()
    {

           datex = new Date();

            datefrom = addDays(datex, -11)
            datefrom_toload = formatDate(datefrom);
             date_toload = formatDate(datex);

                var data = $.ajax({
                  url: "/measuremeterdata/chcases/?date_after="+datefrom_toload.replace('-', '\-')+"&date_before="+date_toload.replace('-', '\-'),
                  dataType: "json",
                  async: false
                  }).responseText;
                  var jsonData = JSON.parse(data);

              var jsonData = JSON.parse(data);

                last_canton = -1

               jsonData.forEach(function (item, index) {


                    if (item.canton.level == 0 && item.canton.id != last_canton)
                    {
                        current_prev = item.cases_past14days
                        current_date = item.date
                        last_canton = item.canton.id

                    }

                });

    if (geojson)
    {
        map.removeLayer(geojson)
    }

    if (legend)
    {
        map.removeControl(legend);
     }

    if (info)
    {
        map.removeControl(info)
    }

        L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
            maxZoom: 18,
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
                '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
                'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            id: 'mapbox/light-v9',
            tileSize: 512,
            zoomOffset: -1
        }).addTo(map);


        // control that shows state info on hover
        info = L.control();

        info.onAdd = function (map) {
            this._div = L.DomUtil.create('div', 'info');
            this.update();
            return this._div;
        };


        info.update = function (props) {
            if (props)
            {
                var datestr = ''
                if (props.start != props.end)
                {
                    datestr = '<br />' + props.start + ' - ' + props.end
                }
                var commentstr = ''
                if (props.comment)
                {
                    commentstr = '<p>' + props.comment + '</p>';
                }
            }
            this._div.innerHTML = '' +  (props ?
                '<div align=left><p><b>' + props.name + '</b></p>' + datestr + commentstr+'</div>'
                : 'Hover over a state');
        };

        info.addTo(map);


        function getColor(d) {
            return  d > 120   ? '#060261' :
                    d > 90   ? '#0b03a8' :
                    d > 70   ? '#180df8' :
                    d > 50   ? '#3127fa' :
                    d > 30   ? '#483ff8' :
                    d > 20   ? '#665ff3' :
                    d > 15   ? '#847ef8' :
                    d > 10   ? '#a09cfa' :
                    d > 5   ? '#bab7ff' :
                    d > 0   ? '#ffffff' :
                    '#ffffff' ;

        }

        function style(feature) {
            return {
                weight: 2,
                opacity: 1,
                color: 'white',
                dashArray: '3',
                fillOpacity: 0.7,
                fillColor: getColor(feature.properties.level)
            };
        }

        function highlightFeature(e) {
            var layer = e.target;

            layer.setStyle({
                weight: 5,
                color: '#666',
                dashArray: '',
                fillOpacity: 0.7
            });

            if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
                layer.bringToFront();
            }

            info.update(layer.feature.properties);
        }

        function resetHighlight(e) {
            geojson.resetStyle(e.target);
            info.update();
        }

        function zoomToFeature(e) {
            map.fitBounds(e.target.getBounds());
        }

        var popup = L.popup();

        function onMapClick(e) {
            var datestr = ''
                if (e.sourceTarget.feature.properties.start != e.sourceTarget.feature.properties.end)
                {
                    datestr = '<br />' + e.sourceTarget.feature.properties.start + ' - ' + e.sourceTarget.feature.properties.end
                }
                var commentstr = ''
                if (e.sourceTarget.feature.properties.comment)
                {
                    commentstr = '<p>' + e.sourceTarget.feature.properties.comment + '</p>';
                }
            popup
                .setLatLng(e.latlng)
                .setContent('<div align=left><p><b>' + e.sourceTarget.feature.properties.name + '</b></p>' + datestr + commentstr+'</div>')
                .openOn(map);
        }

        function onEachFeature(feature, layer) {
            layer.on({
                mouseover: highlightFeature,
                mouseout: resetHighlight,
                click: onMapClick
            });
        }

        geojson = L.geoJson(statesData, {
            style: style,
            onEachFeature: onEachFeature
        }).addTo(map);

        map.attributionControl.addAttribution('Source: <a href="http://covidlaws.net/">covidlaws.net</a>');


        legend = L.control({position: 'bottomleft'});
        legend.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info legend');
        labels = ['<strong>Incidence</strong>'],
        categories = ["<5","<10","<15","<20","<30","<50","<70","<90","<120",">120"];
        categories_vals = [4,9,14,19,29,49,69,89,119,121];

        for (var i = 0; i < categories.length; i++) {

                div.innerHTML +=
                labels.push(
                    '<i class="circle" style="background:' + getColor(categories_vals[i]) + '"></i> ' +
                (categories[i] ? categories[i] : '+'));

            }
            div.innerHTML = labels.join('<br>');
        return div;
        };
        legend.addTo(map);

        map._onResize()


    }



        function addDays(date, days) {
          var result = new Date(date);
          result.setDate(result.getDate() + days);
          return result;
        }

      function formatDate(d)
        {
            var month = d.getMonth()+1;
            var day = d.getDate();

            var date = d.getFullYear() + '-' +
                (month<10 ? '0' : '') + month + '-' +
                (day<10 ? '0' : '') + day;
            return date;
        }



      $(window).on('load', function() {
            LoadRanking();
      });

var config;
var map
var geojson
var legend
var info

var data

    function LoadMap(map, datenow, groupsize, bias, days)
    {

          statesData = $.extend( true, {}, statesDataOrig );

          datefrom = addDays(datenow, -7)

          var data = $.ajax({
          url: "/measuremeterdata/chcases/?date_after="+formatDate(datefrom).replace('-', '\-')+"&date_before="+datenow.replace('-', '\-'),
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

        var row = new Array()
        old_date = new Date(2020, 1, 1);

        canton_pk = -1

        var dataset = new Array()
        var dataset_data = new Array()
        var label_array = new Array()

        date_isfilled = false

               jsonData.forEach(function (item, index) {
                    if (item.canton.level == 0)
                    {
                        var id = statesData['features'].findIndex(x => x.id === item.canton.code.toUpperCase());
                        if (id > -1)
                        {
                            if (days == 7)
                            {
                                value_cases = item.incidence_past7days
                            }
                            else if (days == 10)
                            {
                                value_cases = item.incidence_past10days
                            }
                            else if (days == 14)
                            {
                                value_cases = item.incidence_past14days
                            }


                            value_risk = 100 - (((1-(1/(100000/(value_cases*bias)))) ** groupsize) * 100)
                            statesData.features[id].properties.level = value_risk
                            statesData.features[id].properties.comment = value_cases
                            statesData.features[id].properties.date = item.date
                        }
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
            this._div.innerHTML = '' +  (props ?
                '<div align=left><b>' + props.NAME + '</b><br>' + props.level.toFixed(1) + ' %</div>'
                : 'Hover over a state');
        };

        info.addTo(map);

                function getColor(d) {
            return  d > 90   ? '#060261' :
                    d > 80   ? '#0b03a8' :
                    d > 70   ? '#180df8' :
                    d > 60   ? '#3127fa' :
                    d > 50   ? '#483ff8' :
                    d > 40   ? '#665ff3' :
                    d > 30   ? '#847ef8' :
                    d > 20   ? '#a09cfa' :
                    d > 10   ? '#bab7ff' :
                    d > 0   ? '#c1bfff' :
                    '#aeaeae' ;
                    }


        function style(feature) {
            return {
                weight: 2,
                opacity: 1,
                color: 'white',
                dashArray: '3',
                fillOpacity: 1,
                fillColor: getColor(feature.properties.level)
            };
        }

        function highlightFeature(e) {
            var layer = e.target;

            layer.setStyle({
                weight: 5,
                color: '#666',
                dashArray: '',
                fillOpacity: 1
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
                var commentstr = ''
                if (e.sourceTarget.feature.properties.comment)
                {
                    commentstr = '<p>Cases/100k pop past ' + days + "days:<br>" + e.sourceTarget.feature.properties.comment + '<br>(' + e.sourceTarget.feature.properties.date +')</p>';
                }
                var levelstr = ''
                if (e.sourceTarget.feature.properties.level)
                {
                    levelstr = '<p>Risk: ' + e.sourceTarget.feature.properties.level.toFixed(1) + '%</p>';
                }
                popup
                .setLatLng(e.latlng)
                .setContent('<div align=left><p><b>' + e.sourceTarget.feature.properties.NAME + '</b>' + levelstr + commentstr+'</p></div>')
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
        labels = ['<strong>Risk</strong>'],
        categories = ["<10%","<20%","<30%","<40%","<50%","<60%","<70%","<80%","<90%","<100%"];

        for (var i = 0; i < categories.length; i++) {

                div.innerHTML +=
                labels.push(
                    '<i class="circle" style="background:' + getColor((i+1)*10-1) + '"></i> ' +
                (categories[i] ? categories[i] : '+'));

            }
            div.innerHTML = labels.join('<br>');
        return div;
        };
        legend.addTo(map);

        map._onResize()


    }

      $(window).on('load', function() {



		    $("#load_data").click(function(){
                groupsize = $("#groupsize").val();
                bias = $("#bias").val();
                days = $("#days").val();

                var d = new Date();
                today = formatDate(d);
                LoadMap(mapRisk, today, groupsize, bias, days);
            });

            $('.ui.dropdown')
              .dropdown();

            $('#days_dd').dropdown('set selected', 7)

            var mapRisk = L.map('mapRisk').setView([46.8, 8.4], 8);

            groupsize = $("#groupsize").val();
            bias = $("#bias").val();
            days = $("#days").val();

            var d = new Date();
            today = formatDate(addDays(d, -1));
            LoadMap(mapRisk, today, groupsize, bias, days);

      });

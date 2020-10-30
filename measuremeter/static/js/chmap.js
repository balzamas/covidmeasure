var config;
var data

    function LoadMap(map, measuretype)
    {
              statesData = $.extend( true, {}, statesDataOrig );

              var jsonData = JSON.parse(data);

               jsonData.forEach(function (item, index) {
                    if (item.type.pk == measuretype)
                    {
                        var id = statesData['features'].findIndex(x => x.id === item.canton.code.toUpperCase());
                        if (id > -1)
                        {
                            statesData.features[id].properties.level = item.level;
                            statesData.features[id].properties.comment = item.comment;

                            if (item.start != null)
                              {
                                var start_date_str = item.start
                              }
                              else
                              {
                                var start_date_str = 'undefined'
                              }

                              if (item.end != null)
                              {
                                var end_date_str = item.end
                              }
                              else
                              {
                                var end_date_str = 'undefined'
                              }
                              statesData.features[id].properties.start = start_date_str;
                              statesData.features[id].properties.end = end_date_str;

                        }
                    }
                });

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
        var info = L.control();

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
                '<div align=left><b>' + props.NAME + '</b>' + datestr + commentstr+'</div>'
                : gettext('Hover over a state'));
        };

        info.addTo(map);


        // get color depending on population density value
        function getColor(d) {
            return  d > 2   ? '#060261' :
                    d > 1   ? '#3127fa' :
                    d > 0   ? '#847ef8' :
                    d > -1   ? '#bab7ff' :
                              '#ffffff';
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
                .setContent('<div align=left><b>' + e.sourceTarget.feature.properties.NAME + '</b>' + datestr + commentstr+'</div>')
                .openOn(map);
        }

        function onEachFeature(feature, layer) {
            layer.on({
                mouseover: highlightFeature,
                mouseout: resetHighlight,
                click: onMapClick
            });
        }

        var geojson = L.geoJson(statesData, {
            style: style,
            onEachFeature: onEachFeature
        }).addTo(map);

        map.attributionControl.addAttribution('Source: <a href="http://covidlaws.net/">covidlaws.net</a>');


        var legend = L.control({position: 'bottomleft'});
        legend.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info legend');
        labels = ['<strong>Level</strong>'],
        categories = ["CH","+1","+2","+3","+4"];

        for (var i = 0; i < categories.length; i++) {

                div.innerHTML +=
                labels.push(
                    '<i class="circle" style="background:' + getColor(i-1) + '"></i> ' +
                (categories[i] ? categories[i] : '+'));

            }
            div.innerHTML = labels.join('<br>');
        return div;
        };
        legend.addTo(map);

        map._onResize()


    }

     function FormatPopUp(line, last_line)
     {
        var tendency = "&#11014;"

        if (last_line)
        {

            if (last_line['canton']['pk'] == line['canton']['pk'] && last_line['type']['pk'] == line['type']['pk'])
            {
               if (last_line['level'] > line['level'])
               {
                tendency = "&#11015;"
               }
               else if (last_line['level'] == line['level'])
               {
                tendency = "&#10145;"
               }
               else if (last_line['level'] < line['level'])
               {
                tendency = "&#11014;"
               }
               }

        }
                            str_level = '<i class="green '+line["type"]["icon"] +'" data-tooltip="None"></i>'

                            if (line['level'] == 1)
                            {
                                str_level =  '<i class="yellow '+line["type"]["icon"] +'" data-tooltip="'+line["type"]["tooltip_partial"]+'"></i>'
                            }
                            else if (line['level'] == 2)
                            {
                                str_level =  '<i class="orange '+line["type"]["icon"] +'" data-tooltip="'+line["type"]["tooltip_nonpartial"]+'"></i>'
                            }
                            else if (line['level'] == 3)
                            {
                                str_level =  '<i class="red '+line["type"]["icon"] +'" data-tooltip="'+line["type"]["tooltip_nonpartial"]+'"></i>'
                            }
                            else if (line['level'] == 4)
                            {
                                str_level =  '<i class="red '+line["type"]["icon"] +'" data-tooltip="'+line["type"]["tooltip_nonpartial"]+'"></i>'
                            }

                            endtime = gettext('Undefined')
                            if (line['end'] != null)
                            {
                                endtime = line['end'];
                            }

                            htmlLine = '<p>'+ line['canton']['name'] + "  "+ str_level+ tendency+"<br>"+line["type"]["name"] +'<br>Level: '+ (line['level'] +1) +', End: '+endtime+"<br>"+line["comment"]+"</p>";

         return htmlLine;
     }


      function LoadCantonData()
      {
          var data = $.ajax({
          url: "/measuremeterdata/chcantons/",
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

          LoadMeasures();
      }

      function LoadMeasures()
      {
            var d = new Date();
            today = formatDate(d);


          data = $.ajax({
          url: "/measuremeterdata/chmeasures/?start="+today.replace('-', '\-')+"&end="+today.replace('-', '\-'),
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

      }

      $(window).on('load', function() {
            $('#dimmer').dimmer('show');

            $('.ui.accordion')
                 .accordion()
            ;

            $('#param').hide();

            LoadCantonData();

            var mapSecondary = L.map('mapSecondary').setView([46.8, 8.4], 8);
            LoadMap(mapSecondary, 6);

            var mapDisco = L.map('mapDisco').setView([46.8, 8.4], 8);
            LoadMap(mapDisco, 3);

            var mapMasks = L.map('mapMasks').setView([46.8, 8.4], 8);
            LoadMap(mapMasks, 2);

            var mapRestaurants = L.map('mapRestaurants').setView([46.8, 8.4], 8);
            LoadMap(mapRestaurants, 4);

			$('#dimmer').dimmer('hide');

      });

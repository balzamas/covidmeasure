var current_date = new Date();
var config;


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
        color: "yellow",
        weight: 8,
        opacity: 1,
        fillOpacity: 0.0
      }).addTo(map);
    });
}

    function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }

    function LoadMap(map, date)
    {
              statesData = $.extend( true, {}, statesDataOrig );

            datefrom = addDays(date, -11)
            datefrom_toload = formatDate(datefrom);
             date_toload = formatDate(date);

                var data = $.ajax({
                  url: "/measuremeterdata/chcases/?date_after="+datefrom_toload.replace('-', '\-')+"&date_before="+date_toload.replace('-', '\-'),
                  dataType: "json",
                  async: false
                  }).responseText;
                  var jsonData = JSON.parse(data);

              var jsonData = JSON.parse(data);

               jsonData.forEach(function (item, index) {


                    if (item.canton.level == 0)
                    {
                        id = statesData['features'].findIndex(x => x.id === item.canton.code.toUpperCase());
                        if (id > -1)
                            {
                                statesData.features[id].properties.level = item.incidence_past14days;
                                statesData.features[id].properties.name = item.canton.name;
                                statesData.features[id].properties.comment = "<div align='center'><p>"+item.incidence_past14days +'</p><p>' + gettext('Population') + ':<br>' + item.canton.population.toLocaleString('ch-CH') + '<br>' + gettext('Last update') + ':<br>' + item.date+'</div><br><img src="/static/images/graphs_ch/'+ item.canton.code +'_14.png"><br>' + gettext('Development past 2 months.') + '</p>';
                                statesData.features[id].properties.code = item.canton.code + "_14"
                                statesData.features[id].properties.weekoverweek = item.development7to7

                            }
                    }
                    else if (item.canton.level == 1)
                    {
                        id = statesData['features'].findIndex(x => x.properties["BEZIRKSNUM"] === item.canton.swisstopo_id);
                        if (id > -1)
                            {
                                if (item.canton.name.includes("(D)") || item.canton.name.includes("(A)") || item.canton.name.includes("(I)") || item.canton.name.includes("(F)"))
                                    {
                                        statesData.features[id].properties.is_not_ch = true
                                    }
                                   else
                                   {
                                      statesData.features[id].properties.is_not_ch = false

                                   }
                                if (item.incidence_past14days != null)
                                {
                                    statesData.features[id].properties.level = item.incidence_past14days;
                                    statesData.features[id].properties.name = item.canton.name;
                                    statesData.features[id].properties.weekoverweek = item.development7to7
                                    statesData.features[id].properties.comment = "<div align='center'><p>"+item.incidence_past14days +'</p><p>' + gettext('Population') + ':<br>' + item.canton.population.toLocaleString('ch-CH') + '<br>' + gettext('Last update') + ':<br>' + item.date+'</div><br><img src="/static/images/graphs_ch/'+ item.canton.swisstopo_id +'_14.png"><br>' + gettext('Development past 2 months.') + '</p>';
                                    statesData.features[id].properties.code = item.canton.swisstopo_id + "_14"
                                }
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
                '<div align=center><p><b>' + props.name + '</b></p>' + datestr  + commentstr+ "Entwicklung Fälle<br>Woche/Vorwoche:<br> "+props.weekoverweek+'%</div>'
                : gettext('Hover over a state'));
        };

        info.addTo(map);

        function getColor(d) {
            console.log("hans2")
            return  d > 1000 ? '#000000' :
                    d > 500 ? '#420423' :
                    d > 350 ? '#5f0332' :
                    d > 250 ? '#BF0060' :
                    d > 160   ? '#ff0000' :
                    d > 140   ? '#fb5f5f' :
                    d > 120   ? '#fb8c8c' :
                    d > 100   ? '#ff8916' :
                    d > 80   ? '#ffb56c' :
                    d > 60   ? '#fed1a4' :
                    d > 40   ? '#7aa6fe' :
                    d > 20   ? '#9cbdff' :
                    d > 5   ? '#abc7ff' :
                    d > 0   ? '#d3e1fe' :
                    '#ffffff' ;

        }

        function style(feature) {
             if (feature.properties.is_not_ch)
                {
                    var myPattern = new L.StripePattern({angle:  0,      weight:  7,      color:  getColor(feature.properties.level),      opacity:  1,});
                    myPattern.addTo(map);

                    myPattern.color = 'red'
                    return {
                        weight: 2,
                        opacity: 1,
                        color: 'white',
                        dashArray: '3',
                        fillOpacity: 0.7,
                        fillColor: getColor(feature.properties.level),
                        fillPattern: myPattern, fillOpacity: 0.7,
                    };
                }
                else
                {
                    fillOpacity= 1
                }
            return {
                weight: 2,
                opacity: 1,
                color: 'white',
                dashArray: '3',
                fillOpacity: fillOpacity,
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
                .setContent('<div align=center><p><b>' + e.sourceTarget.feature.properties.name + '</b></p>' + datestr + commentstr+"Entwicklung Fälle<br>Woche/Vorwoche:<br> "+e.sourceTarget.feature.properties.weekoverweek+'%</div>')
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
    //    categories = ["<5","<10","<15","<20","<30","<50","<70","<90","<120","<150",">150"];
    //    categories_vals = [4,9,14,19,29,49,69,89,119,121,151];
        categories = ["<5","<20","<40","<60","<80","<100","<120","<140","<160","<250","<350","<500","<1000",">1000"];
        categories_vals = [4,19,39,59,79,99,119,139,159,161,251,351,501,1001];

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

      function MoveFocus(value)
      {
                    date = addDays(current_date, value);
                    LoadMap(mapDistricts,date);
                    document.getElementById('dateview').innerHTML = formatDate(date);
                    current_date = date;
      }

      $(window).on('load', function() {
                $("#btnPlusDay").click(async function(){
                    MoveFocus(1)
                });

                $("#btnMinusDay").click(async function(){
                    MoveFocus(-1)
                });
                $("#btnPlusWeek").click(async function(){
                    MoveFocus(7)

                });

                $("#btnMinusWeek").click(async function(){
                    MoveFocus(-7)
                });


                $("#btnPlayBegin").click(async function(){
                date = new Date(2020,1,24);
                enddate = new Date();

                while (date < enddate)
                {
                        LoadMap(mapDistricts,date);
                        document.getElementById('dateview').innerHTML = formatDate(date);
                        await sleep(4);
                        date = addDays(date, 7);
                }
          });
                $("#btnPlayJune").click(async function(){
                date = new Date(2020,5,15);
                enddate = new Date();

                while (date < enddate)
                {
                        LoadMap(mapDistricts,date);
                        await sleep(4);
                        document.getElementById('dateview').innerHTML = formatDate(date);
                        date = addDays(date, 7);
                }
          });
                $("#btnPlaySept").click(async function(){
                date = new Date(2020,8,6);
                enddate = new Date();

                while (date < enddate)
                {
                        LoadMap(mapDistricts,date);
                        await sleep(4);
                        document.getElementById('dateview').innerHTML = formatDate(date);
                        date = addDays(date, 7);
                }
          });
                                    $("#btnPlayJan").click(async function(){
                date = new Date(2021,0,1);
                enddate = new Date();

                while (date < enddate)
                {
                        LoadMap(mapDistricts,date);
                        await sleep(6);
                        document.getElementById('dateview').innerHTML = formatDate(date);
                        date = addDays(date, 7);
                }
          });

            real_enddate = new Date();

            mapDistricts = L.map('mapDistricts').setView([46.8, 8.4], 8);
            //applyCountryBorder(mapDistricts, "Switzerland");
            LoadMap(mapDistricts, real_enddate);

      });

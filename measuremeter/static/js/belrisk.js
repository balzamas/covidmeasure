var config;
var map
var geojson
var legend
var info

var data
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

    function AddRow(province,age_groups, bias, groupsize,days, age_dist_obj)
    {
      var table = document.getElementById("riskTable");


      var row = table.insertRow(-1);
      var cell1 = row.insertCell(0);
      cell1.innerHTML = province.name;
      for ( var property in age_dist_obj ) {
            if (days == 7)
            {
                value_cases_tbl = province.cases7[property];
            }
            else if (days == 10)
            {
                value_cases_tbl = province.cases10[property];
            }
            else if (days == 14)
            {
                value_cases_tbl = province.cases14[property];
            }

            pop_agegroups_tbl = age_dist_obj[property]
            pop_agegroups_province_tbl = province.population * pop_agegroups_tbl / age_dist_obj["Total"]
            incidence_tbl = 100000 * value_cases_tbl / pop_agegroups_province_tbl

            value_risk_tbl = 100 - (((1-(1/(100000/(incidence_tbl*bias)))) ** groupsize) * 100)
            var cell = row.insertCell(-1);
            cell.innerHTML = "<div style='background-color:"+getColor(value_risk_tbl)+";padding-left:15px;padding-top:5px;padding-bottom:5px;'><b> " + value_risk_tbl.toFixed(1) + "%</b></div>" ;

      }
    }

    function LoadMap(map, datenow, groupsize, bias, days, provinces, age_dist, age_groups)
    {
           if (age_groups == undefined || age_groups == '')
           {
               age_groups_array = undefined
           }
           else
           {
               age_groups_array = age_groups.split(",")
           }

           var table = document.getElementById("riskTable");

           if (table.rows.length > 1)
           {
               for (var i = 1; i < 12; i++)
               {
                    table.deleteRow(-1)
               }
           }



           provinces_clean=provinces.replace(/&#x27;/g, '"');
           age_dist_clean=age_dist.replace(/&#x27;/g, '"');
           var provinces_obj = JSON.parse(provinces_clean);
           var age_dist_obj = JSON.parse(age_dist_clean);


           statesData = $.extend( true, {}, statesDataOrig );

           provinces_obj.forEach(function (item, index) {
                        var id = statesData['features'].findIndex(x => x.properties["HASC_1"] === item.hasc);
                        if (id > -1)
                        {
                            value_cases = 0
                            pop_agegroups = 0
                            if (days == 7)
                            {
                                if (age_groups == '')
                                {
                                    value_cases = item.cases7["Total"]
                                    pop_agegroups = age_dist_obj["Total"]
                                }
                                else
                                {
                                    for (i = 0; i < age_groups_array.length; i++) {
                                        value_cases += item.cases7[age_groups_array[i]];
                                        pop_agegroups += age_dist_obj[age_groups_array[i]]
                                    }
                                }
                            }
                            else if (days == 10)
                            {
                                if (age_groups == '')
                                {
                                    value_cases = item.cases10["Total"]
                                    pop_agegroups = age_dist_obj["Total"]
                                }
                                else
                                {
                                    for (i = 0; i < age_groups_array.length; i++) {
                                        value_cases += item.cases10[age_groups_array[i]];
                                        pop_agegroups += age_dist_obj[age_groups_array[i]]
                                    }
                                }
                            }
                            else if (days == 14)
                            {
                                if (age_groups == '')
                                {
                                    value_cases = item.cases14["Total"]
                                    pop_agegroups = age_dist_obj["Total"]
                                }
                                else
                                {
                                    for (i = 0; i < age_groups_array.length; i++) {
                                        value_cases += item.cases14[age_groups_array[i]];
                                        pop_agegroups += age_dist_obj[age_groups_array[i]]
                                    }
                                }
                            }

                            pop_agegroups_province = item.population * pop_agegroups / age_dist_obj["Total"]

                            incidence = 100000 * value_cases / pop_agegroups_province

                            AddRow(item, age_groups, bias, groupsize, days, age_dist_obj)

                            value_risk = 100 - (((1-(1/(100000/(incidence*bias)))) ** groupsize) * 100)

                            statesData.features[id].properties.level = value_risk
                            statesData.features[id].properties.comment = incidence
                        }

           });



          datefrom = addDays(datenow, -7)


        var row = new Array()
        old_date = new Date(2020, 1, 1);

        canton_pk = -1

        var dataset = new Array()
        var dataset_data = new Array()
        var label_array = new Array()

        date_isfilled = false

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
                '<div align=left><b>' + props.NAME_1 + '</b><br>'+gettext('Risk') +': ' + props.level.toFixed(1) + ' %<br>Incidence: ' + props.comment.toFixed(1) + '</div>'
                : gettext('Hover over a state'));
        };

        info.addTo(map);




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
                var commentstr = ''
                if (e.sourceTarget.feature.properties.comment)
                {
                    commentstr = '<p>'+gettext('Cases/100k pop past ') + days + gettext('days')+":<br>" + e.sourceTarget.feature.properties.comment.toFixed(1) + '</p>';
                }
                var levelstr = ''
                if (e.sourceTarget.feature.properties.level)
                {
                    levelstr = '<p>'+gettext('Risk')+': ' + e.sourceTarget.feature.properties.level.toFixed(1) + '%</p>';
                }
                popup
                .setLatLng(e.latlng)
                .setContent('<div align=left><p><b>' + e.sourceTarget.feature.properties.NAME_1 + '</b>' + levelstr + commentstr+'</p></div>')
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
        labels = ['<strong>'+gettext('Risk')+'</strong>'],
        labels = ['<strong>'+gettext('Risk')+'</strong>'],
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



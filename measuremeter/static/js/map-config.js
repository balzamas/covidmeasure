
var map
var geojson
var legend
var info

function readloadDate()
{
                var measuretype = $('#measurechooser').dropdown('get value');
                var seldate = document.getElementById("dateselect").value;

                loadMapData(measuretype,seldate);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

$( document ).ready(function() {
            map = L.map('map').setView([52, 12], 4);

          var dataMeasuresTypes = $.ajax({
          url: "/measuremeterdata/oxfordmeasuretypes/",
          dataType: "json",
          async: false
          }).responseText;

          var jsonMeasuresTypes = JSON.parse(dataMeasuresTypes);

          measuretypes = []

          $.each(jsonMeasuresTypes, function(id, line) {
                 measuretypes.push({
                    name: '<font size="5em">'+line['name']+'</font>',
                    value: line['pk']
                  });
          });

          $('#measurechooser')
              .dropdown({
                values:measuretypes
              })
            ;

            $('#dateselect').change(function() {
                           readloadDate();
            });

           $("#measurechooser").change(function() {
               readloadDate();
            });

          $("#btnPlusDays").click(function(){
                var measuretype = $('#measurechooser').dropdown('get value');

                var seldate = document.getElementById("dateselect").value;

                nextdate = addDays(seldate, 3);

                nextdate_f = formatDate(nextdate);

                document.getElementById("dateselect").value = nextdate_f;
                loadMapData(measuretype,nextdate_f);
          });

          $("#btnMinusDays").click(function(){
                var measuretype = $('#measurechooser').dropdown('get value');

                var seldate = document.getElementById("dateselect").value;

                nextdate = addDays(seldate, -3);

                nextdate_f = formatDate(nextdate);

                document.getElementById("dateselect").value = nextdate_f;
                loadMapData(measuretype,nextdate_f);
          });

          $("#btnPlay").click(async function(){
                var measuretype = $('#measurechooser').dropdown('get value');

                date = new Date(2020,2,5);
                enddate_x = new Date();
                enddate = addDays(enddate_x, 3);

                while (date < enddate)
                {
                        date_f = formatDate(date);
                        loadMapData(measuretype,date_f);
                        await sleep(100);
                        date = addDays(date, 2);
                }
          });
          $("#btnPlay2").click(async function(){
                var measuretype = $('#measurechooser').dropdown('get value');

                date = new Date(2020,8,10);
                enddate_x = new Date();
                enddate = addDays(enddate_x, 3);

                while (date < enddate)
                {
                        date_f = formatDate(date);
                        loadMapData(measuretype,date_f);
                        await sleep(100);
                        date = addDays(date, 2);
                }
          });

          $("#btnCopyLink").click(async function(){
                copyToClipboard("/euromap/" + $('#measurechooser').dropdown('get value'));
          });

             var d = new Date();

            today = formatDate(d);
            document.getElementById("dateselect").value = today;

            $('#param').hide();
            if ($('#param').text() != '')
            {
                $('#measurechooser').dropdown('set selected',$('#param').text());
                loadMapData($('#param').text(),today);
            }
            else
            {
                $('#measurechooser').dropdown('set selected',2);
                loadMapData(26,today);
            }
});

function loadMapData(measuretype,filterdate) {

          statesData = $.extend( true, {}, statesDataOrig );

          var dataMeasuresType = $.ajax({
          url: "/measuremeterdata/oxfordmeasuretypes/?pk="+measuretype,
          dataType: "json",
          async: false
          }).responseText;
          var jsonMeasuresType = JSON.parse(dataMeasuresType);

            document.getElementById('chosen_options').innerHTML = jsonMeasuresType[0]['name'] + ' // ' + filterdate;
/*----------------------------------------------------------------------------------*/

          var data = $.ajax({
          url: "/measuremeterdata/oxfordmeasures/?type="+measuretype.toString()+"&start="+filterdate.replace('-', '\-')+"&end="+filterdate.replace('-', '\-'),
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

           jsonData.forEach(function (item, index) {
                var id = statesData['features'].findIndex(x => x.properties.iso_a2 === item.country.code.toUpperCase());
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
			'<div align=left><b>' + props.name + '</b>' + datestr + commentstr+'</div>'
			: 'Hover over a state');
	};

	info.addTo(map);


	function getColor(d) {
		return  d > 3   ? '#FED711' :
		        d > 2   ? '#FEEE00' :
		        d > 1   ? '#FE0000' :
				d > 0   ? '#FED341' :
				d > -1   ? '#00ff80' :
						  '#dfdcdc';
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
        console.log(e.sourceTarget.feature.properties.name);
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
            .setContent('<div align=left><b>' + e.sourceTarget.feature.properties.name + '</b>' + datestr + commentstr+'</div>')
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
    labels = ['<strong>'+ jsonMeasuresType[0]['name'] +'</strong>'],
    categories = ['Unknown',jsonMeasuresType[0]['text_level0'],jsonMeasuresType[0]['text_level1'],jsonMeasuresType[0]['text_level2'], jsonMeasuresType[0]['text_level3'], jsonMeasuresType[0]['text_level4']];

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

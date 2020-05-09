var eujsconfig ="";
loadMapData(1,'2020-05-06');

function loadMapData(measuretype,filterdate) {
eujsconfig = {
  "eujs1":{
    "hover": "ALBANIA",//info of the popup
    "upColor": "#d5d5d5",//default color
    "overColor": "#ECFFB3",//highlight color
    "downColor": "#cae9af",//clicking color
    "active": false//true/false to activate/deactivate
  },
  "eujs2":{
    "hover": "ANDORRA",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs3":{
    "hover": "AUSTRIA",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs4":{
    "hover": "BELARUS",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs5":{
    "hover": "BELGIUM",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs6":{
    "hover": "BOSNIA AND HERZEGOVINA",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs7":{
    "hover": "BULGARIA",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs8":{
    "hover": "CROATIA",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs9":{
    "hover": "CYPRUS",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs10":{
    "hover": "CZECH REPUBLIC",
    "url": "https://www.html5interactivemaps.com/", "target": "same_window",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs11":{
    "hover": "DENMARK",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs12":{
    "hover": "ESTONIA",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs13":{
    "hover": "FINLAND",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs14":{
    "hover": "FRANCE",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs15":{
    "hover": "GERMANY",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs16":{
    "hover": "GREECE",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs17":{
    "hover": "HUNGARY",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs18":{
    "hover": "ICELAND",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs19":{
    "hover": "IRELAND",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs20":{
    "hover": "ITALY",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs21":{
    "hover": "KOSOVO",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs22":{
    "hover": "LATVIA",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs23":{
    "hover": "LIECHTENSTEIN",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs24":{
    "hover": "LITHUANIA",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs25":{
    "hover": "LUXEMBOURG",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs26":{
    "hover": "MACEDONIA",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs27":{
    "hover": "MALTA",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs28":{
    "hover": "MOLDOVA",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs29":{
    "hover": "MONACO",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs30":{
    "hover": "MONTENEGRO",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs31":{
    "hover": "NETHERLANDS",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs32":{
    "hover": "NORWAY",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs33":{
    "hover": "POLAND",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs34":{
    "hover": "PORTUGAL",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs35":{
    "hover": "ROMANIA",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs36":{
    "hover": "RUSSIA",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs37":{
    "hover": "SAN MARINO",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs38":{
    "hover": "SERBIA",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs39":{
    "hover": "SLOVAKIA",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs40":{
    "hover": "SLOVENIA",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs41":{
    "hover": "SPAIN",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs42":{
    "hover": "SWEDEN",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs43":{
    "hover": "SWITZERLAND",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs44":{
    "hover": "UKRAINE",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs45":{
    "hover": "UNITED KINGDOM",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "eujs46":{
    "hover": "VATICAN CITY",
    "upColor": "#d5d5d5", "overColor": "#ECFFB3", "downColor": "#cae9af",
    "active": false
  },
  "general":{
    "borderColor": "#9CA8B6",
    "visibleNames": "#adadad"
  }
};


/*----------------------------------------------------------------------------------*/

          var data = $.ajax({
          url: window.location.href + "../measuremeterdata/measures/?type="+measuretype.toString()+"&start="+filterdate.replace('-', '\-')+"&end="+filterdate.replace('-', '\-'),
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);


          var fullcolor="#c54e35";
          var fullcolorhover ="#e5573a";

          var partcolor="#d3bb33";
          var partcolorhover="#f5da3c";

        $.each(jsonData, function(id, line) {
          console.log(line['country']['name']);
          if (line['start'] != null)
          {
            var start_date_str = line['start']
          }
          else
          {
            var start_date_str = 'undefined'
          }


          if (line['end'] != null)
          {
            var end_date_str = line['end']
          }
          else
          {
            var end_date_str = 'undefined'
          }

          var color_norm = ''
          var color_hover= ''

          if (line['partial'] == true)
          {
             color_norm = partcolor
             color_hover= partcolorhover
          }
          else
          {
             color_norm = fullcolor
             color_hover= fullcolorhover
          }

          var tooltip = '<div style="margin-left: 5;margin-top: 5;margin-bottom: 5;margin-right: 5;width: 300">'
          tooltip += "<p><b>"+line['country']['name']+"</b></p>";
          if (line['none'] == false)
          {
            tooltip += "<p>"+ start_date_str + " - " + end_date_str + " </p>";
          }
          tooltip += "<hr>";
          tooltip += line['comment'].toString();
          tooltip += '</div>';

            eujsconfig[line['country']['mapcode_europe']]['hover'] = tooltip;
            /*eujsconfig[line['country']['mapcode_europe']]['url'] = 'XXXXX';
            eujsconfig[line['country']['mapcode_europe']]['target'] = 'XXXXX';*/
            eujsconfig[line['country']['mapcode_europe']]['upColor'] = color_norm;
            eujsconfig[line['country']['mapcode_europe']]['overColor'] = color_hover;
            /*eujsconfig[line['country']['mapcode_europe']]['downColor'] = partcolor;*/
            eujsconfig[line['country']['mapcode_europe']]['active'] = true;
          }
        );



}

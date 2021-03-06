     function FormatPopUp(line)
     {
                            str_level = '<i class="green '+line["type"]["icon"] +'" data-tooltip="None"></i>'
                            status = "None"

                            if (line['level'] == 0)
                            {
                                status = line['level']
                                str_level =  '<i class="yellow '+line["type"]["icon"] +'" data-tooltip="'+line["type"]["text_level0"]+'"></i>'
                            }
                            if (line['level'] == 1)
                            {
                                status = line['level']
                                str_level =  '<i class="yellow '+line["type"]["icon"] +'" data-tooltip="'+line["type"]["text_level1"]+'"></i>'
                            }
                            else if (line['level'] == 2)
                            {
                                status = line['level']
                                str_level =  '<i class="red '+line["type"]["icon"] +'" data-tooltip="'+line["type"]["text_level2"]+'"></i>'
                            }
                            else if (line['level'] == 3)
                            {
                                status = line['level']
                                str_level =  '<i class="red '+line["type"]["icon"] +'" data-tooltip="'+line["type"]["text_level3"]+'"></i>'
                            }
                            else if (line['level'] == 4)
                            {
                                status = line['level']
                                str_level =  '<i class="red '+line["type"]["icon"] +'" data-tooltip="'+line["type"]["text_level4"]+'"></i>'
                            }

                            endtime = "Undefined"
                            if (line['end'] != null)
                            {
                                endtime = line['end'];
                            }

                          if (line['level'] < line['last_level'])
                           {
                            tendency = "&#11015;"
                           }
                           else if (line['level'] == line['last_level'])
                           {
                            tendency = "&#10145;"
                           }
                           else if (line['level'] > line['last_level'])
                           {
                            tendency = "&#11014;"
                           }

                            source=""
                           if (line['source'] != '')
                           {
                                source = '<p><a href="'+line['source']+'">Source</a></p>'
                           }

                            htmlLine = '<p><i class="'+line['country']['code'] +' flag"/>'+ line['country']['name'] + "  "+ str_level+ tendency +'<br>Measure: '+line["type"]["name"]+'<br>Level: '+status +'<br>End: '+endtime+"<br>"+line["comment"]+source+"</p>";

         return htmlLine;
     }


     function LoadMeasure(countries, measuretypes, startdate, enddate)
     {

           if (countries == undefined)
             {
               //Startup: set random country
               rnd_country = Math.floor(Math.random() * 43) + 1;
               rnd_country2 = Math.floor(Math.random() * 43) + 1;
               rnd_country3 = Math.floor(Math.random() * 43) + 1;

               countries=rnd_country.toString()+","+rnd_country2.toString()+","+rnd_country3.toString();
             }


          var data = $.ajax({
          url: "/measuremeterdata/oxfordmeasures/?country="+countries+"&type="+measuretypes,
          dataType: "json",
          async: false
          }).responseText;
          var jsonData = JSON.parse(data);

        annotations_prepare = new Array()
        annotations = new Array()

        $.each(jsonData, function(id, line) {
            if (line['start'] != null)
            {
                doesexist = false;
                let obj = annotations_prepare.find((o, i) => {
                    if (o.value === line['start']) {
                        if (o.label.includes(line["country"]["code"]))
                        {
                           codes = annotations_prepare[i]["label"]
                        }
                        else
                        {
                           codes = annotations_prepare[i]["label"] + ", " + line["country"]["code"]
                        }

                        popUp = annotations_prepare[i]["popup"] + "<br>" + FormatPopUp(line);

                        annotations_prepare[i] = { label: codes, value: line['start'], popup: popUp };
                        doesexist = true;
                        return true; // stop searching
                    }
                });

                if (!doesexist)
                {
                    annotations_prepare.push(
                        {
                            value: line['start'],
                            label: line["country"]["code"],
                            popup: FormatPopUp(line)
                        }
                    );
                }
            }
            });

            annotations_prepare.forEach(function(element)
                {
                    annotations.push(
                        {
                            drawTime: "afterDatasetsDraw",
                            type: "line",
                            mode: "vertical",
                            scaleID: "x-axis-0",
                            value: element.value,
                            borderColor: "black",
                            borderWidth: 2,
                            label: {
                                backgroundColor: "#5d5d5d",
                                content: element.label,
                                rotation: 270,
                                enabled: true,
                                fontSize: 19
                            },

                        onClick: function(e) {
                        // The annotation is is bound to the `this` variable
                            $("#dialog").html('<div style="margin-left: 10;margin-top: 10;margin-right: 10;margin-bottom: 10;max-height: 800;">' + element.popup + '</div>');
                            $('#dialog').dialog({
                              title: "Introduced measures " + element.value,
                              open: function (event, ui) {
                                    $('.ui-widget-overlay').bind('click', function () {
                                    $("#dialog").dialog('close');
                                    });
                                }
                            }).dialog('open');
                        },
                        }

                    )
                }
            )

        return annotations
     }

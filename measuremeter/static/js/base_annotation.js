     function FormatPopUp(line)
     {
                            str_level = '<i class="green '+line["type"]["icon"] +'" data-tooltip="None"></i>'
                            status = "None"

                            if (line['level'] == 1)
                            {
                                status = line["type"]["tooltip_partial"]
                                str_level =  '<i class="yellow '+line["type"]["icon"] +'" data-tooltip="'+line["type"]["tooltip_partial"]+'"></i>'
                            }
                            else if (line['level'] == 2)
                            {
                                status = line["type"]["tooltip_nonpartial"]
                                str_level =  '<i class="red '+line["type"]["icon"] +'" data-tooltip="'+line["type"]["tooltip_nonpartial"]+'"></i>'
                            }

                            endtime = "Undefined"
                            if (line['end'] != null)
                            {
                                endtime = line['end'];
                            }


                            htmlLine = '<p><i class="'+line['country']['code'] +' flag"/>'+ line['country']['name'] + "  "+ str_level+ '<br>Level: '+line["type"]["name"] +'<br>Measure:'+status+'<br>End: '+endtime+"<br>"+line["comment"]+"</p>";

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
          url: "/measuremeterdata/measures/?country="+countries+"&type="+measuretypes,
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

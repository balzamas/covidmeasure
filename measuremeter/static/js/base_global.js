    let Colors = ["#0000ff",
    "#00ffff",
    "#ff0000",
    "#008000",
    "#000000",
    "#a52a2a",
    "#a9a9a9",
    "#8b0000",
    "#bdb76b",
    "#556b2f",
    "#e9967a",
    "#9400d3",
    "#ff00ff",
    "#ffd700",
    "#4b0082",
    "#add8e6",
    "#e0ffff",
    "#90ee90",
    "#ffb6c1",
    "#ffffe0",
    "#00ff00",
    "#ff00ff",
    "#ffff00",
    "#800000",
    "#000080",
    "#808000",
    "#f0ffff",
    "#f5f5dc",
    "#800080",
    "#c0c0c0",
    "#00008b",
    "#008b8b",
    "#006400",
    "#ffa500",
    "#ff8c00",
    "#8b008b",
    "#9932cc",
    "#ffc0cb",
    "#f0e68c",
    "#d3d3d3",


    ];

    function save_image(graph)
    {
          var canvas = $('#'+graph).get(0);
          canvas.toBlob(function(blob) {
            saveAs(blob, "graph.png");
        });
    }


    function addDays(date, days)
    {
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

    function getRandom(arr, n)
    {
            var result = new Array(n),
                len = arr.length,
                taken = new Array(len);
            if (n > len)
                throw new RangeError("getRandom: more elements taken than available");
            while (n--) {
                var x = Math.floor(Math.random() * len);
                result[n] = arr[x in taken ? taken[x] : x];
                taken[x] = --len in taken ? taken[len] : len;
            }
            return result;
    }

    moment.updateLocale('en', {
      week: {
        dow : 1, // Monday is the first day of the week.
      }
    });

    function copyToClipboard(path) {
          var copyText = window.location.host + path;
          navigator.clipboard.writeText(copyText);
        }

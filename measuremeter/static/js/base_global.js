    let Colors = ["#0000ff",
    "#00ffff",
    "#ff0000",
    "#008000",
    "#000000",
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
     "#a52a2a",
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

function sortTable(n, tablename) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById(tablename);
  switching = true;
  // Set the sorting direction to ascending:
  dir = "asc";
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == "asc") {
        if (Number(x.children[0].innerHTML.replace(",", ".")) > Number(y.children[0].innerHTML.replace(",", "."))) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
         if (Number(x.children[0].innerHTML.replace(",", ".")) < Number(y.children[0].innerHTML.replace(",", "."))) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount ++;
    } else {
      /* If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}

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

    function copyToClipboard(path) {
          var copyText = window.location.host + path;
          navigator.clipboard.writeText(copyText);
        }

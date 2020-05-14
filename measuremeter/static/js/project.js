
      $( document ).ready(function() {
          //document.getElementById("dateselect").valueAsDate = new Date();

          if ( $( "#menu" ).length ) {
               document.getElementById('menu').innerHTML =
              '<div class="border border-dark" style="padding-left: 10;padding-top: 10;padding-bottom: 10;padding-right: 10;margin-bottom: 10"><font size="5rem"><a href="/">Home</a> // <a href="/about/">About</a> // <a href="/timeline/">Timeline</a> // <a href="/euromap/">EuroMap</a>         </font>        </div>';
           }

          if ( $( "#title_bar" ).length ) {
              document.getElementById('title_bar').innerHTML =
              '<div class="border border-dark" style="padding-left: 10;padding-top: 10;padding-bottom: 10;padding-right: 10;margin-bottom: 10"><font size="5rem">Contact: d.berger@dontsniff.co.uk // Twitter: <a href="https://twitter.com/BergerWthur">@BergerWthur</a>// <a href="/measuremeterdata/">REST Endpoints</a>  // <a href="https://github.com/balzamas/covidmeasure/">Project on GitHub</a><br>         Please contact me if you have corrections/find wrong data. </font>        </div>';
          }
       });

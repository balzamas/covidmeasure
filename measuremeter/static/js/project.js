
      $( document ).ready(function() {
          if ( $( "#menu" ).length ) {
               document.getElementById('menu').innerHTML = `
               <div style="padding-left: 10;padding-top: 10;padding-bottom: 10;padding-right: 10;margin-bottom: 10">
               <div class="ui seven item inverted huge menu">
                  <a class="item" href="/">Home</a>
                  <a class="item" href="/about/">Info/About</a>
                  <a class="item" href="/compare/">Compare Countries</a>
                  <a class="item" href="/ranking_europe/">Ranking</a>
                  <a class="item" href="/country/">Country Profiles</a>
                  <a class="item" href="/euromap/">Map</a>
                  <a class="item" href="/ch/">Switzerland</a>
                  </div>
                </div> `
           }

           if ( $( "#menu_ch" ).length ) {
               document.getElementById('menu_ch').innerHTML = `
               <div style="padding-left: 10;padding-top: 10;padding-bottom: 10;padding-right: 10;margin-bottom: 10">
               <div class="ui seven item inverted huge menu">
                  <a class="item" href="/">Home</a>
                  <a class="item" href="/cantons/">${gettext("Measures\<br\>Case\ development")}</a>
                  <a class="item" href="/chrisk/">${gettext("Risk\ calculator")}</a>
                  <a class="item" href="/districts/">${gettext("Map cases\<br\>Districts\ \&\ Cantons")}</a>
                  <a class="item" href="/ranking14/">${gettext("Ranking")}</a>
                  <a class="item" href="/">${gettext("Europe") }</a>
                  </div>
                </div> `
           }

                  //<a class="item" href="/chmaps/">${gettext("Map measures")}</a>


          if ( $( "#title_bar" ).length ) {
              document.getElementById('title_bar').innerHTML = `
              <div class="ui segment">
              Contact: d.berger@dontsniff.co.uk // Twitter: <a href="https://twitter.com/BergerWthur">@BergerWthur</a>// <a href="/measuremeterdata/">REST Endpoints</a> // Please contact me if you have corrections/find wrong data.
               </div><br>`
          }
       });

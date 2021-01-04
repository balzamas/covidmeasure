
      $( document ).ready(function() {
          if ( $( "#menu" ).length ) {
               document.getElementById('menu').innerHTML = `
               <div style="padding-left: 10;padding-top: 10;padding-bottom: 10;padding-right: 10;margin-bottom: 10">
               <div class="ui seven item inverted huge menu">
                  <a class="item" href="/">Home</a>
                  <a class="item" href="/about/">About</a>
                  <a class="item" href="/compare/">Compare<br>Countries</a>
                  <a class="item" href="/ranking_europe/">Ranking</a>
                  <a class="item" href="/deaths/">Deaths</a>
                  <a class="item" href="/euromap/">Map</a>
                  <a class="item" href="/ch/">Switzerland</a>
                  </div>
                </div> `
           }

                  //<a class="item" href="/country/">Country<br>Profiles</a>


           if ( $( "#menu_ch" ).length ) {
               document.getElementById('menu_ch').innerHTML = `
               <div style="padding-left: 10;padding-top: 10;padding-bottom: 10;padding-right: 10;margin-bottom: 10">
               <div class="ui eight item inverted huge menu">
                  <a class="item" href="/">Home</a>
                  <a class="item" href="/cantons/">${gettext("Measures Case development")}</a>
                  <a class="item" href="/districts7/">${gettext("Map cases Districts Cantons")}</a>
                  <a class="item" href="/chrisk/">${gettext("Risk calculator")}</a>
                  <a class="item" href="/ranking7/">${gettext("Ranking")}</a>
                  <a class="item" href="/chmaps/">${gettext("Maps measures")}</a>
                  <a class="item" href="/deaths_ch/">${gettext("Deaths per canton")}</a>
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

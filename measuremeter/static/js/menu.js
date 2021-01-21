
      $( document ).ready(function() {

          if ( $( "#menu" ).length ) {

            $('.example .menu .browse').popup({
                inline: true,
                hoverable: true,
                position: 'bottom left',
                delay: {
                    show: 300,
                    hide: 800
                }
            });

          $('.ui.sidebar').sidebar({
            context: $('.ui.pushable.segment'),
            transition: 'overlay'
            }).sidebar('attach events', '#mobile_item');






               document.getElementById('menu').innerHTML = `
<div class="ui grid">

	<div class="computer only row">
		<div class="column">



      <div class="ui four item menu">
        <a class="item" href="/">${gettext("Home")}</a>

          <div class="ui simple dropdown item">
    ${gettext("Switzerland")}
    <i class="dropdown icon"></i>
    <div class="menu">
                  <a class="item" href="/cantons/">${gettext("Measures Case development")}</a>
                  <a class="item" href="/districts7/">${gettext("Map cases Districts Cantons")}</a>
                  <a class="item" href="/chrisk/">${gettext("Risk calculator")}</a>
                  <a class="item" href="/ranking7/">${gettext("Ranking")}</a>
                  <a class="item" href="/deaths_ch/">${gettext("Deaths per canton")}</a>
    </div>
  </div>
          <div class="ui simple dropdown item">
    ${gettext("World")}
    <i class="dropdown icon"></i>
    <div class="menu">
      <a class="item" href="/compare/">${gettext("Compare countries")}</a>
      <a class="item" href="/ranking_europe/">${gettext("Ranking")}</a>
      <a class="item" href="/country/">${gettext("Country profiles")}</a>
      <a class="item" href="/deaths/">${gettext("Deaths")}</a>
      <a class="item" href="/euromap/">${gettext("Map")}</a>
    </div>
  </div>

        <a class="item" href="about/">${gettext("About")}</a>


</div>

		</div>
	</div>

	 <div class="tablet mobile only row">

		<div class="column">
			<div class="ui menu">
				<a id="mobile_item" class="item"><i class="bars icon"></i></a>
        				<a href="/" class="item">${gettext("Home")}</a>
        				<a href="/ch/" class="item">${gettext("Switzerland")}</a>
        				<a href="about/" class="item">${gettext("About")}</a>

			</div>
		</div>
	</div>

</div>

<div class="ui pushable segment">
		<div class="ui sidebar vertical menu">
      <p><b>${gettext("Switzerland")}</b></p>
                  <a class="item" href="/cantons/">${gettext("Measures Case development")}</a>
                  <a class="item" href="/districts7/">${gettext("Map cases Districts Cantons")}</a>
                  <a class="item" href="/chrisk/">${gettext("Risk calculator")}</a>
                  <a class="item" href="/ranking7/">${gettext("Ranking")}</a>
                  <a class="item" href="/deaths_ch/">${gettext("Deaths per canton")}</a>
      <br><p><b>${gettext("World")}</b></p>
      <a class="item" href="/compare/">${gettext("Compare countries")}</a>
      <a class="item" href="/ranking_europe/">${gettext("Ranking")}</a>
      <a class="item" href="/country/">${gettext("Country profiles")}</a>
      <a class="item" href="/deaths/">${gettext("Deaths")}</a>
      <a class="item" href="/euromap/">${gettext("Map")}</a>
		</div>
`
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import measuremeterdata.scrape_common as sc
from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths, CHCanton, CHCases
from datetime import date, timedelta

district_names = {
    241: "Jura bernois",
    242: "Biel/Bienne",
    243: "Seeland",
    244: "Oberaargau",
    245: "Emmental",
    246: "Bern-Mittelland",
    247: "Thun",
    248: "Obersimmental-Saanen",
    249: "Frutigen-Niedersimmental",
    250: "Interlaken-Oberhasli",
}

district_population = {
    241: 53721,
    242: 101313,
    243: 74769,
    244: 81759,
    245: 97218,
    246: 414356,
    247: 107491,
    248: 16588,
    249: 40375,
    250: 47387,
}

communes = {
"Innertkirchen":250,
"Guttannen":250,
"Grindelwald":250,
"Lauterbrunnen":250,
"Kandersteg":249,
"Diemtigen":249,
"Reichenbach im Kandertal":249,
"Lenk":248,
"Saanen":248,
"Adelboden":249,
"Boltigen":248,
"Zweisimmen":248,
"Frutigen":249,
"Gsteig":248,
"Trub":245,
"St. Stephan":248,
"Eggiwil":245,
"Sumiswald":245,
"Lauenen":248,
"Rüschegg":246,
"Sigriswil":247,
"Guggisberg":246,
"Bern":246,
"Köniz":246,
"Habkern":250,
"Langnau im Emmental":245,
"Brienz":250,
"Oberwil im Simmental":249,
"Schwarzenburg":246,
"Hasliberg":250,
"Meiringen":250,
"Röthenbach im Emmental":245,
"Erlenbach im Simmental":249,
"Schangnau":245,
"Wohlen bei Bern":246,
"Därstetten":249,
"Kandergrund":249,
"Rüeggisberg":246,
"Fraubrunnen":246,
"Schattenhalb":250,
"Aeschi bei Spiez":249,
"Riggisberg":246,
"Beatenberg":250,
"Wynigen":245,
"Nods":241,
"Mühleberg":246,
"Plateau de Diesse":241,
"Tramelan":241,
"Vechigen":246,
"Court":241,
"Petit-Val":241,
"Ins":243,
"Péry-La Heutte":241,
"Sonvilier":241,
"Belp":246,
"Madiswil":244,
"Rapperswil":243,
"Wimmis":249,
"Courtelary":241,
"Heimiswil":245,
"Signau":245,
"Iseltwald":250,
"Hasle bei Burgdorf":245,
"Neuenegg":246,
"Eriz":247,
"Orvin":241,
"Thun":247,
"Biel/Bienne":242,
"Lauperswil":245,
"Lützelflüh":245,
"Worb":246,
"Saint-Imier":241,
"Seedorf":243,
"Oberried am Brienzersee":250,
"Schüpfen":243,
"Niederbipp":244,
"Moutier":241,
"Krauchthal":245,
"Saxeten":250,
"Valbirse":241,
"Kallnach":243,
"Horrenbach-Buchen":247,
"Corgémont":241,
"Huttwil":244,
"Langenthal":244,
"Walkringen":246,
"Rüderswil":245,
"Utzenstorf":245,
"Seeberg":244,
"Spiez":249,
"Gündlischwand":250,
"Bolligen":246,
"Oberdiessbach":246,
"Villeret":241,
"Trachselwald":245,
"Münsingen":246,
"Trubschachen":245,
"Burgdorf":245,
"Blumenstein":247,
"Ersigen":245,
"Buchholterberg":247,
"Grossaffoltern":243,
"Bönigen":250,
"Rüegsau":245,
"Sonceboz-Sombeval":241,
"Lyss":243,
"Steffisburg":247,
"Tavannes":241,
"Cortébert":241,
"Radelfingen":243,
"Bowil":246,
"Kirchdorf":246,
"Wattenwil":247,
"Stocken-Höfen":247,
"La Ferrière":241,
"Dürrenroth":245,
"Unterseen":250,
"Saicourt":241,
"Cormoret":241,
"Sauge":241,
"Wald":246,
"Linden":246,
"Wilderswil":250,
"Konolfingen":246,
"Renan":241,
"Büren an der Aare":243,
"Oberbalm":246,
"Lütschental":250,
"Ochlenberg":244,
"Kirchlindach":246,
"Wyssachen":244,
"Oberburg":245,
"Wichtrach":246,
"Affoltern im Emmental":245,
"Eriswil":244,
"Jegenstorf":246,
"Reutigen":247,
"Twann-Tüscherz":242,
"Kappelen":243,
"Oberthal":246,
"Gampelen":243,
"Arni":246,
"Leissigen":250,
"Leuzigen":243,
"Melchnau":244,
"Landiswil":246,
"Meikirch":246,
"Bätterkinden":245,
"Uetendorf":247,
"Brienzwiler":250,
"Aarwangen":244,
"Pohlern":247,
"Herzogenbuchsee":244,
"Thunstetten":244,
"Crémines":241,
"Gondiswil":244,
"Frauenkappelen":246,
"Ursenbach":244,
"Oberlangenegg":247,
"Roches":241,
"Kirchberg":245,
"Ringgenberg":250,
"Münchenbuchsee":246,
"Hofstetten bei Brienz":250,
"Perrefitte":241,
"Oberbipp":244,
"Seehof":241,
"Pieterlen":242,
"Reconvilier":241,
"Grandval":241,
"Aarberg":243,
"Walterswil":244,
"Bargen":243,
"Gals":243,
"Roggwil":244,
"Ferenbalm":246,
"Gerzensee":246,
"Attiswil":244,
"Muri bei Bern":246,
"Brienzwiler":250,
"Thierachern":247,
"Burgistein":247,
"Wiedlisbach":244,
"Lengnau":242,
"Niedermuhlern":246,
"Urtenen-Schönbühl":246,
"Champoz":241,
"Wengi":243,
"Schwanden bei Brienz":250,
"Gsteigwiler":250,
"Romont":241,
"Walperswil":243,
"Grosshöchstetten":246,
"Koppigen":245,
"Därligen":250,
"Rubigen":246,
"Sorvilier":241,
"Unterlangenegg":247,
"Corcelles":241,
"La Neuveville":241,
"Hindelbank":245,
"Oberwil bei Büren":243,
"Fahrni":247,
"Brüttelen":243,
"Eschert":241,
"Alchenstorf":245,
"Homberg":247,
"Rüti bei Büren":243,
"Rohrbachgraben":244,
"Moosseedorf":246,
"Arch":243,
"Diessbach bei Büren":243,
"Lotzwil":244,
"Lyssach":245,
"Oberhünigen":246,
"Krattigen":249,
"Ostermundigen":246,
"Thurnen":246,
"Heimenhausen":244,
"Bleienbach":244,
"Safnern":242,
"Schelten":241,
"Heiligenschwendi":247,
"Siselen":243,
"Heimberg":247,
"Lüscherz":243,
"Niederhünigen":246,
"Zäziwil":246,
"Zollikofen":246,
"Wangen an der Aare":244,
"Rumisberg":244,
"Wynau":244,
"Iffwil":246,
"Brügg":242,
"Toffen":246,
"Müntschemier":243,
"Bannwil":244,
"Kriechenwil":246,
"Treiten":243,
"Amsoldingen":247,
"Loveresse":241,
"Kiesen":246,
"Rümligen":246,
"Auswil":244,
"Jens":243,
"Vinelz":243,
"Thörigen":244,
"Teuffenthal":247,
"Gurzelen":247,
"Forst-Längenbühl":247,
"Kehrsatz":246,
"Uebeschi":247,
"Meinisberg":242,
"Täuffelen":243,
"Mont-Tramelan":241,
"Saules":241,
"Interlaken":250,
"Dotzigen":243,
"Ittigen":246,
"Wileroltigen":246,
"Schwadernau":242,
"Laupen":246,
"Niederried bei Interlaken":250,
"Rohrbach":244,
"Rütschelen":244,
"Orpund":242,
"Bettenhausen":244,
"Oeschenbach":244,
"Obersteckholz":244,
"Seftigen":247,
"Rüeggisberg":246,
"Matten bei Interlaken":250,
"Wiler bei Utzenstorf":245,
"Belprahon":241,
"Allmendingen":246,
"Uttigen":247,
"Bellmund":242,
"Schwarzhäusern":244,
"Mattstetten":246,
"Evilard":242,
"Farnern":244,
"Büetigen":243,
"Biglen":246,
"Sutz-Lattrigen":242,
"Finsterhennen":243,
"Rebévelier":241,
"Wachseldorn":247,
"Stettlen":246,
"Zuzwil":246,
"Hermrigen":243,
"Epsach":243,
"Oppligen":246,
"Inkwil":244,
"Kernenried":245,
"Lützelflüh":245,
"Tschugg":243,
"Graben":244,
"Walliswil bei Wangen":244,
"Häutligen":246,
"Bühl":243,
"Freimettigen":246,
"Mötschwil":245,
"Wangenried":244,
"Diemerswil":246,
"Busswil bei Melchnau":244,
"Erlach":243,
"Hilterfingen":247,
"Niederönz":244,
"Herbligen":246,
"Worben":243,
"Bäriswil":246,
"Studen":243,
"Rüdtligen-Alchenflüh":245,
"Oberhofen am Thunersee":247,
"Horrenbach-Buchen":247,
"Höchstetten":245,
"Münchenwiler":246,
"Zwieselberg":247,
"Port":242,
"Rumendingen":245,
"Lützelflüh":245,
"Mirchel":246,
"Merzligen":243,
"Brenzikofen":246,
"Jegenstorf":246,
"Willadingen":245,
"Deisswil bei Münchenbuchsee":246,
"Aegerten":242,
"Mörigen":242,
"Scheuren":242,
"Matten bei Interlaken":250,
"Kaufdorf":246,
"Aefligen":245,
"Reisiswil":244,
"Zielebach":245,
"Bremgarten bei Bern":246,
"Ipsach":242,
"Gurbrü":246,
"Hagneck":243,
"Ligerz":242,
"Nidau":242,
"Hellsau":245,
"Walliswil bei Niederbipp":244,
"Wiggiswil":246,
"Berken":244,
"Jaberg":246,
"Ferenbalm":246,
"Rüti bei Lyssach":245,
"Oberburg":245,
"Oberburg":245,
"Heimiswil":245,
"Twann-Tüscherz":242,
"Clavaleyres":246,
"Erlach":243,
"Meienried":243,
"Mont-Tramelan":241,
"Gampelen":243,
#Map crippled Gemeinden names to districts
"Sonceboz-": 241,
"Oster-":246,
"Frauen-kappelen":246,
"Frauen-":246,
"Kleinst-":241,
"Urtenen-":246,
"Rüdtligen-":245,
"Forst-":247,
"München-":246,
"Schwarzen-":246,
"Biel":242,
"Thoune":247,
"Tavanne":241,
"Plateau":241,
"Péry-La":241,
"Safern":242,
"Buchholter-":247,
"Wohlen":246,
"Büren":243,
"Muri":246,
"Muri-Gümligen":246,
"St.":248,
"St-Imier":241,



}


class Command(BaseCommand):
    def handle(self, *args, **options):

        url = 'https://www.besondere-lage.sites.be.ch/besondere-lage_sites/de/index/corona/index.html'
        d = sc.download(url, silent=True)
        d = d.replace('&nbsp;', ' ')

        soup = BeautifulSoup(d, 'html.parser')
        table = soup.find(string=re.compile(r'Corona-Erkrankungen im Kanton Bern')).find_next('table')

        for tr in table.tbody.find_all('tr'):
            date_be = tr.find_all('td')[0].find_all('strong')[0].string
            if not date_be:
                #There are some annoying elements in the date field like <br>
                date_be = str(tr.find_all('td')[0].find_all('strong')[0]).split(">")[1].split("<")[0]

            line = str(tr.find_all('td')[2])

            disctricts = {
                241: 0,
                242: 0,
                243: 0,
                244: 0,
                245: 0,
                246: 0,
                247: 0,
                248: 0,
                249: 0,
                250: 0,
            }

            value_total = 0

            for commune in line.split("<br/>"):
                if "</td>" in commune:
                    commune = commune.split('</td>')[0]
                if ">" in commune:
                    commune = commune.split('>')[1]
                if "<" in commune:
                    commune = commune.split('<')[0]
                if len(commune.split(' ')) > 1:

                    try:
                        value = int(commune.split(' ')[0])
                        value_total += value
                        name = commune.split(' ')[1]

                        if name in communes:
                            bezirknum = communes[name]
                            disctricts[bezirknum] += value
                        else:
                            print(f"Value:{value}")
                            print(f"Name:{name}")
                            print("----ERROR---")

                    except:
                        print("A weird line")

            for district in disctricts:
                    print(f"{district};{date_be};{district_names[district]};{district_population[district]};{disctricts[district]}")

                    year = date_be.split(".")[2]
                    if len(year) == 2:
                        year = f"20{year}"

                    date_iso = f'{year}-{date_be.split(".")[1]}-{date_be.split(".")[0]}'
                    date_tosave = date.fromisoformat(date_iso)

                    bezirk = CHCanton.objects.get(swisstopo_id=district)

                    incidence7days = None
                    incidence14days = None
                    cases7days = disctricts[district]
                    has_a_none=False

                    for x in range(1, 7):
                        print(x)
                        try:
                            past = CHCases.objects.get(canton=bezirk, date=date_tosave-timedelta(days=x))
                            if past.cases is not None:
                                cases7days += past.cases
                            else:
                                has_a_none = True
                        except:
                            has_a_none = True

                    if not has_a_none:
                        incidence7days = cases7days * 100000 / bezirk.population

                        try:
                            past7 = CHCases.objects.get(canton=bezirk, date=date_tosave-timedelta(days=7))

                            if (past7.incidence_past7days):
                                incidence14days = incidence7days + float(past7.incidence_past7days)
                        except:
                            print("Well....")

                    try:
                        cd_existing = CHCases.objects.get(canton=bezirk, date=date_tosave)
                        cd_existing.cases = disctricts[district]
                        if (incidence7days):
                            cd_existing.incidence_past7days = incidence7days
                        if (incidence14days):
                            cd_existing.incidence_past14days = incidence14days
                        cd_existing.save()
                    except CHCases.DoesNotExist:
                        cd = CHCases(canton=bezirk, cases=disctricts[district], date=date_tosave)
                        if (incidence7days):
                            cd.incidence_past7days = incidence7days
                        if (incidence14days):
                            cd.incidence_past14days = incidence14days
                        cd.save()




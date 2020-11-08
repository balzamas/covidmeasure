import requests
from django.core.management.base import BaseCommand, CommandError
import urllib.request, json
from measuremeterdata.models.models_ch import CHCanton, CHCases
from datetime import date, timedelta


def load_bezirk(bezirk):
        kreis = CHCanton.objects.filter(swisstopo_id="D" + bezirk)

        if kreis:
            url_toload = f"https://raw.githubusercontent.com/entorb/COVID-19-Coronavirus-German-Regions/master/data/de-districts/de-district_timeseries-{bezirk}.json"
            with urllib.request.urlopen(url_toload) as url:

                last_numbers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
                data = json.loads(url.read().decode())
                for row in data:
                    print(row['Cases'])
                    print("xxxxx")

                    val_today = row['Cases_New']

                    last_numbers.append(val_today)
                    last_numbers.pop(0)

                    tot = 0
                    seven_tot = 0

                    daycount = 0
                    for x in last_numbers:
                        tot += x

                        if (daycount > 6):
                            seven_tot += x

                        daycount += 1

                    fourteen_avg = tot * 100000 / kreis[0].population
                    seven_avg = seven_tot * 100000 / kreis[0].population

                    date_tosave = date.fromisoformat(row['Date'])

                    development7to7 = 0
                    if (tot - seven_tot) > 0:
                        development7to7 = (seven_tot * 100 / (tot - seven_tot)) - 100

                    print(kreis[0])
                    print(date_tosave)
                    print(fourteen_avg)

                    try:
                        cd_existing = CHCases.objects.get(canton=kreis[0], date=date_tosave)
                        cd_existing.cases = val_today
                        cd_existing.incidence_past7days = seven_avg
                        cd_existing.incidence_past14days = fourteen_avg
                        cd_existing.development7to7 = development7to7
                        cd_existing.date = date_tosave
                        cd_existing.save()
                    except CHCases.DoesNotExist:
                        cd = CHCases(canton=kreis[0], incidence_past7days=seven_avg, incidence_past14days=fourteen_avg,
                                     cases=val_today, development7to7=development7to7, date=date_tosave)
                        cd.save()


class Command(BaseCommand):
    def handle(self, *args, **options):


        bezirke = ["08335", "08336", "08337", "08435", "09776", "08326"]

        for bezirk in bezirke:
            load_bezirk(bezirk)




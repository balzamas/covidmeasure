from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models_ch import CHCanton, CHCases
import os
import csv
import datetime
from datetime import datetime
import requests
import pandas as pd
from io import BytesIO
import io
from datetime import date, timedelta
from measuremeterdata.tasks.socialmedia.tweet_district_ranking import tweet

def load_data(file, name, swisstopo):
    print(file.columns)

    last_numbers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
    bezirk = CHCanton.objects.filter(swisstopo_id=swisstopo)

    for index_row, row in file.iterrows():
        cases_td = row[name]
        last_numbers.append(cases_td)
        last_numbers.pop(0)

        tot = 0
        seven_tot = 0

        daycount = 0
        for x in last_numbers:
            tot += x

            if (daycount > 6):
                seven_tot += x

            daycount += 1

        fourteen_avg = tot * 100000 / bezirk[0].population
        seven_avg = seven_tot * 100000 / bezirk[0].population

        development7to7 = 0
        if (tot - seven_tot) > 0:
            development7to7 = (seven_tot * 100 / (tot - seven_tot)) - 100

        date_tosave = datetime.strptime(row['Date'], "%d.%m.%Y")

        print(bezirk[0])
        print(cases_td)
        print(date_tosave)
        print(f"Average:{fourteen_avg}")

        try:
            cd_existing = CHCases.objects.get(canton=bezirk[0], date=date_tosave)
            cd_existing.cases = cases_td
            cd_existing.incidence_past7days = seven_avg
            cd_existing.incidence_past14days = fourteen_avg
            cd_existing.development7to7 = development7to7
            cd_existing.date = date_tosave
            cd_existing.save()
        except CHCases.DoesNotExist:
            has_new_data = True
            cd = CHCases(canton=bezirk[0], incidence_past7days=seven_avg, incidence_past14days=fourteen_avg,
                         cases=cases_td, development7to7=development7to7, date=date_tosave)
            cd.save()


def import_data():
    fr_data = requests.get('https://www.fr.ch/de/document/422471').content
    df = pd.read_csv(io.StringIO(fr_data.decode('ISO-8859-1')), delimiter=';')

    load_data(df, "Broye", 1001)
    load_data(df, "Glâne", 1002)
    load_data(df, "Gruyère", 1003)
    load_data(df, "Sarine", 1004)
    load_data(df, "Lac", 1005)
    load_data(df, "Singine", 1006)
    load_data(df, "Veveyse", 1007)


class Command(BaseCommand):
    def handle(self, *args, **options):

        import_data()

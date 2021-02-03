from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, MeasureCategory, Continent, CasesDeaths
import os
import csv
import datetime
from datetime import timedelta
import requests
import pandas as pd
from io import BytesIO
import io
import gzip
from urllib.request import urlopen
from measuremeterdata.tasks import import_helper
import shutil
import fileinput

def getdata(country):
    print(country)

    url = 'https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=data/demo_r_mwk_ts.tsv.gz'
    resp = urlopen(
        'https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=data/demo_r_mwk_ts.tsv.gz')

    r = requests.get(url, allow_redirects=True)

    open('/tmp/deaths.csv.gz', 'wb').write(r.content)

    with gzip.open('/tmp/deaths.csv.gz', 'rb') as f_in:
        with open('/tmp/deaths.csv', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    # Read in the file
    with open('/tmp/deaths.csv', 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('geo\\time', 'geo')

    # Write the file out again
    with open('/tmp/deaths.csv', 'w') as file:
        file.write(filedata)

    df = pd.read_csv('/tmp/deaths.csv', sep='\t')

    if (country.code.lower() == 'gb'):
        code = 'UK'
    elif (country.code.lower() == 'gr'):
        code = 'EL'
    else:
        code = country.code.upper()

    for index_row, row in df.iterrows():
        if row['sex,unit,geo'] == f'T,NR,{code}':
            index_column = 0
            for col in row:
                if "W" in df.columns[index_column] and "99" not in df.columns[index_column] and ":" not in col:

                    year = int(df.columns[index_column].split('W')[0])
                    week = int(df.columns[index_column].split('W')[1])

                    if year > 2019:
                        savedate = import_helper.get_start_end_dates(year, week)[0]
                        value = int(col.replace('p', '').replace('e', '').replace(' ', ''))
                        avg = value / 7

                        if week < 10:
                            week_str = "0" + str(week)
                        else:
                            week_str = week


                        try:
                            value_peak = int(
                                row[f"{country.peak_year}W{week_str} "].replace('p', '').replace('e', '').replace(' ',
                                                                                                                  ''))
                            avg_peak = value_peak / 7
                        except:
                            avg_peak = -1

                        avg_1519 = None
                        if country.code == "de":
                            if week < 53:
                                avg_1519 = (int(row[f"2016W{week_str} "].replace('p', '').replace('e', '').replace(' ','')) + int(row[f"2017W{week_str} "].replace('p', '').replace('e', '').replace(' ','')) + int(row[f"2018W{week_str} "].replace('p', '').replace('e', '').replace(' ','')) + int(row[f"2019W{week_str} "].replace('p', '').replace('e', '').replace(' ',''))) / 4
                        else:
                            if week < 53:
                                avg_1519 = (int(row[f"2015W{week_str} "].replace('p', '').replace('e', '').replace(' ','')) + int(row[f"2016W{week_str} "].replace('p', '').replace('e', '').replace(' ','')) + int(row[f"2017W{week_str} "].replace('p', '').replace('e', '').replace(' ','')) + int(row[f"2018W{week_str} "].replace('p', '').replace('e', '').replace(' ','')) + int(row[f"2019W{week_str} "].replace('p', '').replace('e', '').replace(' ',''))) / 5
                            else:
                                avg_1519 = int(row[f"2015W{week_str} "].replace('p', '').replace('e', '').replace(' ',''))

                        if avg_1519:
                            avg_1519 = avg_1519 / 7

                        for number in range(1, 8):
                            try:
                                cd_existing = CasesDeaths.objects.get(country=country, date=savedate)
                                cd_existing.deathstotal = avg
                                cd_existing.deathstotal_peak = avg_peak
                                cd_existing.deathstotal_average = avg_1519
                                cd_existing.save()
                            except CasesDeaths.DoesNotExist:
                                cd = CasesDeaths(country=country, deathstotal=avg, deathstotal_peak=avg_peak, deathstotal_average=avg_1519, date=savedate)
                                cd.save()

                            savedate += timedelta(days=1)

                index_column += 1

class Command(BaseCommand):



    def handle(self, *args, **options):
        getdata(Country.objects.get(pk=25)) #Eesti
        getdata(Country.objects.get(pk=3)) #cz
        getdata(Country.objects.get(pk=32)) #bg
        getdata(Country.objects.get(pk=14)) #be
        getdata(Country.objects.get(pk=7)) #uk
        getdata(Country.objects.get(pk=12)) #sk
        getdata(Country.objects.get(pk=31)) #pt
        getdata(Country.objects.get(pk=36)) #hr
        getdata(Country.objects.get(pk=29)) #hu
        getdata(Country.objects.get(pk=33)) #it
        getdata(Country.objects.get(pk=19)) #si
        getdata(Country.objects.get(pk=16)) #lt
        getdata(Country.objects.get(pk=26)) #lv
        getdata(Country.objects.get(pk=17)) #lu
        getdata(Country.objects.get(pk=41)) #me
        getdata(Country.objects.get(pk=22)) #no
        getdata(Country.objects.get(pk=37)) #rs
        getdata(Country.objects.get(pk=18)) #pl
        getdata(Country.objects.get(pk=13)) #nl
        getdata(Country.objects.get(pk=8)) #dk
        getdata(Country.objects.get(pk=20))  # es
        getdata(Country.objects.get(pk=34)) #fr
#        getdata(Country.objects.get(pk=1)) #ch
        getdata(Country.objects.get(pk=30)) #ro
        getdata(Country.objects.get(pk=45)) #arm
        getdata(Country.objects.get(pk=6)) #at
        getdata(Country.objects.get(pk=23)) #se
        getdata(Country.objects.get(pk=38)) #greece
        getdata(Country.objects.get(pk=44)) #is
        getdata(Country.objects.get(pk=24)) #fi
        getdata(Country.objects.get(pk=35)) #de
        getdata(Country.objects.get(pk=49)) #cy



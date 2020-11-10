from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths
import os
import csv
import datetime
from datetime import timedelta
import requests
import pandas as pd
from io import BytesIO
import gzip
from urllib.request import urlopen

def CalcCaesesPer100k(cases, population):
    casespm = int(cases) *100000 / (int(population))
    return casespm

def get_start_end_dates(year, week):
    d = datetime.datetime(year, 1, 1)
    if (d.weekday() <= 3):
        d = d - timedelta(d.weekday())
    else:
        d = d + timedelta(7 - d.weekday())
    dlt = timedelta(days=(week - 1) * 7)
    return d + dlt , d + dlt + timedelta(days=6)





def getdata(country):
    print(country)
    resp = urlopen(
        'https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=data/demo_r_mwk_ts.tsv.gz')

    import gzip
    nr = 0
    with gzip.open(resp, 'rt') as f:
        file_content = f.read()

        weeks = []

        head = file_content.splitlines()[0]

        col_cnt = 0
        for header_col in head.split('\t'):
            if ("W" in header_col and header_col.split('W')[0] == '2020' and "99" not in header_col):
                weeks.append(get_start_end_dates(int(header_col.split('W')[0]), int(header_col.split('W')[1])))

            if (str(country.peak_year)+"W"+str(len(weeks)-1) in header_col):
                peak_col_nr = col_cnt-3
            col_cnt += 1

        week = -1;
        for line in file_content.splitlines():
            if (line.split('\t')[0].split(',')[0] == 'T'):
                if (country.code.lower() == 'gb'):
                    code ='uk'
                elif (country.code.lower() == 'gr'):
                        code = 'el'
                else:
                    code = country.code.lower()
                if (line.split('\t')[0].split(',')[2].lower() == code):
                    columns = line.split('\t')
                    col_cnt = 0
                    for col in columns:

                        if (col_cnt > peak_col_nr):
                            if ("NR" not in col and ':' not in col and week < len(weeks)):
                                value = int(col.replace('p', '').replace('e', '').replace(' ', ''))
                                avg = value / 7

                                savedate = weeks[week][0]

                                for number in range(1, 8):
                                    try:
                                        cd_existing = CasesDeaths.objects.get(country=country, date=savedate)
                                        cd_existing.deathstotal_peak = avg
                                        cd_existing.save()
                                    except CasesDeaths.DoesNotExist:
                                        cd = CasesDeaths(country=country, deathstotal_peak=avg,
                                                                           date=savedate)
                                        cd.save()

                                    savedate += timedelta(days=1)
                                week += 1

                        elif ("NR" not in col and ':' not in col and week < len(weeks)):

                            value = int(col.replace('p', '').replace('e', '').replace(' ', ''))

                            avg = value / 7

                            savedate = weeks[week][0]

                            for number in range(1, 8):
                                try:
                                    cd_existing = CasesDeaths.objects.get(country=country, date=savedate)
                                    cd_existing.deathstotal = avg
                                    cd_existing.save()
                                except CasesDeaths.DoesNotExist:
                                    cd = CasesDeaths(country=country, deathstotal=avg,date=savedate)
                                    cd.save()

                                savedate += timedelta(days=1)

                            week += 1
                        elif ':' in col:
                            week += 1

                        if (col_cnt == peak_col_nr):
                            week = -1

                        col_cnt += 1

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



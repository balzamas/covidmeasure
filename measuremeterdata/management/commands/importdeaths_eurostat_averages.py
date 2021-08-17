from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, MeasureCategory, Continent, CasesDeaths
import os
import csv
import datetime
from datetime import timedelta
import requests
import pandas as pd
from io import BytesIO
import gzip
from urllib.request import urlopen
from measuremeterdata.tasks import import_helper

def getdata(country):
    print(country)
    resp = urlopen(
        'https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=data/demo_r_mwk_ts.tsv.gz')

    import gzip
    nr = 0
    with gzip.open(resp, 'rt') as f:
        file_content = f.read()

        weeks19 = []
        weeks18 = []
        weeks17 = []
        weeks16 = []
        weeks15 = []

        head = file_content.splitlines()[0]

        col_nr_15 = -1
        col_nr_16 = -1
        col_nr_17 = -1
        col_nr_18 = -1
        col_nr_19 = -1

        col_cnt = 0
        for header_col in head.split('\t'):
            if ("W" in header_col and header_col.split('W')[0] == '2019' and "99" not in header_col):
                weeks19.insert(0,col_cnt)

            if ("W" in header_col and header_col.split('W')[0] == '2018' and "99" not in header_col):
                weeks18.insert(0,col_cnt)

            if ("W" in header_col and header_col.split('W')[0] == '2017' and "99" not in header_col):
                weeks17.insert(0,col_cnt)

            if ("W" in header_col and header_col.split('W')[0] == '2016' and "99" not in header_col):
                weeks16.insert(0,col_cnt)

            if ("W" in header_col and header_col.split('W')[0] == '2015' and "99" not in header_col):
                weeks15.insert(0,col_cnt)

            col_cnt += 1


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

                    for week in range(0, 52):
                        try:
                            total = (int(columns[weeks19[week]].replace('p', '').replace('e', '').replace(' ', '')) + int(columns[weeks18[week]].replace('p', '').replace('e', '').replace(' ', '')) + int(columns[weeks17[week]].replace('p', '').replace('e', '').replace(' ', '')) + int(columns[weeks16[week]].replace('p', '').replace('e', '').replace(' ', '')) + int(columns[weeks15[week]].replace('p', '').replace('e', '').replace(' ', '')))/5
                        except:
                            total = int(columns[weeks15[week]].replace('p', '').replace('e', '').replace(' ', ''))

                        avg = total / 7

                        savedate = import_helper.get_start_end_dates(2020,(week+1))[0]
                        print(savedate)
                        print(avg)

                        for number in range(1, 8):
                            try:
                                cd_existing = CasesDeaths.objects.get(country=country, date=savedate)
                                cd_existing.deathstotal_average = avg
                                cd_existing.save()
                            except CasesDeaths.DoesNotExist:
                                cd = CasesDeaths(country=country, deathstotal_average=avg,date=savedate)
                                cd.save()

                            savedate += timedelta(days=1)



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
    #    getdata(Country.objects.get(pk=33)) #it incomplete data 2015
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
#        getdata(Country.objects.get(pk=35)) #de incomplete data 2015
        getdata(Country.objects.get(pk=49)) #cy
        getdata(Country.objects.get(pk=39)) #al
        getdata(Country.objects.get(pk=53)) #mt



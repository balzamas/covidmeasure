from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, MeasureCategory, Continent, CasesDeaths, CountryMeasure, CountryMeasureType
import os
import csv
import datetime
import requests
from datetime import date, datetime, timedelta
from decimal import *
import pandas as pd
import numpy as np

import io


class Command(BaseCommand):
    def handle(self, *args, **options):
        import_oxford(
            'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/c1_school_closing.csv',
            'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/c1_flag.csv',
            2
        )

        import_oxford(
            'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/c8_internationaltravel.csv',
            None,
            7
        )

        import_oxford(
            'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/h2_testing_policy.csv',
            None,
            10
        )

        import_oxford(
            'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/c4_restrictions_on_gatherings.csv',
            'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/c4_flag.csv',
            1
        )


        import_oxford(
            'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/c2_workplace_closing.csv',
            'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/c2_flag.csv',
            3
        )

        import_oxford(
            'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/c3_cancel_public_events.csv',
            'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/c3_flag.csv',
            4
        )

        import_oxford(
            'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/c6_stay_at_home_requirements.csv',
            'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/c6_flag.csv',
            5
        )

        import_oxford(
            'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/c7_movementrestrictions.csv',
            'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/c7_flag.csv',
            6
        )

        import_oxford(
            'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/h7_vaccination_policy.csv',
            None,
            8
        )

        import_oxford(
            'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/h6_facial_coverings.csv',
            'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/h6_flag.csv',
            9
        )

def import_oxford(measures, flags, category):
    category = CountryMeasureType.objects.get(pk=category)

    s_measures = requests.get(measures).content
    df_measures = pd.read_csv(io.StringIO(s_measures.decode('utf-8')))

    if flags:
        s_flags = requests.get(flags).content
        df_flags = pd.read_csv(io.StringIO(s_flags.decode('utf-8')))
        df_flags.set_index("country_code", inplace=True)

    # Load countries
    cntries = []
    for cntry in Country.objects.all():
        if (cntry.iso_code):
            cntries.append(cntry.iso_code.lower())

    print(f"Load {category} into django")

    for index_row, row in df_measures.iterrows():
        if len(row) > 1 and row[1].lower() in cntries:
            country = Country.objects.get(iso_code=row[1])
            print(country)

            index_column = 0
            last_level = -1
            last_flag = 1
            measure = None

            for col in row:
                if flags:
                    try:
                        flag = int(df_flags.loc[row['country_code']][df_measures.columns[index_column]])
                    except:
                        flag = 1
                else:
                    flag = 1

                if (index_column > 2):
                    if np.isfinite(col) and (int(col) != last_level or int(flag) != last_flag):
                            start_date = datetime.strptime(df_measures.columns[index_column], '%d%b%Y')
                            stop_date = start_date + timedelta(days=-1)
                            if measure:
                                measure.end = stop_date
                                measure.save()

                            level = int(col)

                            if level == 0:
                                comment = category.text_level0
                            elif level == 1:
                                comment = category.text_level1
                            elif level == 2:
                                comment = category.text_level2
                            elif level == 3:
                                comment = category.text_level3
                            elif level == 4:
                                comment = category.text_level4

                            if flag == 0:
                                isregional = True
                            else:
                                isregional = False


                                if last_level == -1:
                                    last_level_tosave = 0
                                else:
                                    last_level_tosave = last_level

                            try:
                                measure = CountryMeasure.objects.get(country=country, type=category, start=start_date)
                                measure.level = level
                                measure.comment = comment
                                measure.last_level = last_level_tosave
                                measure.isregional = isregional
                                measure.source = "https://www.bsg.ox.ac.uk/research/research-projects/coronavirus-government-response-tracker"
                                measure.save()
                            except:
                                print("does not exist, create new")
                                measure = CountryMeasure(country=country, type=category, comment = comment,
                                                         source="https://www.bsg.ox.ac.uk/research/research-projects/coronavirus-government-response-tracker", start=start_date,
                                                         isregional=isregional, level=level, last_level = last_level_tosave)
                                measure.save()
                            last_level = int(col)
                            last_flag = flag

                index_column += 1



def import_oxford_old(url, flag, category):

      with requests.Session() as s:
        category = CountryMeasureType.objects.get(pk=category)

        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        print(cr.row[6])

        #Load countries
        cntries = []
        for cntry in Country.objects.all():
            if (cntry.iso_code):
                cntries.append(cntry.iso_code.lower())

        print(f"Load {category} into django")


        row_count = 0

        for row in cr:
            if row_count == 0:
                firstrow = row
            row_count += 1


            if len(row) > 1 and row[1].lower() in cntries:
                country=Country.objects.get(iso_code=row[1])

                col_num = 0
                last_level = 0
                measure = None
                for col in row:
                    if (col_num > 2):
                        if col != "" and int(col) != last_level:
                            start_date = datetime.strptime(firstrow[col_num], '%d%b%Y')
                            stop_date = start_date + timedelta(days=-1)
                            if measure:
                                measure.end = stop_date
                                measure.save()

                            level = int(col)

                            if level == 0:
                                comment = category.text_level0
                            elif level == 1:
                                comment = category.text_level1
                            elif level == 2:
                                comment = category.text_level2
                            elif level == 3:
                                comment = category.text_level3
                            elif level == 4:
                                comment = category.text_level4

                            try:
                                measure = CountryMeasure.objects.get(country=country, type=category, start=start_date)
                                measure.level = level
                                measure.comment = comment
                                measure.last_level = last_level
                                measure.source = "https://www.bsg.ox.ac.uk/research/research-projects/coronavirus-government-response-tracker"
                                measure.save()
                            except:
                                print("does not exist, create new")
                                measure = CountryMeasure(country=country, type=category, comment = comment,
                                                         source="https://www.bsg.ox.ac.uk/research/research-projects/coronavirus-government-response-tracker", start=start_date, level=level, last_level = last_level)
                                measure.save()
                            last_level = int(col)

                    col_num += 1



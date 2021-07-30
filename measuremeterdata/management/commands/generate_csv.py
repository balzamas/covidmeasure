from measuremeterdata.models.models_ch import CHCanton, CHCases
from measuremeterdata.models.models import CasesDeaths
from riskcalc.models import BELCases
from django.core.management.base import BaseCommand, CommandError
from datetime import date

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            f = open("measuremeter/static/csv/cantons7_october.csv", "w")
            start_date = date(2020, 10, 1)
            cases = CHCases.objects.filter(canton__level=0, date__gte=start_date).order_by("date")
            f.write("Date,Canton,Value\n")
            for day  in cases:
                f.write(f"{day.date},{day.canton.name},{day.incidence_past7days}\n")
            f.close()
        except:
            pass

        try:
            f = open("measuremeter/static/csv/cantons14_start.csv", "w")
            start_date = date(2020, 2, 28)
            cases = CHCases.objects.filter(canton__level=0, date__gte=start_date).order_by("date")
            f.write("Date,Canton,Value\n")
            for day  in cases:
                f.write(f"{day.date},{day.canton.name},{day.incidence_past14days}\n")
            f.close()
        except:
            pass

        try:
            f = open("measuremeter/static/csv/cantons14_july.csv", "w")
            start_date = date(2020, 7, 1)
            cases = CHCases.objects.filter(canton__level=0, date__gte=start_date).order_by("date")
            f.write("Date,Canton,Value\n")
            for day  in cases:
                f.write(f"{day.date},{day.canton.name},{day.incidence_past14days}\n")
            f.close()
        except:
            pass

        try:
            f = open("measuremeter/static/csv/bel14_start.csv", "w")
            start_date = date(2020, 2, 28)
            cases = BELCases.objects.filter(date__gte=start_date).order_by("date")
            f.write("Date,Province,Value\n")
            for day  in cases:
                total_cases = day.cases0_9 + day.cases10_19 + day.cases20_29 + day.cases30_39 + day.cases40_49 + day.cases50_59 + day.cases60_69 + day.cases70_79 + day.cases80_89 + day.cases90plus
                f.write(f"{day.date},{day.province.name},{total_cases}\n")
            f.close()
        except:
            pass

        try:
            f = open("measuremeter/static/csv/bel14_july.csv", "w")
            start_date = date(2020, 7, 1)
            cases = BELCases.objects.filter(date__gte=start_date).order_by("date")
            f.write("Date,Province,Value\n")
            for day  in cases:
                total_cases = day.cases0_9 + day.cases10_19 + day.cases20_29 + day.cases30_39 + day.cases40_49 + day.cases50_59 + day.cases60_69 + day.cases70_79 + day.cases80_89 + day.cases90plus
                f.write(f"{day.date},{day.province.name},{total_cases}\n")
            f.close()
        except:
            pass

        try:
            f = open("measuremeter/static/csv/countries14_start.csv", "w")
            start_date = date(2020, 2, 25)
            cases = CasesDeaths.objects.filter(country__continent=1,date__gte=start_date).order_by("date")
            f.write("Date,Country,Value\n")
            for day  in cases:
                f.write(f"{day.date},{day.country.name},{day.cases_past14days}\n")
            f.close()
        except:
            pass

        try:
            f = open("measuremeter/static/csv/countries14_july.csv", "w")
            start_date = date(2020, 7, 1)
            cases = CasesDeaths.objects.filter(country__continent=1,date__gte=start_date).order_by("date")
            f.write("Date,Country,Value\n")
            for day  in cases:
                f.write(f"{day.date},{day.country.name},{day.cases_past14days}\n")
            f.close()
        except:
            pass

        try:
            f = open("measuremeter/static/csv/countries14_june21.csv", "w")
            start_date = date(2021, 6, 1)
            cases = CasesDeaths.objects.filter(country__continent=1,date__gte=start_date).order_by("date")
            f.write("Date,Country,Value\n")
            for day  in cases:
                f.write(f"{day.date},{day.country.name},{day.cases_past14days}\n")
            f.close()
        except:
            pass

        f = open("measuremeter/static/csv/countries14_october.csv", "w")
        start_date = date(2020, 10, 1)
        cases = CasesDeaths.objects.filter(country__continent=1,date__gte=start_date).order_by("date")
        f.write("Date,Country,Value\n")
        for day  in cases:
            f.write(f"{day.date},{day.country.name},{day.cases_past14days}\n")
        f.close()

        f = open("measuremeter/static/csv/countries7_start.csv", "w")
        start_date = date(2020, 2, 25)
        cases = CasesDeaths.objects.filter(country__continent=1,date__gte=start_date).order_by("date")
        f.write("Date,Country,Value\n")
        for day  in cases:
            f.write(f"{day.date},{day.country.name},{day.cases_past7days}\n")
        f.close()

        f = open("measuremeter/static/csv/countries7_july.csv", "w")
        start_date = date(2020, 7, 1)
        cases = CasesDeaths.objects.filter(country__continent=1,date__gte=start_date).order_by("date")
        f.write("Date,Country,Value\n")
        for day  in cases:
            f.write(f"{day.date},{day.country.name},{day.cases_past7days}\n")
        f.close()

        f = open("measuremeter/static/csv/countries7_june21.csv", "w")
        start_date = date(2021, 6, 1)
        cases = CasesDeaths.objects.filter(country__continent=1,date__gte=start_date).order_by("date")
        f.write("Date,Country,Value\n")
        for day  in cases:
            f.write(f"{day.date},{day.country.name},{day.cases_past7days}\n")
        f.close()

        f = open("measuremeter/static/csv/countries7_october.csv", "w")
        start_date = date(2020, 10, 1)
        cases = CasesDeaths.objects.filter(country__continent=1,date__gte=start_date).order_by("date")
        f.write("Date,Country,Value\n")
        for day  in cases:
            f.write(f"{day.date},{day.country.name},{day.cases_past7days}\n")
        f.close()

        f = open("measuremeter/static/csv/countries7_int_start.csv", "w")
        start_date = date(2020, 2, 25)
        cases = CasesDeaths.objects.filter(date__gte=start_date).order_by("date")
        f.write("Date,Country,Value\n")
        for day  in cases:
            f.write(f"{day.date},{day.country.name},{day.cases_past7days}\n")
        f.close()

        f = open("measuremeter/static/csv/countries7_int_july.csv", "w")
        start_date = date(2020, 7, 1)
        cases = CasesDeaths.objects.filter(date__gte=start_date).order_by("date")
        f.write("Date,Country,Value\n")
        for day  in cases:
            f.write(f"{day.date},{day.country.name},{day.cases_past7days}\n")
        f.close()


        f = open("measuremeter/static/csv/countries14_death_start.csv", "w")
        start_date = date(2020, 3, 20)
        cases = CasesDeaths.objects.filter(country__continent=1,date__gte=start_date).order_by("date")
        f.write("Date,Country,Value\n")
        for day  in cases:
            f.write(f"{day.date},{day.country.name},{day.deaths_past14days}\n")
        f.close()

        f = open("measuremeter/static/csv/countries14_positivity_start.csv", "w")
        start_date = date(2020, 2, 27)
        cases = CasesDeaths.objects.filter(country__continent=1,date__gte=start_date).order_by("date")
        f.write("Date,Country,Value\n")
        for day  in cases:
            if day.positivity == None:
                pos = 0
            else:
                pos = day.positivity

            f.write(f"{day.date},{day.country.name},{pos}\n")
        f.close()



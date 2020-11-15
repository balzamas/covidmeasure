from measuremeterdata.models.models_ch import CHCanton, CHCases
from measuremeterdata.models.models import CasesDeaths
from django.core.management.base import BaseCommand, CommandError
from datetime import date

class Command(BaseCommand):
    def handle(self, *args, **options):
        f = open("measuremeter/static/csv/cantons14_start.csv", "w")
        start_date = date(2020, 2, 28)
        cases = CHCases.objects.filter(canton__level=0, date__gte=start_date).order_by("date")
        f.write("Date,Canton,Value\n")
        for day  in cases:
            f.write(f"{day.date},{day.canton.name},{day.incidence_past14days}\n")
        f.close()

        f = open("measuremeter/static/csv/cantons14_july.csv", "w")
        start_date = date(2020, 7, 1)
        cases = CHCases.objects.filter(canton__level=0, date__gte=start_date).order_by("date")
        f.write("Date,Canton,Value\n")
        for day  in cases:
            f.write(f"{day.date},{day.canton.name},{day.incidence_past14days}\n")
        f.close()

        f = open("measuremeter/static/csv/countries14_start.csv", "w")
        start_date = date(2020, 2, 25)
        cases = CasesDeaths.objects.filter(country__continent=1,date__gte=start_date).order_by("date")
        f.write("Date,Country,Value\n")
        for day  in cases:
            f.write(f"{day.date},{day.country.name},{day.cases_past14days}\n")
        f.close()

        f = open("measuremeter/static/csv/countries14_july.csv", "w")
        start_date = date(2020, 7, 1)
        cases = CasesDeaths.objects.filter(country__continent=1,date__gte=start_date).order_by("date")
        f.write("Date,Country,Value\n")
        for day  in cases:
            f.write(f"{day.date},{day.country.name},{day.cases_past14days}\n")
        f.close()

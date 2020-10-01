from pylab import figure, axes, pie, title, show
from django.core.management.base import BaseCommand, CommandError
from matplotlib import pyplot as plt
from measuremeterdata.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths, CHCanton, CHCases
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not os.path.exists('measuremeter/static/images/graphs_world/'):
            os.makedirs('measuremeter/static/images/graphs_world/')
        for country in Country.objects.all():
            print(country)
            print(".....")

            cases = []
            dates = []

            for day in CasesDeaths.objects.filter(country=country).order_by('-date')[:31]:
                if (day.cases_past14days is not None):
                    cases.append(int(day.cases_past14days))
                    dates.append(day.date)

            plt.figure()

            fig, ax = plt.subplots()
            ax.plot(dates, cases)

            fig.patch.set_visible(False)
            ax.axis('off')

            #plt.xlabel("Age")
            #plt.ylabel("Total Population")
            #plt.title("Cases per 100k/past 7 days")
            plt.tight_layout()

            plt.fill_between(dates, cases)

            #plt.ylim(0, 850)

            figure = plt.gcf()

            figure.set_size_inches(2, 1)

            frame1 = plt.gca()
            frame1.axes.get_xaxis().set_visible(False)
            frame1.axes.get_yaxis().set_visible(False)



            plt.savefig(f'measuremeter/static/images/graphs_world/{country.code}.png', dpi=100)
            plt.close()

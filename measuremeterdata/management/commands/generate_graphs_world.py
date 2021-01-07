from pylab import figure, axes, pie, title, show
from django.core.management.base import BaseCommand, CommandError
from matplotlib import pyplot as plt
from measuremeterdata.models.models import Country, MeasureCategory, MeasureType_old, Measure_old, Continent, CasesDeaths
import os

def write_graph(country,dates, data, suffix, ymax):
    plt.figure()

    fig, ax = plt.subplots()
    ax.plot(dates, data, color='#fed1a4')

    fig.patch.set_visible(False)
    ax.axis('off')

    # plt.xlabel("Age")
    # plt.ylabel("Total Population")
    # plt.title("Cases per 100k/past 7 days")
    plt.tight_layout()

    plt.fill_between(dates, data, color='#fed1a4')

    plt.ylim(0, ymax)

    figure = plt.gcf()

    figure.set_size_inches(2, 1)

    frame1 = plt.gca()
    frame1.axes.get_xaxis().set_visible(False)
    frame1.axes.get_yaxis().set_visible(False)

    plt.savefig(f'measuremeter/static/images/graphs_world/{country.code}_{suffix}.png', dpi=100)
    plt.close()

class Command(BaseCommand):
    def handle(self, *args, **options):
        for country in Country.objects.all():
            print(country)
            print(".....")

            cases = []
            deaths = []
            positivity = []
            dates = []
            dates_positivity = []
            largest_pos = 5

            for day in CasesDeaths.objects.filter(country=country).order_by('-date')[:61]:
                if (day.cases_past14days is not None and day.deaths_past14days is not None):
                    cases.append(int(day.cases_past14days))
                    deaths.append(float(day.deaths_past14days))
                    dates.append(day.date)
                    if (day.positivity is not None):
                        if (day.positivity > largest_pos):
                            largest_pos = day.positivity
                        positivity.append(float(day.positivity))
                        dates_positivity.append(day.date)

            if (len(cases) > 0):
                write_graph(country, dates, cases,  "cases", None)
            if (len(deaths) > 0):
                write_graph(country, dates, deaths, "deaths", None)
            if (len(positivity) > 0):
                write_graph(country, dates_positivity, positivity, "positivity", largest_pos)



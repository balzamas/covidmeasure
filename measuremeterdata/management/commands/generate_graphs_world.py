from pylab import figure, axes, pie, title, show
from django.core.management.base import BaseCommand, CommandError
from matplotlib import pyplot as plt
from measuremeterdata.models.models import Country, Continent, CasesDeaths
import os
from measuremeterdata.tasks.importer.world.generate_graphs_world import generate

class Command(BaseCommand):
    def handle(self, *args, **options):
        generate()


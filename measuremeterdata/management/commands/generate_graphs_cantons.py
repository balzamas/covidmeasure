from pylab import figure, axes, pie, title, show
from django.core.management.base import BaseCommand, CommandError
from matplotlib import pyplot as plt
from measuremeterdata.models.models_ch import CHCanton, CHCases
from measuremeterdata.tasks.importer.ch.generate_graphs_cantons import generate
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        generate()

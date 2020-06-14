from django.shortcuts import render
from .models import Measure, Country, MeasureType, MeasureCategory, CasesDeaths
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import MeasureSerializer, CountrySerializer, MeasureTypeSerializer, MeasureCategorySerializer,CasesDeathsSerializer
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
import datetime

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

from django_filters import rest_framework as filters

class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass

class DateFilter(filters.BaseInFilter, filters.DateFilter):
    pass

class MeasureTypeFilter(filters.FilterSet):
     pk = NumberInFilter(field_name='pk', lookup_expr='in')

class CountryFilter(filters.FilterSet):
    pk = NumberInFilter(field_name='pk', lookup_expr='in')

class CasesDeathsFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter(field_name='date')

class MeasureFilter(filters.FilterSet):
    country = NumberInFilter(field_name='country')
    type = NumberInFilter(field_name='type')
    start = filters.DateFilter(field_name='start')
    end = filters.DateFilter(field_name='end')
    level = filters.DateFilter(field_name='level')


def get_queryset(self):
        countries = self.request.query_params.get('country')
        types = self.request.query_params.get('type')
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        levels = self.request.query_params.get('level')
        measures = Measure.objects
        if countries:
            measures.filter(country__in=countries)  # returned queryset filtered by ids
        if type:
            measures.filter(type__in=types)  # returned queryset filtered by ids
        if start:
            measures.filter(start__lte=start)  # returned queryset filtered by ids
        if end:
            measures.filter(end__gte=end)  # returned queryset filtered by ids
        if levels:
            measures.filter(level__in=levels)  # returned queryset filtered by ids

        measures.order_by('country__name', 'type__category','type__name')

        return measures  # return whole queryset

        class Meta:
            model = Measure
            fields = ['country', 'type', 'start', 'end', 'level']

class MeasureViewSet(viewsets.ModelViewSet):
    queryset = Measure.objects.filter(type__isactive=True).order_by('country__name', 'type__category','type__name')
    serializer_class = MeasureSerializer
#    filter_backends = [DjangoFilterBackend]
#    filter_class = MeasureFilter

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        queryset = Measure.objects
        countries = self.request.query_params.get('country', None)
        types = self.request.query_params.get('type', None)
        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', None)
        levels = self.request.query_params.get('level')
        if countries and countries != '' and types != ',':
            print(countries)
            country_params = []
            for x in countries.split(','):
                if (x != ''):
                    country_params.append(x)
            queryset = queryset.filter(country__in=country_params)

        if types != None and types != '' and types != ',':
            type_params = []
            for x in types.split(','):
                if (x != ''):
                    type_params.append(x)
            queryset = queryset.filter(type__in=type_params)

        if start != None:
            queryset = queryset.filter(Q(start__lte=start)|Q(start__isnull=True))

        if end != None:
            queryset = queryset.filter(Q(end__gt=end)|Q(end__isnull=True))

        if levels != None and levels != '' and types != ',':
            level_params = []
            for x in levels.split(','):
                if (x != ''):
                    level_params.append(x)
            queryset = queryset.filter(level__in=level_params)

        queryset = queryset.filter(type__isactive=True).order_by('country__name', 'type__category__name','type__name')
        return queryset

class MeasureByMeasureViewSet(viewsets.ModelViewSet):
    queryset = Measure.objects.filter(type__isactive=True).order_by('country__name', 'type__category__name','type__name' )
    serializer_class = MeasureSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = MeasureFilter

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all().order_by('name')
    serializer_class = CountrySerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = CountryFilter

class MeasureTypeViewSet(viewsets.ModelViewSet):
    queryset = MeasureType.objects.filter(isactive=True).order_by('category','name')
    serializer_class = MeasureTypeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = MeasureTypeFilter

class MeasureCategoryViewSet(viewsets.ModelViewSet):
    queryset = MeasureCategory.objects.all().order_by('name')
    serializer_class = MeasureCategorySerializer

class CasesDeathsViewSet(viewsets.ModelViewSet):
    queryset = CasesDeaths.objects
    serializer_class = CasesDeathsSerializer

    def get_queryset(self):
        queryset = CasesDeaths.objects
        countries = self.request.query_params.get('country')
        date_after = self.request.query_params.get('date_after')
        date_before = self.request.query_params.get('date_before')

        if countries and date_after and date_before:
            print(countries)
            country_params = []
            for x in countries.split(','):
                if (x != ''):
                    country_params.append(x)
            print(country_params)
            queryset = queryset.filter(country__in=country_params, date__range=[date_after, date_before]).order_by('date','country')

        print(queryset)

        return queryset  # return whole queryset

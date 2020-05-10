from django.shortcuts import render
from .models import Measure, Country, MeasureType, MeasureCategory
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import MeasureSerializer, CountrySerializer, MeasureTypeSerializer, MeasureCategorySerializer
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

class MeasureFilter(filters.FilterSet):
#    country = NumberInFilter(field_name='country', lookup_expr='in')
#    type = NumberInFilter(field_name='type', lookup_expr='in')
#    start = filters.DateFilter(lookup_expr="lte")
#    end = filters.DateFilter(lookup_expr="gte")
    country = NumberInFilter(field_name='country')
    type = NumberInFilter(field_name='type')
    start = filters.DateFilter(field_name='start')
    end = filters.DateFilter(field_name='end')

    def get_queryset(self):
        countries = self.request.query_params.get('country')
        types = self.request.query_params.get('type')
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        measures = Measure.objects.all()
        if countries:
            measures.filter(country__in=countries)  # returned queryset filtered by ids
        if type:
            measures.filter(type__in=types)  # returned queryset filtered by ids
        if start:
            measures.filter(start__lte=start)  # returned queryset filtered by ids
        if end:
            measures.filter(end__gt=end)  # returned queryset filtered by ids
        return measures  # return whole queryset

    class Meta:
        model = Measure
        fields = ['country', 'type', 'start', 'end']

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
        queryset = Measure.objects.all()
        countries = self.request.query_params.get('country', None)
        types = self.request.query_params.get('type', None)
        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', None)
        print("XENA")
        if countries is not None and countries is not '' and types is not ',':
            print(countries)
            country_params = []
            for x in countries.split(','):
                if (x is not ''):
                    country_params.append(x)
            queryset = queryset.filter(country__in=country_params)

        if types is not None and types is not '' and types is not ',':
            type_params = []
            for x in types.split(','):
                if (x is not ''):
                    type_params.append(x)
            queryset = queryset.filter(type__in=type_params)

        if start is not None:
            queryset = queryset.filter(Q(start__lte=start)|Q(start__isnull=True))

        if end is not None:
            queryset = queryset.filter(Q(end__gt=end)|Q(end__isnull=True))

        queryset = queryset.filter(type__isactive=True).order_by('country__name', 'type__category','type__name')
        return queryset

class MeasureByMeasureViewSet(viewsets.ModelViewSet):
    queryset = Measure.objects.filter(type__isactive=True).order_by('type__category','type__name', 'country__name')
    serializer_class = MeasureSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = MeasureFilter

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all().order_by('name')
    serializer_class = CountrySerializer

class MeasureTypeViewSet(viewsets.ModelViewSet):
    queryset = MeasureType.objects.filter(isactive=True).order_by('category','name')
    serializer_class = MeasureTypeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = MeasureTypeFilter

class MeasureCategoryViewSet(viewsets.ModelViewSet):
    queryset = MeasureCategory.objects.all().order_by('name')
    serializer_class = MeasureCategorySerializer

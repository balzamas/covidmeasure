from django.shortcuts import render
from .models import Measure, Country, MeasureType, MeasureCategory
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import MeasureSerializer, CountrySerializer, MeasureTypeSerializer, MeasureCategorySerializer
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
import datetime

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

from django_filters import rest_framework as filters

class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass

class DateFilter(filters.BaseInFilter, filters.DateFilter):
    pass

class MeasureFilter(filters.FilterSet):
    country = NumberInFilter(field_name='country', lookup_expr='in')
    type = NumberInFilter(field_name='type', lookup_expr='in')
    start = filters.DateFilter(lookup_expr="lte")
    end = filters.DateFilter(lookup_expr="gte")

    class Meta:
        model = Measure
        fields = ['country', 'type', 'start', 'end']

class MeasureViewSet(viewsets.ModelViewSet):
    queryset = Measure.objects.filter(type__isactive=True).order_by('country__name', 'type__category','type__name')
    serializer_class = MeasureSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = MeasureFilter

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

class MeasureCategoryViewSet(viewsets.ModelViewSet):
    queryset = MeasureCategory.objects.all().order_by('name')
    serializer_class = MeasureCategorySerializer

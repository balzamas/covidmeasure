from django.shortcuts import render
from .models import Measure, Country, MeasureType, MeasureCategory
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import MeasureSerializer, CountrySerializer, MeasureTypeSerializer, MeasureCategorySerializer
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

from django_filters import rest_framework as filters

class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass

class MeasureFilter(filters.FilterSet):
    country_in = NumberInFilter(field_name='country', lookup_expr='in')
    type_in = NumberInFilter(field_name='type', lookup_expr='in')

    class Meta:
        model = Measure
        fields = ['country_in', 'type_in']

class MeasureViewSet(viewsets.ModelViewSet):
    queryset = Measure.objects.all().order_by('country__name', 'type__category','type__name')
    serializer_class = MeasureSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = MeasureFilter
    permission_classes = [permissions.IsAuthenticated]

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all().order_by('name')
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAuthenticated]

class MeasureTypeViewSet(viewsets.ModelViewSet):
    queryset = MeasureType.objects.all().order_by('category','name')
    serializer_class = MeasureTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class MeasureCategoryViewSet(viewsets.ModelViewSet):
    queryset = MeasureCategory.objects.all().order_by('name')
    serializer_class = MeasureCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

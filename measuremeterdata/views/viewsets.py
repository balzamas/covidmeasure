from django.shortcuts import render
from measuremeterdata.models.models import Country, MeasureCategory, CasesDeaths, CountryMeasure, CountryMeasureType
from measuremeterdata.models.models_ch import CHCanton, CHMeasureType, CHMeasure, CHCases, CHDeaths
from rest_framework import viewsets
from rest_framework import permissions
from measuremeterdata.serializers.serializers_ch import CHMeasureTypeSerializer, CantonSerializer, CHMeasureSerializer, CHCasesSerializer, CHMeasurePublicSerializer, CHMeasureTypePublicSerializer, CantonPublicSerializer, CHDeathsPublicSerializer
from measuremeterdata.serializers.serializers_int import MeasureSerializer, CountrySerializer, MeasureTypeSerializer, MeasureCategorySerializer,CasesDeathsSerializer, OxfordMeasureSerializer, OxfordMeasureTypeSerializer
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
    http_method_names = ['get', 'head']

class CountryFilter(filters.FilterSet):
    pk = NumberInFilter(field_name='pk', lookup_expr='in')
    http_method_names = ['get', 'head']

class CasesDeathsFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter(field_name='date')
    http_method_names = ['get', 'head']

class CHCasesFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter(field_name='date')
    http_method_names = ['get', 'head']

class MeasureFilter(filters.FilterSet):
    country = NumberInFilter(field_name='country')
    type = NumberInFilter(field_name='type')
    start = filters.DateFilter(field_name='start')
    end = filters.DateFilter(field_name='end')
    level = filters.DateFilter(field_name='level')
    http_method_names = ['get', 'head']


def get_queryset(self):
        countries = self.request.query_params.get('country')
        types = self.request.query_params.get('type')
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        levels = self.request.query_params.get('level')
        measures = CountryMeasure.objects
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

        measures.order_by('country__name', 'type__name')

        return measures  # return whole queryset

        class Meta:
            model = CountryMeasure
            fields = ['country', 'type', 'start', 'end', 'level']

class MeasureViewSet(viewsets.ModelViewSet):
    queryset = CountryMeasure.objects.filter(type__isactive=True).order_by('country__name', 'type__name')
    serializer_class = MeasureSerializer
    http_method_names = ['get', 'head']

#    filter_backends = [DjangoFilterBackend]
#    filter_class = MeasureFilter

    def get_queryset(self):
        queryset = CountryMeasure.objects
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
            queryset = queryset.filter(Q(end__gte=end)|Q(end__isnull=True))

        if levels != None and levels != '' and types != ',':
            level_params = []
            for x in levels.split(','):
                if (x != ''):
                    level_params.append(x)
            queryset = queryset.filter(level__in=level_params)

        queryset = queryset.filter(type__isactive=True).order_by('country__name', 'type__name')
        return queryset

class OxfordMeasureViewSet(viewsets.ModelViewSet):
    queryset = CountryMeasure.objects.filter(type__isactive=True).order_by('country__name', 'type__name')
    serializer_class = OxfordMeasureSerializer
    http_method_names = ['get', 'head']

#    filter_backends = [DjangoFilterBackend]
#    filter_class = MeasureFilter

    def get_queryset(self):
        queryset = CountryMeasure.objects
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
            queryset = queryset.filter(Q(end__gte=end)|Q(end__isnull=True))

        if levels != None and levels != '' and types != ',':
            level_params = []
            for x in levels.split(','):
                if (x != ''):
                    level_params.append(x)
            queryset = queryset.filter(level__in=level_params)

        queryset = queryset.filter(type__isactive=True).order_by('country__name', 'type__name')
        return queryset

class MeasureByMeasureViewSet(viewsets.ModelViewSet):
    queryset = CountryMeasure.objects.filter(type__isactive=True).order_by('country__name', 'type__name')
    serializer_class = MeasureSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = MeasureFilter
    http_method_names = ['get', 'head']

class CountryWithMeasuresViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.filter(has_measures=True).order_by('name')
    serializer_class = CountrySerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = CountryFilter
    http_method_names = ['get', 'head']

class MeasureTypeViewSet(viewsets.ModelViewSet):
    queryset = CountryMeasureType.objects.filter(isactive=True).order_by('name')
    serializer_class = MeasureTypeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = MeasureTypeFilter
    http_method_names = ['get', 'head']

class OxfordMeasureTypeViewSet(viewsets.ModelViewSet):
    queryset = CountryMeasureType.objects.filter(isactive=True).order_by('name')
    serializer_class = OxfordMeasureTypeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = MeasureTypeFilter
    http_method_names = ['get', 'head']


class MeasureCategoryViewSet(viewsets.ModelViewSet):
    queryset = MeasureCategory.objects.all().order_by('name')
    serializer_class = MeasureCategorySerializer
    http_method_names = ['get', 'head']

class CasesDeathsViewSet(viewsets.ModelViewSet):
    queryset = CasesDeaths.objects
    serializer_class = CasesDeathsSerializer
    http_method_names = ['get', 'head']

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
            queryset = queryset.filter(country__in=country_params, date__range=[date_after, date_before]).order_by('country__name','date')

        print(queryset)

        return queryset  # return whole queryset


class CHCasesViewSet(viewsets.ModelViewSet):
    queryset = CHCases.objects
    serializer_class = CHCasesSerializer
    http_method_names = ['get', 'head']

    def get_queryset(self):
        queryset = CHCases.objects
        date_after = self.request.query_params.get('date_after')
        date_before = self.request.query_params.get('date_before')
        cantons = self.request.query_params.get('canton', None)
        number = self.request.query_params.get('nr', None)
        level = self.request.query_params.get('level', None)

        if cantons and cantons != '':
            print(cantons)
            canton_params = []
            for x in cantons.split(','):
                if (x != ''):
                    canton_params.append(x)
            queryset = queryset.filter(canton__in=canton_params)

        if number and number != '':
            number_params = []
            for x in number.split(','):
                if (x != ''):
                    number_params.append(x)
            queryset = queryset.filter(canton__swisstopo_id__in=number_params)


        if level and level != '':
            queryset = queryset.filter(canton__level=level)

        if date_after and date_before:
            queryset = queryset.filter(date__range=[date_after, date_before]).order_by('canton__code','date')

        print(queryset)

        return queryset  # return whole queryset


class CHMeasureTypeFilter(filters.FilterSet):
    pk = NumberInFilter(field_name='pk', lookup_expr='in')
    http_method_names = ['get', 'head']

class CHCantonFilter(filters.FilterSet):
    pk = NumberInFilter(field_name='pk', lookup_expr='in')
    http_method_names = ['get', 'head']

class CHCantonViewSet(viewsets.ModelViewSet):
    queryset = CHCanton.objects.filter(level=0).order_by('name')
    serializer_class = CantonSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = CHCantonFilter
    http_method_names = ['get', 'head']

class CHMeasureTypeViewSet(viewsets.ModelViewSet):
    queryset = CHMeasureType.objects.filter(isactive=True).order_by('name')
    serializer_class = CHMeasureTypeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = CHMeasureTypeFilter
    http_method_names = ['get', 'head']

class CHMeasureFilter(filters.FilterSet):
    canton = NumberInFilter(field_name='canton')
    type = NumberInFilter(field_name='type')
    start = filters.DateFilter(field_name='start')
    end = filters.DateFilter(field_name='end')
    level = filters.DateFilter(field_name='level')
    http_method_names = ['get', 'head']


    def get_queryset(self):
            cantons = self.request.query_params.get('canton')
            types = self.request.query_params.get('type')
            start = self.request.query_params.get('start')
            end = self.request.query_params.get('end')
            levels = self.request.query_params.get('level')
            measures = CountryMeasure.objects
            if cantons:
                measures.filter(canton__in=cantons)  # returned queryset filtered by ids
            if type:
                measures.filter(type__in=types)  # returned queryset filtered by ids
            if start:
                measures.filter(start__lte=start)  # returned queryset filtered by ids
            if end:
                measures.filter(end__gte=end)  # returned queryset filtered by ids
            if levels:
                measures.filter(level__in=levels)  # returned queryset filtered by ids

            measures.order_by('canton__name', 'type__name', 'start')

            return measures  # return whole queryset

            class Meta:
                model = CountryMeasure
                fields = ['canton', 'type', 'start', 'end', 'level']

class CHMeasureViewSet(viewsets.ModelViewSet):
    queryset = CHMeasure.objects.filter(type__isactive=True).order_by('canton__code','type__name', 'start')
    serializer_class = CHMeasureSerializer
    http_method_names = ['get', 'head']

#    filter_backends = [DjangoFilterBackend]
#    filter_class = MeasureFilter

    def get_queryset(self):
        queryset = CHMeasure.objects
        cantons = self.request.query_params.get('canton', None)
        types = self.request.query_params.get('type', None)
        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', None)
        levels = self.request.query_params.get('level')
        if cantons and cantons != '' and types != ',':
            print(cantons)
            canton_params = []
            for x in cantons.split(','):
                if (x != ''):
                    canton_params.append(x)
            queryset = queryset.filter(canton__in=canton_params)

        if types != None and types != '' and types != ',':
            type_params = []
            for x in types.split(','):
                if (x != ''):
                    type_params.append(x)
            queryset = queryset.filter(type__in=type_params)

        if start != None:
            queryset = queryset.filter(Q(start__lte=start)|Q(start__isnull=True))

        if end != None:
            queryset = queryset.filter(Q(end__gte=end)|Q(end__isnull=True))

        if levels != None and levels != '' and types != ',':
            level_params = []
            for x in levels.split(','):
                if (x != ''):
                    level_params.append(x)
            queryset = queryset.filter(level__in=level_params)

        queryset = queryset.filter(type__isactive=True).order_by('canton__code','type__name', 'start')
        return queryset

class CHMeasureTypePublicViewSet(viewsets.ModelViewSet):
    queryset = CHMeasureType.objects.filter(isactive=True).order_by('name')
    serializer_class = CHMeasureTypePublicSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = CHMeasureTypeFilter
    http_method_names = ['get', 'head']


class CHMeasurePublicViewset(viewsets.ModelViewSet):
    queryset = CHMeasure.objects.filter(type__isactive=True).order_by('canton__code', 'type__name', 'start')
    serializer_class = CHMeasurePublicSerializer
    http_method_names = ['get', 'head']

    def get_queryset(self):
        queryset = CHMeasure.objects
        cantons = self.request.query_params.get('cantons', None)
        types = self.request.query_params.get('types', None)
        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', None)
        levels = self.request.query_params.get('level')
        if cantons and cantons != '' and types != ',':
            print(cantons)
            canton_params = []
            for x in cantons.split(','):
                if (x != ''):
                    if (x == "ch"):
                        canton = CHCanton.objects.get(code=x)
                    else:
                        canton = CHCanton.objects.get(code=x, level=0)
                    canton_params.append(canton.pk)
            queryset = queryset.filter(canton__in=canton_params)

        if types != None and types != '' and types != ',':
            type_params = []
            for x in types.split(','):
                if (x != ''):
                    type_params.append(x)
            queryset = queryset.filter(type__in=type_params)

        if start != None:
            queryset = queryset.filter(Q(start__lte=start) | Q(start__isnull=True))

        if end != None:
            queryset = queryset.filter(Q(end__gte=end) | Q(end__isnull=True))

        if levels != None and levels != '' and types != ',':
            level_params = []
            for x in levels.split(','):
                if (x != ''):
                    level_params.append(x)
            queryset = queryset.filter(level__in=level_params)

        queryset = queryset.filter(type__isactive=True).order_by('canton__code', 'type__name', 'start')
        return queryset


class CHDeathsPublicViewset(viewsets.ModelViewSet):
    queryset = CHDeaths.objects.order_by('canton__code', 'week')
    serializer_class = CHDeathsPublicSerializer
    http_method_names = ['get', 'head']

    def get_queryset(self):
        queryset = CHDeaths.objects
        cantons = self.request.query_params.get('cantons', None)
        if cantons and cantons != '':
            print(cantons)
            canton_params = []
            for x in cantons.split(','):
                if (x != ''):
                    if (x == "ch"):
                        canton = CHCanton.objects.get(code=x)
                    else:
                        canton = CHCanton.objects.get(code=x, level=0)
                    canton_params.append(canton.pk)
            queryset = queryset.filter(canton__in=canton_params)

        queryset = queryset.order_by('canton__code', 'week')
        return queryset

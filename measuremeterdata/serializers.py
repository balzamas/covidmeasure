from .models import Measure, Country, MeasureType, MeasureCategory, CasesDeaths, CHCanton, CHMeasure, CHMeasureType, CHCases
from rest_framework import serializers


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['pk', 'name', 'code', 'iso_code', 'link_dashboard', 'link_worldometer','link_gov', 'comment',  'continent', 'average_death_per_day','average_death_per_day_peak', 'avg_desc', 'avg_peak_desc', 'source_death', 'population', 'has_measures']

class CasesDeathsSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    class Meta:
        model = CasesDeaths
        fields = ['pk', 'country', 'date', 'deaths', 'cases', 'deathstotal', 'deaths_past14days', 'cases_past14days', 'deaths_per100k', 'deaths_total_per100k', 'cases_past7days', 'positivity']

class MeasureCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureCategory
        fields = ['pk','name']

class MeasureTypeSerializer(serializers.ModelSerializer):
    category = MeasureCategorySerializer()
    class Meta:
        model = MeasureType
        fields = ['pk', 'name', 'category', 'isactive', 'tooltip_nonpartial','tooltip_partial', 'comment', 'icon']

class MeasureSerializer(serializers.ModelSerializer):
    type = MeasureTypeSerializer()
    country = CountrySerializer()
    class Meta:
        model = Measure
        fields = ['country', 'type', 'level', 'start', 'end', 'sources', 'comment', 'isregional', 'created', 'updated']

class CantonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CHCanton
        fields = ['pk', 'name', 'code', 'population', 'swisstopo_id', 'level']


class CHMeasureTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CHMeasureType
        fields = ['pk', 'name', 'isactive', 'tooltip_level1','tooltip_level2','tooltip_level3','tooltip_level4', 'comment', 'icon']

class CHMeasureSerializer(serializers.ModelSerializer):
    type = CHMeasureTypeSerializer()
    canton = CantonSerializer()
    class Meta:
        model = CHMeasure
        fields = ['canton', 'type', 'level', 'start', 'end', 'sources', 'comment', 'isregional', 'created', 'updated']

class CHCasesSerializer(serializers.ModelSerializer):
    canton = CantonSerializer()
    class Meta:
        model = CHCases
        fields = ['pk', 'canton', 'date', 'cases', 'incidence_past14days', 'incidence_past10days', 'incidence_past7days']

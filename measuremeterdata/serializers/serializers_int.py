from measuremeterdata.models.models import Country, MeasureCategory, CasesDeaths, CountryMeasure, CountryMeasureType
from rest_framework import serializers


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['pk', 'name', 'code', 'iso_code', 'link_dashboard', 'link_worldometer','link_gov', 'comment',  'continent', 'average_death_per_day','average_death_per_day_peak', 'avg_desc', 'avg_peak_desc', 'source_death', 'population', 'has_measures', 'peak_year']

class CasesDeathsSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    class Meta:
        model = CasesDeaths
        fields = ['pk', 'country', 'date', 'deaths', 'cases', 'deathstotal', 'deaths_past14days', 'deaths_past7days','cases_past14days', 'cases_past7days', 'positivity', 'development7to7', 'r0peak', 'r0low', 'r0median', 'tests', 'tests_smoothed_per_thousand', 'stringency_index', 'death_to_cases']

class MeasureCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureCategory
        fields = ['pk','name']

class MeasureTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryMeasureType
        fields = ['pk', 'name', 'isactive', 'text_level0','text_level1','text_level2','text_level3','text_level4','code', 'icon']

class MeasureSerializer(serializers.ModelSerializer):
    type = MeasureTypeSerializer()
    country = CountrySerializer()
    class Meta:
        model = CountryMeasure
        fields = ['country', 'type', 'level', 'start', 'end', 'source', 'comment', 'isregional', 'created', 'updated']

class OxfordMeasureTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryMeasureType
        fields = ['pk', 'name', 'isactive', 'text_level0', 'text_level1', 'text_level2', 'text_level3', 'text_level4','icon']

class OxfordMeasureSerializer(serializers.ModelSerializer):
    type = OxfordMeasureTypeSerializer()
    country = CountrySerializer()
    class Meta:
        model = CountryMeasure
        fields = ['country', 'type', 'level', 'last_level', 'start', 'end', 'comment', 'isregional', 'source','created', 'updated']

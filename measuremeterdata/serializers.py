from .models import Measure, Country, MeasureType, MeasureCategory, CasesDeaths
from rest_framework import serializers


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['pk', 'name', 'code', 'link_worldometer','link_gov', 'comment',  'mapcode_europe', 'continent', 'average_death_per_day','average_death_per_day_peak', 'avg_desc', 'avg_peak_desc', 'source_death', 'population']

class CasesDeathsSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    class Meta:
        model = CasesDeaths
        fields = ['pk', 'country', 'date', 'deaths', 'cases', 'deathstotal', 'cases_per_mio', 'cases_per_mio_seven']

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

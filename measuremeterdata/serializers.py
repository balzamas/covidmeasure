from .models import Measure, Country, MeasureType, MeasureCategory
from rest_framework import serializers


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name', 'code']

class MeasureTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureType
        fields = ['name', 'category']

class MeasureCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureCategory
        fields = ['name']

class MeasureSerializer(serializers.ModelSerializer):
    type = MeasureTypeSerializer()
    country = CountrySerializer()
    class Meta:
        model = Measure
        fields = ['country', 'type', 'start', 'end', 'source', 'isregional']

from measuremeterdata.models.models_ch import CHCanton, CHMeasure, CHMeasureType, CHCases
from rest_framework import serializers

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
        fields = ['pk', 'canton', 'date', 'cases', 'incidence_past14days', 'incidence_past10days', 'incidence_past7days', 'development7to7']


class CHMeasureTypePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = CHMeasureType
        fields = ['pk', 'name', 'isactive', 'comment']

class CantonPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = CHCanton
        fields = ['name', 'code']

class CHMeasurePublicSerializer(serializers.ModelSerializer):
    type = CHMeasureTypePublicSerializer()
    canton = CantonPublicSerializer()
    class Meta:
        model = CHMeasure
        fields = ['canton', 'type', 'level', 'start', 'end', 'sources', 'comment', 'created', 'updated']



from rest_framework import serializers

from dash.models import EventClass, Metric

class EventClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventClass
        fields = ('name', 'label', 'is_prolonged')

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ('name', 'label')


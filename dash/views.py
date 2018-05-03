from django.shortcuts import render

from rest_framework import viewsets

from dash.models import EventClass, Metric
from dash.serializers import EventClassSerializer, MetricSerializer

class EventClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EventClass.objects.all()
    serializer_class = EventClassSerializer

class MetricViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer

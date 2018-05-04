from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/events/(?P<eventclass>[\w\d_-]+)/(?P<frequency>\d+)/$', consumers.EventsFrequencyConsumer),
    url(r'^ws/metrics/(?P<label>[\w\d_-]+)/(?P<frequency>\d+)/$', consumers.MetricConsumer),
]

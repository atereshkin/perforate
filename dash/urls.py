from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from dash import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'eventclasses', views.EventClassViewSet)
router.register(r'metrics', views.MetricViewSet)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^', include(router.urls))
]

from django.db import models

class Event(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    eventclass = models.CharField(max_length=512)
    value = models.CharField(max_length=8192)

    # Events can be timed (http request, sql query etc) and untimed (connection)
    duration = models.PositiveIntegerField(null=True, blank=True)

class Tag(models.Model):
    events = models.ManyToManyField(Event)
    key = models.CharField(max_length=1024)
    value = models.CharField(max_length=8192)

class Measurement(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    metric = models.CharField(max_length=512)
    value = models.PositiveIntegerField()

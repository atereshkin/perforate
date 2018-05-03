from django.db import models


class EventClass(models.Model):
    name = models.CharField(max_length=2048)
    label = models.CharField(max_length=1024)
    is_prolonged = models.BooleanField()

class Event(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    eventclass = models.ForeignKey(EventClass, on_delete=models.CASCADE)
    value = models.CharField(max_length=8192)

    # Events can be timed (http request, sql query etc) and untimed (connection)
    duration = models.PositiveIntegerField(null=True, blank=True)

class Tag(models.Model):
    events = models.ManyToManyField(Event)
    key = models.CharField(max_length=1024)
    value = models.CharField(max_length=8192)



class Metric(models.Model):
    name = models.CharField(max_length=2048)
    label = models.CharField(max_length=1024)


class Measurement(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()


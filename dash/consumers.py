import json
import time
import asyncio
from datetime import timedelta

from django.utils import timezone

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from dash.models import Event, Measurement

class EventsFrequencyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.connected = True
        self.eventclass = self.scope['url_route']['kwargs']['eventclass']
        self.frequency = int(self.scope['url_route']['kwargs']['frequency'])
        loop = asyncio.get_event_loop()
        loop.create_task(self.produce_values())


    def compute_average(self, at):
        return Event.objects.filter(eventclass__label=self.eventclass,
                                    timestamp__gte=at - timedelta(seconds=self.frequency)).count() / self.frequency
        
    async def produce_values(self):        
        while self.connected:
            at = timezone.now()
            await self.send(text_data=json.dumps({
                'average' : await database_sync_to_async(self.compute_average)(at),
                'timestamp' : time.mktime(at.timetuple())
            }))
            await asyncio.sleep(self.frequency)
            

    async def disconnect(self, close_code):
        self.connected = False

    async def receive(self, text_data):
        print(text_data)


class MetricConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.connected = True
        self.metric = self.scope['url_route']['kwargs']['label']
        self.frequency = int(self.scope['url_route']['kwargs']['frequency'])
        loop = asyncio.get_event_loop()
        loop.create_task(self.produce_values())


    def get_last_measurement(self):
        return Measurement.objects.filter(metric__label=self.metric).latest('id')
        
    async def produce_values(self):        
        while self.connected:
            m = await database_sync_to_async(self.get_last_measurement)()
            await self.send(text_data=json.dumps({
                'value' : m.value,
                'timestamp' : time.mktime(m.timestamp.timetuple())
            }))
            await asyncio.sleep(self.frequency)
            

    async def disconnect(self, close_code):
        self.connected = False

    async def receive(self, text_data):
        print(text_data)

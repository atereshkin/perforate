import logging

import zmq

from django.core.management.base import BaseCommand, CommandError

from dash.models import Event, EventClass, Metric, Measurement

from perforate import perforate_pb2

log = logging.getLogger('perforate.listener')

class Command(BaseCommand):
    help = 'Starts the Perforate daemon listening for events'

    def add_arguments(self, parser):
        parser.add_argument('--host', dest='host', action='store',
                            default='127.0.0.1',
                            help='The IP address/hostname to listen on')
        parser.add_argument('--port', dest='port', action='store', type=int,
                            default='14541',
                            help='The port to listen on')        

    def handle(self, *args, **options):       
        context = zmq.Context.instance()
        socket = context.socket(zmq.SUB)
        socket.bind("tcp://%s:%d"%(options['host'], options['port']))
        socket.setsockopt(zmq.SUBSCRIBE, b'')
        eventclasses = {}
        metrics = {}

        while True:
            raw_msg = socket.recv()
            msg = perforate_pb2.Message.FromString(raw_msg)
            msgtype = msg.WhichOneof('content')
            try:
                if msgtype == 'event':
                    Event.objects.create(eventclass=eventclasses[msg.event.class_session_code],
                                         value=msg.event.value,
                                         duration=msg.event.duration)
                elif msgtype == 'eventclass':
                    ec, created = EventClass.objects.get_or_create(label=msg.eventclass.label,
                                                                   defaults={'name' : msg.eventclass.name,
                                                                            'is_prolonged' : msg.eventclass.is_prolonged})
                    eventclasses[msg.eventclass.session_code] = ec

                elif msgtype == 'metric':                   
                    m, created = Metric.objects.get_or_create(label=msg.metric.label,
                                                              defaults={'name' : msg.metric.name})
                    metrics[msg.metric.session_code] = m
                elif msgtype == 'measurement':
                    Measurement.objects.create(metric=metrics[msg.measurement.metric_session_code],
                                               value=msg.measurement.value)
                else:
                    log.error('Received message of unknown type %s'%msgtype)
            except:
                log.exception('Error processing event message: %s'%msg)


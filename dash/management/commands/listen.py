import logging

import zmq

from django.core.management.base import BaseCommand, CommandError

from dash.models import Event, EventClass, Metric, Measurement


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
        eventclasses = dict([(ec.label, ec) for ec in EventClass.objects.all()])
        metrics = dict([(m.label, m) for m in Metric.objects.all()])
        while True:
            msg = socket.recv_json()
            try:
                if msg['type'] == 'event':
                    Event.objects.create(eventclass=eventclasses[msg['class']],
                                         value=msg['value'],
                                         duration=msg.get('duration',None))
                elif msg['type'] == 'eventclass':
                    ec, created = EventClass.objects.get_or_create(label=msg['label'],
                                                                   defaults={'name' : msg['name'],
                                                                            'is_prolonged' : msg['is_prolonged']})
                    eventclasses[ec.label] = ec

                elif msg['type'] == 'metric':
                    m, created = Metric.objects.get_or_create(label=msg['label'],
                                                              defaults={'name' : msg['name']})
                    metrics[m.label] = m
                elif msg['type'] == 'measurement':
                    Measurement.objects.create(metric=metrics[msg['metric']],
                                               value=msg['value'])
                else:
                    log.error('Received message of unknown type %s'%msg['type'])
            except:
                log.exception('Error processing event message: %s'%msg)


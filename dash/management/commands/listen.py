import logging

import zmq

from django.core.management.base import BaseCommand, CommandError

from dash.models import Event


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
        while True:
            msg = socket.recv_json()
            try:
                if msg['t'] == 'e':
                    Event.objects.create(eventclass=msg['c'],
                                         value=msg['v'],
                                         duration=msg.get('d',None))
                else:
                    log.error('Received message of unknown type %s'%msg['type'])
            except:
                log.exception('Error processing event message: %s'%msg)


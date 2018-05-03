import zmq

class Perforate(object):
    def __init__(self, host='127.0.0.1', port=14541):
        context = zmq.Context.instance()
        self.socket = context.socket(zmq.PUB)
        self.socket.connect('tcp://%s:%d'%(host,port))
        self.event_classes = set()
        self.metrics = set()
    
    def register_event_class(self, label, name, is_prolonged):
        assert label not in self.event_classes
        self.socket.send_json({'type' : 'eventclass',
                               'label' : label,
                               'name' : name,
                               'is_prolonged' : is_prolonged})
        self.event_classes.add(label)
        def emit_this_event(value=None, duration=None):
            self.emit_event(label, value=value, duration=duration)
        setattr(self, 'emit_%s'%label, emit_this_event)

    def register_metric(self, label, name):
        assert label not in self.metrics
        self.socket.send_json({'type' : 'metric',
                               'label' : label,
                               'name' : name})
        self.metrics.add(label)
        def record_this_metric(value):
            self.record_measurement(label, value)
        setattr(self, 'record_%s'%label, record_this_metric)
        

    def emit_event(self, eventclass, value=None, duration=None):
        assert eventclass in self.event_classes
        ev = {'type' : 'event',
              'class' : eventclass,
              'value' : value}
        if duration is not None:
            ev['duration'] = duration
        self.socket.send_json(ev)
        
    def record_measurement(self, metric, value):
        assert metric in self.metrics
        ev = {'type' : 'measurement',
              'metric' : metric,
              'value' : value}
        self.socket.send_json(ev)
        

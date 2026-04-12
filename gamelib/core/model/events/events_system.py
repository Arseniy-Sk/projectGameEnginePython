class Event:
    def __init__(self, source, event_type, data=None):
        self.source = source
        self.type = event_type
        self.data = data


class EventBus:
    """Шина событий"""
    
    def __init__(self):
        self._subscribers = {}
    
    def subscribe(self, source, event_type, callback):
        key = (source, event_type)
        if key not in self._subscribers:
            self._subscribers[key] = []
        self._subscribers[key].append(callback)
    
    def unsubscribe(self, source, event_type, callback):
        key = (source, event_type)
        if key in self._subscribers:
            subscribers = self._subscribers[key]
            if callback in subscribers:
                subscribers.remove(callback)
    
    def emit(self, source, event_type, data=None):
        event = Event(source, event_type, data)
        
        patterns = [
            (source, event_type),
            (source, None),
            (None, event_type),
            (None, None)
        ]
        
        for pattern in patterns:
            callbacks = self._subscribers.get(pattern)
            if callbacks:
                for cb in callbacks:
                    cb(event)


global_bus = EventBus()
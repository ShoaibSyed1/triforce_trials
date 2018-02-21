from game.ecs import Component
from game.from_dict import FromDict

class EventComponent(Component, FromDict):
    def __init__(self, listen):
        self.events = []
        self.listen = listen
        self.send = []
        self.to_remove = []
    
    def get_events(self):
        new_events = self.events
        self.events = []
        return new_events
    
    def remove(self, event):
        self.to_remove.append(event)
    
    @staticmethod
    def from_dict(data):
        from game.event import EventType

        listen = []
        for event_type in data.get('listen', []):
            listen.append(EventType[event_type])
        
        return EventComponent(listen)
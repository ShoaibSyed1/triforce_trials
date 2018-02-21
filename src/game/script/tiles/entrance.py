from game.component import EventComponent, Transform
from game.event import Event, EventType, PlayerEventType
from game.script.script import Script

class EntranceScript(Script):
    def __init__(self, oneway):
        self.oneway = oneway
        
    def start(self, entity, world):
        self.event_bus = world.component_for_entity(entity, EventComponent)
        self.transform = world.component_for_entity(entity, Transform)

        self.event_bus.send.append(Event({
            'type': PlayerEventType.SET_POS,
            'x': self.transform.position.x,
            'y': self.transform.position.y
        }, EventType.PLAYER))
    
    def update(self, dt):
        pass
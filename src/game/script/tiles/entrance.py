from game.component import EventComponent, Tag, Transform
from game.event import Event, EventType, NotifyEventType, PlayerEventType
from game.script.script import Script

class EntranceScript(Script):
    def __init__(self, oneway):
        self.oneway = oneway
        
        self.touched = False

    def start(self, entity, world):
        self.entity = entity
        self.world = world

        self.event_bus = world.component_for_entity(entity, EventComponent)
        self.transform = world.component_for_entity(entity, Transform)

        self.event_bus.send.append(Event({
            'type': PlayerEventType.SET_POS,
            'x': self.transform.position.x,
            'y': self.transform.position.y
        }, EventType.PLAYER))
    
    def update(self, dt):
        for event in self.event_bus.get_events():
            if event.ty == EventType.COLLISION:
                other = None
                if event.data['first'] == self.entity:
                    other = event.data['second']
                elif event.data['second'] == self.entity:
                    other = event.data['first']
                
                if other != None:
                    if self.world.has_component(other, Tag):
                        tag = self.world.component_for_entity(other, Tag)
                        if "player" in tag.tags:
                            if not self.touched:
                                self.touched = True

                                self.event_bus.send.append(Event({
                                'type': NotifyEventType.NOTIFY,
                                'time': 2,
                                'title': "Saved",
                                'text': "Game Saved"
                            }, EventType.NOTIFY))
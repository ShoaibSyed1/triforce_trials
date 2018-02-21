from game.component import EventComponent, Tag
from game.event import Event, EventType, ActionEventType, CaveEventType, CollisionEventType
from game.script.script import Script

class Exit(Script):
    def start(self, entity, world):
        self.entity = entity
        self.world = world

        self.event_bus = world.component_for_entity(entity, EventComponent)
    
    def update(self, dt):
        sent = False

        for event in self.event_bus.get_events():
            if event.ty == EventType.COLLISION:
                player = None
                if event.data['first'] == self.entity:
                    player = event.data['second']
                elif event.data['second'] == self.entity:
                    player = event.data['first']
                
                if player != None and self.world.has_component(player, Tag) and "player" in self.world.component_for_entity(player, Tag).tags:
                    self.event_bus.send.append(Event({
                        'type': ActionEventType.SET_INFO,
                        'id': self.entity,
                        'text': "Descend",
                        'callback': self.descend,
                        'timeout': 0.2
                    }, EventType.ACTION))
                    sent = True
        
        if not sent:
            return
            self.event_bus.send.append(Event({
                'type': ActionEventType.DELETE_INFO,
                'id': self.entity
            }, EventType.ACTION))
    
    def descend(self):
        self.event_bus.send.append(Event({
            'type': CaveEventType.DESCEND
        }, EventType.CAVE, True))

        return True
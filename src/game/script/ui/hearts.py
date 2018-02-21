from game import loader
from game.component import EventComponent, Transform
from game.event import Event, EventType, PlayerEventType
from game.script.script import Script

class HeartsScript(Script):
    def __init__(self):
        self._hearts = []
    
    def start(self, entity, world):
        self.entity = entity
        self.world = world

        self.event_bus = world.component_for_entity(self.entity, EventComponent)
    
    def update(self, dt):
        for event in self.event_bus.get_events():
            if event.ty == EventType.PLAYER:
                if event.data['type'] == PlayerEventType.HEALTH_CHANGED:
                    self.draw_hearts(event.data['new'])
    
    def clear_hearts(self):
        for entity in self._hearts:
            self.world.delete_entity(entity)
        
        self._hearts.clear()
    
    def draw_hearts(self, amount):
        self.clear_hearts()

        for i in range(amount):
            heart_entity = self.world.create_entity_with(*loader.load("entity", "ui/overworld/heart")[0])
            transform = self.world.component_for_entity(heart_entity, Transform)
            transform.position.x = 5 + i * 17
            transform.position.y = 5
            self._hearts.append(heart_entity)
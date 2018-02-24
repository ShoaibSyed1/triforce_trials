from game import loader
from game.component import EventComponent, Sprite, Transform
from game.event import Event, EventType, PlayerEventType
from game.script.script import Script

class ArrowCounter(Script):
    def __init__(self):
        self.text_entity = None
    
    def start(self, entity, world):
        self.entity = entity
        self.world = world

        self.event_bus = world.component_for_entity(entity, EventComponent)
        self.transform = world.component_for_entity(entity, Transform)

        self.update_text(0)

    def update(self, dt):
        for event in self.event_bus.get_events():
            if event.ty == EventType.PLAYER:
                if event.data['type'] == PlayerEventType.ARROWS_CHANGED:
                    self.update_text(event.data['new'])
    
    def update_text(self, new):
        if self.text_entity != None:
            self.world.delete_entity(self.text_entity)
            self.text_entity = None
        
        self.text_entity = self.world.create_entity_with(*loader.load("entity", "ui/overworld/arrow_text")[0])
        
        transform = self.world.component_for_entity(self.text_entity, Transform)

        transform.position.x = self.transform.position.x + 16
        transform.position.y = self.transform.position.y + 18

        self.world.remove_component(self.text_entity, Sprite)
        
        new_sprite = Sprite.new_text(str(new), (255, 255, 255), 14)

        self.world.add_component(self.text_entity, new_sprite)
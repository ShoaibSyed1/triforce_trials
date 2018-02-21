from game import constants
from game.component import EventComponent, Sprite, Transform
from game.event import Event, EventType, PlayerEventType
from game.player_data import PlayerData
from game.script.script import Script

class PlayerLevel(Script):
    def start(self, entity, world):
        self.entity = entity
        self.world = world

        self.event_bus = world.component_for_entity(entity, EventComponent)
        self.sprite = world.component_for_entity(entity, Sprite)
        self.transform = world.component_for_entity(entity, Transform)
    
    def update(self, dt):
        for event in self.event_bus.get_events():
            if event.ty == EventType.PLAYER:
                if event.data['type'] == PlayerEventType.XP_ADDED:
                    new_level = PlayerData.level_from_xp(event.data['new'])
                    
                    self.world.remove_component(self.entity, self.sprite)
                    self.sprite = Sprite.new_text("Level " + str(new_level), (255, 255, 255), 14)
                    self.world.add_component(self.entity, self.sprite)
                    self.sprite._redraw = True
                    self.transform.x = constants.WIDTH / 2 - self.sprite.bounds.width / 2
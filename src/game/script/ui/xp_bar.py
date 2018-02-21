
from game.component import EventComponent, Sprite, Transform
from game.event import Event, EventType, PlayerEventType
from game.player_data import PlayerData
from game.script.script import Script

class XpBar(Script):
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
                    new_xp = event.data['new']

                    cur_level = PlayerData.level_from_xp(new_xp)
                    prev_total_xp = PlayerData.xp_from_level(cur_level)
                    total_xp = PlayerData.xp_from_level(cur_level+1)

                    self.sprite.bounds.width = 624 * (new_xp-prev_total_xp) / (total_xp-prev_total_xp)
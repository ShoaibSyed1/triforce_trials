import pygame

from game import constants, loader
from game.component import AnimationSets, EventComponent, Tag, Transform
from game.event import Event, EventType, MusicEventType
from game.script.script import Script

class GameoverScript(Script):
    def __init__(self):
        self.player_pos = pygame.math.Vector2(0, 0)

        self.wait_counter = 0
        self.waited = False
    
    def start(self, entity, world):
        self.entity = entity
        self.world = world

        self.event_bus = world.component_for_entity(entity, EventComponent)

        for all_ent in world.get_all_entities():
            if all_ent == self.entity:
                continue
            
            if world.has_component(all_ent, Tag):
                tag = world.component_for_entity(all_ent, Tag)
                if not "system" in tag.tags:
                    world.delete_entity(all_ent)
            else:
                world.delete_entity(all_ent)
        
        self.event_bus.send.append(Event({
            'type': MusicEventType.CLEAR
        }, EventType.MUSIC))

        self.create_player()
    
    def create_player(self):
        self.player_gameover = self.world.create_entity_with(*loader.load("entity", "player_gameover")[0])

        transform = self.world.component_for_entity(self.player_gameover, Transform)

        transform.position.x = self.player_pos.x
        transform.position.y = self.player_pos.y

        animation = self.world.component_for_entity(self.player_gameover, AnimationSets)

        animation.current = "still"
    
    def update(self, dt):
        if not self.waited:
            self.wait_counter += dt

            if self.wait_counter >= constants.GAMEOVER_DELAY + constants.GAMEOVER_SPIN + 1:
                self.waited = True
                self.event_bus.send.append(Event({
                    'type': MusicEventType.PLAY,
                    'path': "gameover/gameover",
                    'id': constants.MUSIC_GAMEOVER
                }, EventType.MUSIC))
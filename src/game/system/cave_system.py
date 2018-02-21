import random

import pygame

from game import constants, loader, paths
from game.component import CollisionComponent, EventComponent, ScriptComponent, Sprite, Tag, Transform
from game.ecs import System
from game.event import CameraEventType, Event, EventType, CaveEventType, PlayerEventType, MusicEventType
from game.generator import Generator
from game.populator import Populator
from game.script.load_script import LoadScript

# TODO: Turn into script
class CaveSystem(System):
    def __init__(self):
        self._event_bus = EventComponent([EventType.CAVE])
    
    def start(self):
        for entity in self.world.get_all_entities():
            if self.world.has_component(entity, Tag):
                tag = self.world.component_for_entity(entity, Tag)
                if not "system" in tag.tags:
                    self.world.delete_entity(entity)
            else:
                self.world.delete_entity(entity)
        
        self.world.create_entity_with(self._event_bus)

        for components in loader.load("entity", "OVERWORLD"):
            self.world.create_entity_with(*components)
        
        ld = self.world.create_entity_with(*loader.load("entity", "loading")[0])
        self.world.add_component(ld, ScriptComponent(LoadScript(self.generate())))
    
    def update(self, dt):
        for event in self._event_bus.get_events():
            if event.ty == EventType.CAVE:
                if event.data['type'] == CaveEventType.DESCEND:
                    self.start()
                    
                    self._event_bus.send.append(Event({
                        'type': MusicEventType.POP,
                        'id': constants.MUSIC_BG,
                        'fade': True,
                        'fade_time': 1000
                    }, EventType.MUSIC))
    
    def generate(self):
        pygame.mixer.Sound(paths.SOUNDS + "player/climb.wav").play()
        # TODO
        gen = Generator(32, 32)
        basicmap = gen.create_dungeon()
        yield
        tilemap = [0 for i in range(len(basicmap))]
        for y in range(0, 32):
            for x in range(0, 32):
                if gen.get_tile(x, y) == 1:
                    tilemap[x + y * 32] = -1
                    continue
                n = gen.get_tile(x, y-1)
                ne = gen.get_tile(x+1, y-1)
                e = gen.get_tile(x+1, y)
                se = gen.get_tile(x+1, y+1)
                s = gen.get_tile(x, y+1)
                sw = gen.get_tile(x-1, y+1)
                w = gen.get_tile(x-1, y)
                nw = gen.get_tile(x-1, y-1)
                sprite_number = 0
                if n == 0:
                    sprite_number += 1
                if e == 0:
                    sprite_number += 2
                if s == 0:
                    sprite_number += 4
                if w == 0:
                    sprite_number += 8
                
                if sprite_number == 15:
                    sprite_number += 1
                    if ne == 0:
                        sprite_number += 1
                    if se == 0:
                        sprite_number += 2
                    if sw == 0:
                        sprite_number += 4
                    if nw == 0:
                        sprite_number += 8
                
                tilemap[x + y * 32] = sprite_number
            
            yield
        
        populator = Populator(tilemap, 32, 32)
        tilemap = populator.populate(15, True)

        yield

        tile_mappings = loader.load("data", "tiles")
        
        for y in range(0, 32):
            for x in range(0, 32):
                tile_type = type(tilemap[x + y * 32])
                if tile_type == int:
                    if tilemap[x + y * 32] > -1:
                        collision = CollisionComponent(size=pygame.math.Vector2(16, 16), solid=True)
                        sprite = loader.load("sprite", "bricks")
                        transform = Transform(position=pygame.math.Vector2(x * 16 * 2, y * 16 * 2), scale=pygame.math.Vector2(2, 2))
                        sprite.start = tilemap[x + y * 32]
                        sprite.end = sprite.start + 1

                        self.world.create_entity_with(collision, sprite, transform)
                else:
                    chance_list = tile_mappings[tilemap[x + y * 32]]
                    weights = list(map(lambda x: x.get('chance', 1), chance_list))
                    choice = random.choices(chance_list, weights)
                    entity_path = choice[0]['entity']
                    entities = loader.load("entity", entity_path)

                    for components in entities:
                        for component in components:
                            if type(component) == Transform:
                                component.position.x = x * 16 * 2
                                component.position.y = y * 16 * 2
                                component.scale.x = 2
                                component.scale.y = 2
                        
                        self.world.create_entity_with(*components)
            
            yield
        
        floor_sprite = loader.load("sprite", "tiles/floor").repeated(32, 32)
        floor_transform = Transform(scale=pygame.math.Vector2(2, 2), layer=-1)
        self.world.create_entity_with(floor_sprite, floor_transform)

        yield

        self._event_bus.send.append(Event({
            'type': CameraEventType.SET_BOUNDS,
            'x': 0,
            'y': 0,
            'width': 16 * 2 * 32,
            'height': 16 * 2 * 32 + 80
        }, EventType.CAMERA))

        self._event_bus.send.append(Event({
            'type': MusicEventType.PLAY,
            'path': "background/background",
            'id': constants.MUSIC_BG
        }, EventType.MUSIC))

        raise StopIteration
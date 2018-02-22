import pygame

import random

from game import constants
from game.direction import Direction
from game.event import Event, EventType, MusicEventType, PlayerEventType
from game.script.enemies.enemy import Enemy

class MiniMoldorm(Enemy):
    def __init__(self):
        super().__init__()

        self.tracking = False
        self.tracking_x = 0
        self.tracking_y = 0

        self.dir_x = Direction.LEFT
        self.dir_y = Direction.DOWN
        self.dir_counter = 0
        self.max_dir_counter = 0
    
    def e_start(self):
        self.max_dir_counter = 0
    
    def e_update(self, dt):
        for event in self.event_bus.get_events():
            if event.ty == EventType.PLAYER:
                if event.data['type'] == PlayerEventType.PLAYER_MOVED:
                    x = event.data['x']
                    y = event.data['y']
                    
                    self.tracking = False

                    self.tracking_x = x
                    self.tracking_y = y
            elif event.ty == EventType.COLLISION:
                if event.data['first'] == self.entity or event.data['second'] == self.entity:
                    self.max_dir_counter = 0
        
        if not self.tracking:
            self_x = self.transform.position.x
            self_y = self.transform.position.y
            x = self.tracking_x
            y = self.tracking_y

            if self_x > x - constants.MINIMOLDORM_RANGE and self_x < x + constants.MINIMOLDORM_RANGE and self_y > y - constants.MINIMOLDORM_RANGE and self_y < y + constants.MINIMOLDORM_RANGE:
                self.tracking = True
                
                self.event_bus.send.append(Event({
                    'type': MusicEventType.PUSH,
                    'path': 'encounter/encounter',
                    'id': constants.MUSIC_ENCOUNTER,
                    'lifetime': 1
                }, EventType.MUSIC))
        
        if self.tracking:
            x = self.tracking_x
            y = self.tracking_y
            self_x = self.transform.position.x
            self_y = self.transform.position.y

            self.event_bus.send.append(Event({
                'type': MusicEventType.PUSH,
                'path': 'encounter/encounter',
                'id': constants.MUSIC_ENCOUNTER,
                'lifetime': 3
            }, EventType.MUSIC))

            self.max_dir_counter = 0

            if self_x > x + 4:
                self.dir_x = Direction.LEFT
            elif self_x < x - 4:
                self.dir_x = Direction.RIGHT
            else:
                self.dir_x = None

            if self_y > y + 4:
                self.dir_y = Direction.UP
            elif self_y < y - 4:
                self.dir_y = Direction.DOWN
            else:
                self.dir_y = None
        
        self.dir_counter += dt
        if self.dir_counter >= self.max_dir_counter:
            self.max_dir_counter = random.uniform(constants.MINIMOLDORM_ROTATE_MIN, constants.MINIMOLDORM_ROTATE_MAX)
            self.dir_counter = 0
            if not self.tracking:
                self.dir_x = random.choice([None, Direction(random.randrange(2, 4))])
                self.dir_y = random.choice([None, Direction(random.randrange(0, 2))])

            aname = None
            if self.dir_y == None:
                if self.dir_x == Direction.LEFT:
                    aname = "west"
                elif self.dir_x == Direction.RIGHT:
                    aname = "east"
            elif self.dir_y == Direction.UP:
                if self.dir_x == None:
                    aname = "north"
                elif self.dir_x == Direction.LEFT:
                    aname = "northwest"
                elif self.dir_x == Direction.RIGHT:
                    aname = "northeast"
            elif self.dir_y == Direction.DOWN:
                if self.dir_x == None:
                    aname = "south"
                elif self.dir_x == Direction.LEFT:
                    aname = "southwest"
                elif self.dir_x == Direction.RIGHT:
                    aname = "southeast"
            
            if aname != None:
                self.animation.current = aname
        
        if self.dir_x != None and self.dir_y != None:
            self.damage_knockback = pygame.math.Vector2(self.dir_x.to_vector(constants.MINIMOLDORM_SPEED).x * 10, self.dir_y.to_vector(constants.MINIMOLDORM_SPEED).y * 10)
        
        if self.dir_x != None:
            self.collision.velocity.x += self.dir_x.to_vector(constants.MINIMOLDORM_SPEED).x
        if self.dir_y != None:
            self.collision.velocity.y += self.dir_y.to_vector(constants.MINIMOLDORM_SPEED).y
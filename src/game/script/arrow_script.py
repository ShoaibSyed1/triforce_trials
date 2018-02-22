import pygame

from game import constants, paths
from game.component import CollisionComponent, EventComponent, Tag
from game.damage_data import DamageData
from game.direction import Direction
from game.event import Event, EventType, CollisionEventType
from game.script.script import Script

class ArrowScript(Script):
    def __init__(self):
        self.dir = None
        self.timer = constants.ARROW_LIFE
        self.moving = True

        self.sound = pygame.mixer.Sound(paths.SOUNDS + "arrow.wav")
        self.sound_delay = constants.ARROW_SOUND_DELAY
        self.sound_played = False

        self.sound_hit = pygame.mixer.Sound(paths.SOUNDS + "arrow_hit.wav")

        self.data = None
        self.player = None
    
    def start(self, entity, world):
        self.entity = entity
        self.world = world

        self.collision = world.component_for_entity(entity, CollisionComponent)
        self.event_bus = world.component_for_entity(entity, EventComponent)
        self.tag = world.component_for_entity(entity, Tag)

        if self.dir == None:
            self.dir = Direction.DOWN
    
    def update(self, dt):
        for event in self.event_bus.get_events():
            if event.ty == EventType.COLLISION:
                if self.moving:
                    other = None
                    if event.data['first'] == self.entity:
                        other = event.data['second']
                    elif event.data['second'] == self.entity:
                        other = event.data['first']
                    
                    if other != None:
                        other_collision = self.world.component_for_entity(other, CollisionComponent)
                        if other_collision.solid:
                            self.moving = False
                            self.tag.tags.remove("weapon")
                            self.collision.velocity.x = 0
                            self.collision.velocity.y = 0

                            self.sound_hit.play()

                        if self.world.has_component(other, Tag):
                            tag = self.world.component_for_entity(other, Tag)
                            if "enemy" in tag.tags:
                                self.timer = 0
        
        self.timer -= dt
        if self.timer <= 0:
            self.world.delete_entity(self.entity)

        if not self.sound_played:
            self.sound_delay -= dt
            if self.sound_delay <= 0:
                self.sound.play()
                self.sound_played = True
        
        if self.moving:
            self.collision.velocity = self.dir.to_vector(constants.ARROW_SPEED)
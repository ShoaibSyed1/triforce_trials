import pygame

from game import constants, loader, paths
from game.component import Sprite, Transform
from game.script.script import Script

class BombScript(Script):
    def __init__(self):
        self.timer = 0

        self.sound = pygame.mixer.Sound(paths.SOUNDS + "bomb.wav")
    
    def start(self, entity, world):
        self.entity = entity
        self.world = world

        self.transform = world.component_for_entity(entity, Transform)

        self.sound.play()
    
    def update(self, dt):
        self.timer += dt

        if self.timer >= constants.BOMB_TIME:
            self.world.delete_entity(self.entity)

            explosion = self.world.create_entity_with(*loader.load("entity", "explosion")[0])
            sprite = self.world.component_for_entity(explosion, Sprite)
            transform = self.world.component_for_entity(explosion, Transform)

            transform.position.x = (self.transform.position.x + 16) - (sprite.frame_width * transform.scale.x) / 2
            transform.position.y = (self.transform.position.y + 16) - (sprite.frame_height * transform.scale.y) / 2
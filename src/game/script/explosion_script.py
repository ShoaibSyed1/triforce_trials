import pygame

from game import constants, paths
from game.script.script import Script

class ExplosionScript(Script):
    def __init__(self):
        self.timer = 0

        self.sound = pygame.mixer.Sound(paths.SOUNDS + "explosion.wav")
    
    def start(self, entity, world):
        self.entity = entity
        self.world = world

        self.sound.play()
    
    def update(self, dt):
        self.timer += dt

        if self.timer >= constants.EXPLOSION_TIME:
            self.world.delete_entity(self.entity)
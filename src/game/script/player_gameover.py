import pygame

from game import constants, loader, paths
from game.component import AnimationSets
from game.script.script import Script

class PlayerGameover(Script):
    def __init__(self):
        self.sound = pygame.mixer.Sound(paths.SOUNDS + "player/gameover.wav")

        self.still_timer = 0
        self.is_still = True
        
        self.spin_timer = 0
        self.is_spinning = False
    
    def start(self, entity, world):
        self.entity = entity
        self.world = world

        self.animation = world.component_for_entity(entity, AnimationSets)

        self.animation.current = "still"
    
    def update(self, dt):
        if self.is_still:
            self.still_timer += dt

            if self.still_timer >= constants.GAMEOVER_DELAY:
                self.is_still = False
                self.animation.current = "spin"
                self.sound.play()
                self.is_spinning = True
        elif self.is_spinning:
            self.spin_timer += dt

            if self.spin_timer >= constants.GAMEOVER_SPIN:
                self.is_spinning = False
                self.animation.current = "lay"
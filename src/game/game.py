import pygame

from game import constants
from game.scene import Scene

class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        
        self.window = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        pygame.display.set_caption("The Legend of Zelda: Trials of the Triforce")

        self.clock = pygame.time.Clock()
        self.dt = 0

        self.scene = Scene(self)

        self.running = False
    
    def start(self):
        self.running = True

        self.scene.start()

        COUNTER = 0

        while self.running:
            self.scene.update(self.dt)

            self.dt = self.clock.tick(60) / 1000
            if self.dt > 0.33:
                self.dt = 0.33

            COUNTER += self.dt

            if COUNTER > 0.5:
                COUNTER = 0

                #print(1 / self.dt)
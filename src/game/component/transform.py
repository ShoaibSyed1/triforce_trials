import pygame

from game.ecs import Component
from game.from_dict import FromDict

class Transform(Component, FromDict):
    def __init__(self, position=pygame.math.Vector2(0, 0), scale=pygame.math.Vector2(1, 1), layer=0, fixed=False):
        self.position = position
        self.scale = scale
        self.layer = layer
        self.fixed = fixed
    
    @staticmethod
    def from_dict(data):
        position = pygame.math.Vector2(data.get('position', (0, 0))[0], data.get('position', (0, 0))[1])
        scale = pygame.math.Vector2(data.get('scale', (1, 1))[0], data.get('scale', (1, 1))[1])
        layer = int(data.get('layer', 0))
        fixed = bool(data.get('fixed', False))

        return Transform(position, scale, layer, fixed)
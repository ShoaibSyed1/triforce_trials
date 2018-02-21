import pygame

from game.ecs import Component
from game.from_dict import FromDict

class CollisionComponent(Component, FromDict):
    def __init__(self, size, friction=0.7, layer=0, max_speed=500, solid=False, persistent=False):
        self.size = size
        self.friction = friction
        self.layer = layer
        self.max_speed = max_speed
        self.solid = solid
        self.persistent = persistent

        self.velocity = pygame.math.Vector2(0, 0)
    
    @staticmethod
    def from_dict(data):
        size = pygame.math.Vector2(data.get('size')[0], data.get('size')[1])
        friction = float(data.get('friction', 0.7))
        layer = int(data.get('layer', 0))
        max_speed = int(data.get('max_speed', 500))
        solid = bool(data.get('solid', False))
        persistent = bool(data.get('persistent', False))

        return CollisionComponent(size, friction, layer, max_speed, solid, persistent)
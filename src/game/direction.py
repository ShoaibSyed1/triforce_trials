from enum import Enum

import pygame

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def to_vector(self, value=1):
        if self == Direction.UP:
            return pygame.math.Vector2(0, -value)
        elif self == Direction.LEFT:
            return pygame.math.Vector2(-value, 0)
        elif self == Direction.RIGHT:
            return pygame.math.Vector2(value, 0)
        else:
            return pygame.math.Vector2(0, value)

    def opposite(self):
        if self == Direction.UP:
            return Direction.DOWN
        elif self == Direction.DOWN:
            return Direction.UP
        elif self == Direction.LEFT:
            return Direction.RIGHT
        elif self == Direction.RIGHT:
            return Direction.LEFT
    
    def is_horizontal(self):
        return self == Direction.LEFT or self == Direction.RIGHT

    def is_vertical(self):
        return self == Direction.UP or self == Direction.DOWN
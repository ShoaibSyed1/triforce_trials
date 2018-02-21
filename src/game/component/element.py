import pygame

from game.ecs import Component

class Element(Component):
    def __init__(self, position, root=False, visible=True, parent=None, children=[]):
        self.position = position
        self.root = root
        self.visible = visible
        self.parent = parent
        self.children = children
    
    @staticmethod
    def from_dict(data):
        position = pygame.math.Vector2(data['position'][0], data['position'][1])
        root = data.get('root', False)
        visible = data.get('visible', True)

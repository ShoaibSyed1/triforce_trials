from enum import Enum

from game import loader
from game.component import Sprite
from game.script.script import Script

class LoadScript(Script):
    def __init__(self, load_generator):
        self.load_generator = load_generator
    
    def start(self, entity, world):
        self.entity = entity
        self.world = world

        self.sprite = self.world.component_for_entity(self.entity, Sprite)

        self.load_circle = self.world.create_entity_with(*loader.load("entity", "load_circle")[0])
        self.load_circle_sprite = self.world.component_for_entity(self.load_circle, Sprite)
    
    def update(self, dt):        
        try:
            next(self.load_generator)
        except StopIteration:
            self.stop()
    
    def stop(self):
        self.world.delete_entity(self.entity)
        self.world.delete_entity(self.load_circle)

from game.script.script import Script

class Poof(Script):
    def __init__(self):
        self.counter = 0.4
    
    def start(self, entity, world):
        self.entity = entity
        self.world = world
    
    def update(self, dt):
        self.counter -= dt

        if self.counter <= 0:
            self.world.delete_entity(self.entity)
from game.drop import Drop, DropType
from game.script.script import Script

class DropScript(Script):
    def __init__(self, drop_data):
        if type(drop_data) == Drop:
            self.drop = drop_data
        else:
            self.drop = Drop.from_data(drop_data)
    
    def start(self, entity, world):
        self.entity = entity
        self.world = world

    def collected(self):
        self.world.delete_entity(self.entity)
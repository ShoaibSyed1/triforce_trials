from game.drop import Drop, DropType
from game.script.script import Script

class DropScript(Script):
    def __init__(self, drop_data):
        self.drop = Drop(DropType[drop_data['type']], drop_data['data'])
    
    def start(self, entity, world):
        self.entity = entity
        self.world = world

    def collected(self):
        self.world.delete_entity(self.entity)
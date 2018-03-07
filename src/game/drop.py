from enum import Enum

class Drop:
    def __init__(self, ty, data):
        self.ty = ty
        self.data = data
    
    @staticmethod
    def from_data(data):
        return Drop(DropType[data['type']], data.get('data', {}))

class DropType(Enum):
    NOTHING = 0
    ARROW = 1
    BOMB = 2
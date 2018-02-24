from enum import Enum

class Drop:
    def __init__(self, ty, data):
        self.ty = ty
        self.data = data

class DropType(Enum):
    ARROW = 0
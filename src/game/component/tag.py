from game.ecs import Component
from game.from_dict import FromDict

class Tag(Component, FromDict):
    def __init__(self, tags=[]):
        self.tags = tags
    
    @staticmethod
    def from_dict(data):
        tags = data['tags']

        return Tag(tags)
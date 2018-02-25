
from game.ecs import Component
from game.from_dict import FromDict

class AnimationSets(Component, FromDict):
    def __init__(self, sets, current=None):
        self.sets = sets
        self.current = current
        self.last = None
    
    @staticmethod
    def from_dict(data):
        sets = {}
        set_info_dict = data.get('sets', {})
        for key, value in set_info_dict.items():
            sets[key] = AnimationSet(value['delay'], value['start'], value['end'])
        current = data.get('current', None)
        
        return AnimationSets(sets, current)

class AnimationSet:
    def __init__(self, delay, start, end):
        self.delay = delay
        self.start = start
        self.end = end
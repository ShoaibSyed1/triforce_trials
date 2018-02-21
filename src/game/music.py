from enum import Enum

class MusicInfo:
    def __init__(self, choices, repeat_type):
        self.choices = choices
        self.repeat_type = repeat_type

class RepeatType(Enum):
    NONE = 0
    PLAYLIST = 1
    RANDOM = 2
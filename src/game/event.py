from enum import Enum

class Event:
    def __init__(self, data, ty, delete_after=False):
        self.data = data
        self.ty = ty
        self.delete_after = delete_after

class EventType(Enum):
    PYGAME = 0
    CAMERA = 1
    COLLISION = 2
    PLAYER = 3
    MUSIC = 4
    ACTION = 5
    CAVE = 6
    
    DELETE = 5

class CameraEventType(Enum):
    FOLLOW = 0
    SET_BOUNDS = 1

class CollisionEventType(Enum):
    pass

"""
class MusicEventType(Enum):
    PLAY = 0
    PAUSE = 1
    STOP = 2
    LOAD = 3
"""
class MusicEventType(Enum):
    PLAY = 1 # path: string, id: int, [lifetime: int]
    PUSH = 2 # path: string, id: int, [lifetime: int]
    POP = 3 # id: int, fade: boolean -> [fade_time: int (in millis)]

class PlayerEventType(Enum):
    SET_POS = 0
    PLAYER_MOVED = 1

    ADD_XP = 2
    XP_ADDED = 3

    HURT = 4 # amount: int, knockback: vector2
    HEAL = 5
    HEALTH_CHANGED = 6 # original: int, amount: int, new: int

class ActionEventType(Enum):
    SET_INFO = 0 # id: int (entity id), text: string (action name), callback: bool def() (called when action key is pressed, return True to delete action info), timeout: float = None (auto delete)
    DELETE_INFO = 1 # id: int (entity id)

class CaveEventType(Enum):
    DESCEND = 0

class DeleteEventType(Enum):
    ENTITY = 0
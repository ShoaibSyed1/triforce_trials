from enum import Enum

from game import saving
from game.damage_data import DamageData

class PlayerData:
    def __init__(self):
        self.name = ""
        self.health = 5
        self.max_health = 5
        self.xp = 0
        self.arrows = 0
        self.skills = {
            PlayerSkill.MELEE: 0,
            PlayerSkill.RANGED: 0
        }
        self.special1 = None
        self.special2 = None
    
    def load(self):
        data = saving.load("player")

        self.name = data.get('name', "")
        self.xp = data.get('xp', 0)
        self.arrows = data.get('arrows', 5)
        self.health = data.get('health', 5)
        self.max_health = data.get('max_health', 5)
        for key, value in data.get('skills', {}).items():
            skill = PlayerSkill[key]
            self.skills[skill] = value

        self.save()
    
    def save(self):
        data = {
            'name': self.name,
            'xp': self.xp,
            'arrows': self.arrows,
            'health': self.health,
            'max_health': self.max_health,
            'skills': {
                "MELEE": self.skills[PlayerSkill.MELEE],
                "RANGED": self.skills[PlayerSkill.RANGED]
            }
        }

        saving.save("player", data)
    
    def get_level(self):
        return PlayerData.level_from_xp(self.xp)
    
    def add_xp(self, amount):
        lvl = self.get_level()
        self.xp += amount

        return self.get_level() > lvl
    
    def get_sword_damage(self):
        # TODO
        return 1
    
    def get_bow_damage(self):
        # TODO
        return 1
    
    @staticmethod
    def level_from_xp(xp):
        return int(pow((5 * xp) / 4, 1/3))
    
    @staticmethod
    def xp_from_level(level):
        return (4 / 5) * (level ** 3)

class PlayerSkill(Enum):
    MELEE = 0
    RANGED = 1

class Special:
    def __init__(self, ty):
        self.ty = ty
        self.level = 0

class SpecialType(Enum):
    SPIN_ATTACK = 0

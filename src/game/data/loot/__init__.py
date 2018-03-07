import random

from game import loader
from game.drop import Drop

class LootData:
    def __init__(self, items):
        self.items = items
    
    @staticmethod
    def load(loot_name):
        loot_data = loader.load("data", "loot/" + loot_name)

        items = []

        for item_data in loot_data.get('item', []):
            drop = Drop.from_data(item_data['drop'])

            chance = item_data['chance']
            level_factor = item_data.get('level_factor', 1)
            level_add = item_data.get('level_add', 0)

            items.append(LootItem(drop, chance, level_factor, level_add))
        
        return LootData(items)
    
    def get_item(self):
        if len(self.items) > 0:
            return random.choices(self.items, weights=[item.get_total_chance() for item in self.items])[0]
        else:
            return None
    
    def get_drop(self):
        item = self.get_item()
        if item == None:
            return None
        
        return item.drop

class LootItem:
    def __init__(self, drop, chance, level_factor=1, level_add=0):
        self.drop = drop
        self.chance = chance
        self.level_factor = level_factor
        self.level_add = level_add
    
    def get_total_chance(self, level):
        return self.chance + ((level + self.level_add) * self.level_factor)
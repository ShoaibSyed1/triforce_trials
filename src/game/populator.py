import random

from game import loader
from game.constants import TILE_ENTITIES_START

class Populator:
    def __init__(self, tiles, width, height):
        self._tiles = tiles
        self._width = width
        self._height = height
    
    def populate(self, enemies, oneway=True):
        self.entrance_pos = self.add_entrance(oneway)
        self.add_exit()

        self.add_multiple("enemy", enemies)

        return self._tiles
    
    def add_multiple(self, tile_name, max):
        counter = 0

        for i in range(1000):
            if counter >= max:
                return
            
            x = random.randint(0, self._width-1)
            y = random.randint(0, self._height-1)

            if self.get_tile(x, y) == -1 and (
                x < self.entrance_pos[0] - 5 or x > self.entrance_pos[0] + 5
            ) and (
                y < self.entrance_pos[1] - 5 or y > self.entrance_pos[1] + 5
            ):
                self.set_tile(x, y, tile_name)
                counter += 1
    
    def add_exit(self):
        self.add_one("exit")
    
    def add_entrance(self, oneway):
        tile_name = "entrance"
        if oneway:
            tile_name = "oneway_entrance"
        
        return self.add_one(tile_name)
    
    def add_one(self, tile_name):        
        for i in range(1000):
            x = random.randint(0, self._width-1)
            y = random.randint(0, self._height-1)

            if self.get_tile(x, y) == -1:
                self.set_tile(x, y, tile_name)
                return (x, y)
        
        for y in range(0, self._height):
            for x in range(0, self._width):
                if self.get_tile(x, y) == -1:
                    self.set_tile(x, y, tile_name)
                    return (x, y)
        
    def get_tile(self, x, y):
        return self._tiles[x + self._width * y]
    
    def set_tile(self, x, y, id):
        self._tiles[x + self._width * y] = id
    
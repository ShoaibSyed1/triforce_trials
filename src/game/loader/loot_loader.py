from game import paths
from game.loader.loader import Loader

# TODO
class LootLoader(Loader):
    @staticmethod
    def load(data, path):
        pass
    
    @staticmethod
    def get_full_path(part_path):
        return paths.LOOT + part_path
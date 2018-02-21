from game import paths
from game.loader.loader import Loader

class DataLoader(Loader):
    @staticmethod
    def load(data, path):
        return data
    
    @staticmethod
    def get_full_path(part_path):
        return paths.DATA + part_path
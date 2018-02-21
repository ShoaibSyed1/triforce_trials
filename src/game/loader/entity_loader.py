from game import paths
from game.loader.loader import Loader

class EntityLoader(Loader):
    @staticmethod
    def load(data, path):
        from game import loader

        entities = []

        if "include" in data.keys():
            for entity in data['include']:
                entities += loader.load_raw("entity", entity)
            
            del data['include']
        
        components = []

        for key, value in data.items():
            components.append(loader.load_raw(key, value))
        
        entities.append(components)
        
        return entities
    
    @staticmethod
    def get_full_path(part_path):
        return paths.ENTITIES + part_path
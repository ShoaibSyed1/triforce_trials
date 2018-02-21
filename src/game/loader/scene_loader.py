from game import paths
from game.loader.loader import Loader

class SceneLoader(Loader):
    @staticmethod
    def load(data, path):
        from game import loader

        entity_list = data.get('entities', [])

        entity_info_list = []

        for entity_info in entity_list:
            for entities in loader.load_raw("entity", entity_info):
                entity_info_list.append(entities)
        
        return entity_info_list
    
    @staticmethod
    def get_full_path(part_path):
        return paths.SCENES + part_path
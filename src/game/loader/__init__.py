from game.component import AnimationSets, CollisionComponent, EventComponent, ScriptComponent, Tag, Transform
from game.deepupdate import deepupdate
from game.from_dict import FromDict
from game.loader.data_loader import DataLoader
from game.loader.entity_loader import EntityLoader
from game.loader.loot_loader import LootLoader
from game.loader.music_loader import MusicLoader
from game.loader.scene_loader import SceneLoader
from game.loader.sprite_loader import SpriteLoader

LOADERS = {
    "animation": AnimationSets,
    "collision": CollisionComponent,
    "event": EventComponent,
    "script": ScriptComponent,
    "tag": Tag,
    "transform": Transform,

    "sprite": SpriteLoader,

    "data": DataLoader,
    "entity": EntityLoader,
    "loot": LootLoader,
    "music": MusicLoader,
    "scene": SceneLoader
}

def load_toml(name, raw_path):
    import toml

    path = raw_path
    
    if not issubclass(LOADERS[name], FromDict):
        path = LOADERS[name].get_full_path(path)

    data = None
    with open(path + ".toml") as file:
        data = toml.load(file)
    
    return data

def load_entities_into(path, world):
    entities = load("entity", path)
    first = None
    for i in range(len(entities)):
        if i == 0:
            first = world.create_entity_with(*entities[i])
        else:
            world.create_entity_with(*entities[i])
    
    return first

def load(name, raw_path):
    import toml

    path = raw_path

    data = load_toml(name, raw_path)
    
    return load_raw(name, data, raw_path)

def load_raw(name, data, path=""):
    if issubclass(LOADERS[name], FromDict):
        return LOADERS[name].from_dict(data)
    
    if 'parent' in data.keys():
        parent = load_toml(name, data['parent'])
        data = deepupdate(parent, data)
        del data['parent']
    
    path = LOADERS[name].get_full_path(path)

    return LOADERS[name].load(data, path)
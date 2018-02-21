import toml

from game import paths

def load(path):
    data = {}
    try:
        with open(paths.SAVE + path + ".toml") as file:
            data = toml.load(file)
    except FileNotFoundError:
        with open(paths.SAVE + path + ".toml", 'w') as file:
            toml.dump(data, file)
    
    return data

def save(path, data):
    with open(paths.SAVE + path + ".toml", 'w') as file:
        toml.dump(data, file)
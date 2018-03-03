MAP = {
    3: 1,
    15: 2,
    63: 31,
    92: 84,
    207: 199,
    135: 2,
    143: 2,
    159: 31,
    191: 31,
    252: 124
}

def get(id):
    if id in MAP.keys():
        return MAP[id]
    
    return id
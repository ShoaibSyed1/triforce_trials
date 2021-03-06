MAP = {
    3: 1,
    12: 4,
    14: 4,
    15: 2,
    24: 16,
    30: 28,
    60: 28,
    62: 28,
    63: 31,
    92: 84,
    96: 64,
    120: 112,
    126: 124,
    131: 1,
    135: 2,
    143: 2,
    159: 31,
    191: 31,
    192: 64,
    195: 193,
    207: 199,
    224: 64,
    225: 193,
    227: 193,
    231: 199,
    240: 112,
    243: 241,
    248: 112,
    249: 241,
    251: 241,
    252: 124,
    254: 124
}

def get(id):
    if id in MAP.keys():
        return MAP[id]
    
    return id
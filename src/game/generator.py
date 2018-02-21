PASSES = 5

# Uses Cellular Automata to Generates Caves
class Generator:
    def __init__(self, width, height):
        self._width = width
        self._height = height

        self._map = [get_tile() for i in range(width * height)]

        for x in range(width):
            self._map[x] = 0
            self._map[(height-1) * width + x] = 0
        for y in range(height):
            self._map[y * width] = 0
            self._map[y * width + (width-1)] = 0
    
    def create_dungeon(self):
        import copy

        # Number of passes for algorithm
        for p in range(PASSES):
            new_map = list(self._map)

            for y in range(0, self._height):
                for x in range(0, self._width):
                    # If the 3x3 area surrounding a tile
                    # (including the tile itself) has at
                    # least 5 wall(0) tiles, it becomes
                    # (or stays) a wall tile
                    num_wall_neighbours = 0
                    for yo in range(-1, 2):
                        for xo in range(-1, 2):
                            if self.get_tile(x + xo, y + yo) == 0:
                                num_wall_neighbours += 1
                    
                    if num_wall_neighbours >= 5:
                        new_map[x + y * self._width] = 0
                    else:
                        new_map[x + y * self._width] = 1
            
            self._map = new_map
        
        self.connect_rooms()

        return self._map
    
    # Used to get rid of rooms that don't connect
    def connect_rooms(self):
        # Number of seperate rooms
        loops = 0

        # Uses flood-fill algorithm to determine number of rooms
        while True:
            start_x, start_y = self.get_floodfill_start()

            # If there aren't anymore ground(1) tiles, break the loop
            if start_x == None or start_y == None:
                break
            
            # Used to seperate rooms
            room_number = 2 + loops

            self.set_tile(start_x, start_y, room_number)

            nodes = [(start_x, start_y)]

            # Flood fill algorithm to set every connecting ground(1) tile to it's room number
            while len(nodes) > 0:
                node = nodes.pop()

                if self.get_tile(node[0] - 1, node[1]) == 1:
                    self.set_tile(node[0] - 1, node[1], room_number)
                    nodes.append((node[0] - 1, node[1]))
                if self.get_tile(node[0] + 1, node[1]) == 1:
                    self.set_tile(node[0] + 1, node[1], room_number)
                    nodes.append((node[0] + 1, node[1]))
                if self.get_tile(node[0], node[1] - 1) == 1:
                    self.set_tile(node[0], node[1] - 1, room_number)
                    nodes.append((node[0], node[1] - 1))
                if self.get_tile(node[0], node[1] + 1) == 1:
                    self.set_tile(node[0], node[1] + 1, room_number)
                    nodes.append((node[0], node[1] + 1))
            
            loops += 1
        
        # If there is only 1 room
        if loops <= 1:
            self.finish_connect()
            return

        # Determine number of tiles each room has
        counts = {}

        for y in range(0, self._height):
            for x in range(0, self._width):
                tile = self.get_tile(x, y)
                if tile > 1:
                    if not tile in counts.keys():
                        counts[tile] = 0
                    counts[tile] += 1
        
        # Get room with most number of tiles
        maximum = counts[2]
        max_index = 0
        for i in range(2, 2 + loops):
            maximum = max(maximum, counts[i])
            if maximum == counts[i]:
                max_index = i

        dont_remove = max_index

        # Fill in every room with wall(0) tiles except the one with the most tiles
        for y in range(0, self._height):
            for x in range(0, self._width):
                tile = self.get_tile(x, y)
                if tile > 1 and tile != dont_remove:
                    self.set_tile(x, y, 0)
        
        self.finish_connect()

    # Changes every tile greater than 1 back to a ground(1) tile
    def finish_connect(self):
        for y in range(0, self._height):
            for x in range(0, self._width):
                if self.get_tile(x, y) > 1:
                    self.set_tile(x, y, 1)

    # Finds first ground(1) tile available
    def get_floodfill_start(self):
        start_x = None
        start_y = None

        for y in range(0, self._height):
            for x in range(0, self._width):
                if self.get_tile(x, y) == 1:
                    start_x = x
                    start_y = y
        
        return (start_x, start_y)
    
    def set_tile(self, x, y, tile):
        self._map[self.bound_x(x) + self.bound_y(y) * self._width] = tile

    def get_tile(self, x, y):
        if x < 0 or x >= self._width or y < 0 or y >= self._height:
            return 0
        
        return self._map[self.bound_x(x) + self.bound_y(y) * self._width]

    def bound_x(self, x):
        return min(max(0, x), self._width)

    def bound_y(self, y):
        return min(max(0, y), self._height)

def get_tile():
    import random
    
    if random.random() <= 0.45:
        return 0
    else:
        return 1
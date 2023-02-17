class Moebel:
    moebel_sizes = [5, 4, 3, 3, 2]
    directions = ['h', 'v']

    def __init__(self, size, x, y, direction):
        self.size = size
        self.x = x
        self.y = y
        self.direction = direction
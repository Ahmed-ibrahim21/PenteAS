
from copy import copy, deepcopy

class Board:
    def __init__(self):
        # initialize the start grid
        start_row = []
        for i in range (19):
            start_row.append(0)

        self.grid = []
        for i in range (19):
            self.grid.append(deepcopy(start_row))

        self.captures = {
                1: 0,
                2: 0
                }

        self.occupied = [] #list of occupied positions
        self.empty_adjacent = [] # list of empty spots adjacent to an occupied spot

    def play(self, player, r, c):
        tuple = (r,c)
        self.grid[r][c] = player
        self.occupied.append(tuple)

        if tuple in self.empty_adjacent:
            self.empty_adjacent.remove(tuple)

        # add adjacents
        for i in range(r-1, r+2):
            for j in range (c-1, c+2):
                if r >= 0 and r < 19:
                    if c >= 0 and c < 19:
                        if (self.spot_empty(i,j) and not (i,j) in self.empty_adjacent):
                            self.empty_adjacent.append((i,j))
        return self


    def get_piece(self, r, c):
        if (r > 18 or c > 18 or r < 0 or c < 0):
            return -1
        return self.grid[r][c]
    
    def piece_captured(self, r, c):
        self.grid[r][c] = 0
        self.occupied.remove((r,c))
        self.empty_adjacent.append((r,c))

    def spot_empty(self, r, c):
        return self.get_piece(r, c) == 0

    def get_captures(self, pid):
        return self.captures[pid]

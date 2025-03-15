import random

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[" " for _ in range(cols)] for _ in range(rows)]
        self.place_objects()

    def place_objects(self):
        #posicion jugador
        self.grid[0][0] = "A" 
        #posicion del oro
        self.grid[random.randint(1, self.rows-1)][random.randint(1, self.cols-1)] = "O" 
        for _ in range(3):
            #posicion del wumpus
            self.grid[random.randint(0, self.rows-1)][random.randint(0, self.cols-1)] = "W"  
            #posicion del pozo
            self.grid[random.randint(0, self.rows-1)][random.randint(0, self.cols-1)] = "P"  

    def display(self, player_pos):
        for y in range(self.rows):
            row = ""
            for x in range(self.cols):
                if (x, y) == player_pos:
                    row += "A "
                else:
                    row += f"{self.grid[y][x]} "
            print(row)
        print()

    def get_percepts(self, pos):
        x, y = pos
        percepts = []
        if self.grid[y][x] == "O":
            percepts.append("Oro")
        if self.grid[y][x] == "W":
            percepts.append("Hedor")
        if self.grid[y][x] == "P":
            percepts.append("Brisa")
        return percepts

    def is_wumpus(self, pos):
        x, y = pos
        return self.grid[y][x] == "W"

    def is_pit(self, pos):
        x, y = pos
        return self.grid[y][x] == "P"

    def has_gold(self, pos):
        x, y = pos
        return self.grid[y][x] == "O"
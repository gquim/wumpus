class Player:
    def __init__(self):
        self.position = (0, 0)
        self.has_gold = False

    def move(self, direction):
        x, y = self.position
        if direction == "N" and y > 0:
            self.position = (x, y-1)
        elif direction == "S" and y < 9:
            self.position = (x, y+1)
        elif direction == "E" and x < 11:
            self.position = (x+1, y)
        elif direction == "O" and x > 0:
            self.position = (x-1, y)

    def update(self, percepts):
        print("Percibido:", percepts)

    def reset(self):
        self.position = (0, 0)
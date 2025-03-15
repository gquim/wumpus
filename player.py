class Player:
    def __init__(self):
        self.position = (0, 0)
        self.gold_collected = 0 
        self.total_gold = 2 

    def move(self, direction):
        x, y = self.position
        if direction == "N" and y > 0:
            self.position = (x, y-1)
        elif direction == "S" and y < 11:
            self.position = (x, y+1)
        elif direction == "E" and x < 15:
            self.position = (x+1, y)
        elif direction == "O" and x > 0:
            self.position = (x-1, y)

    def collect_gold(self):
        self.gold_collected += 1 

    def has_all_gold(self):
        return self.gold_collected >= self.total_gold 
    def update(self, percepts):
        self.percepts = percepts
        print("", self.percepts)
    def reset(self):
        self.position = (0, 0)

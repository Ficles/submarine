import time

class Info:
    def __init__(self, name):
        self.name = name
        self.creation = time.time()
        self.last_used = time.time()

    def refresh(self):
        self.last_used = time.time()

class Stats:
    def __init__(self, difficulty):
        self.rank = 0
        self.reputation = 0
        self.sub_max_depth = 30
        match difficulty:
            case 0:
                self.sub_health = 1000
                self.sub_speed = 10
                self.sub_cargo = 8
                self.ship_cargo = 24
            case 1:
                self.sub_health = 800
                self.sub_speed = 8
                self.sub_cargo = 6
                self.ship_cargo = 18
            case 2:
                self.sub_health = 600
                self.sub_speed = 8
                self.sub_cargo = 6
                self.ship_cargo = 18

class Unlocks:
    def __init__(self):
        pass
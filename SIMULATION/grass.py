import random
from animal import Animals, Grid_size, Grid, Animal, Site_list_random, Grid_Grass



class Grass(Animals):

    max_life = 1000
    min_life = 300
    site = 0
    birth_rate = 0.2
    hunting_rate = 0.0
    predator = ["Impala", "Rhino", "Grasshopper", "Mouse"]
    food = []
    calorie = 1000
    calorie_waste_rate = 0
    max_calorie = 100
    threshold_birth = 0.7

    name = "Grass"

    def __init__(self, x, y, energy_left):
        self.time_left = random.randint(self.min_life, self.max_life)
        self.energy_left = energy_left
        self.x = x
        self.y = y
        Grid_Grass[x][y] = self
        Animal[self.name].append(self)


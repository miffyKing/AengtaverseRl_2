import random
from animal import Animals,  Grid_size, Grid, Animal, Site_list_random
from lion import Lion
from leopard import Leopard

class Baboon(Animals):

    max_life = 120
    min_life = 90
    site = 4
    birth_rate = 0.6
    hunting_rate = 0.9
    predator = ["Leopard"]
    food = ["Snake"]
    calorie_waste_rate = 2
    max_calorie = 900
    calorie = 150

    name = "Baboon"

    def make_child(self):
        # 일정 칼로리이상이면 번식한다.
        # 움직이고나서 실행된다
        for i in range(1, self.site + 1):
            k = random.randint(0, len(Site_list_random[i]) - 1)
            for j in range(0, len(Site_list_random[i])):
                child_x = self.x + Site_list_random[i][k - j][0]
                child_y = self.y + Site_list_random[i][k - j][1]
                if (child_x >= Grid_size):
                    child_x -= Grid_size
                if (child_y >= Grid_size):
                    child_y -= Grid_size
                if (Grid[child_x][child_y] == 0):
                    a = Baboon(child_x, child_y, self.energy_left / 2)
                    self.energy_left /= 2
                    return

    def use_turn(self): # 결국 매 틱 실행되는 함수
        self.check_site()
        if self.energy_left >= self.max_calorie * self.threshold_birth :
            if 1 - self.birth_rate < random.random():
                self.make_child()

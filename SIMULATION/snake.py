import random
from animal import Animals,  Grid_size, Grid, Animal, Site_list_random
from lion import Lion
from leopard import Leopard

class Snake(Animals):
    max_life = 150
    min_life = 120
    site = 3
    birth_rate = 0.3
    hunting_rate = 0.7
    predator = ["Baboon"]
    food = ["Mouse"]
    calorie_waste_rate = 2
    max_calorie = 1000
    calorie = 400

    name = "Snake"

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
                    a = Snake(child_x, child_y, self.energy_left / 2)
                    self.energy_left /= 2
                    return

    def use_turn(self): # 결국 매 틱 실행되는 함수
        self.check_site()
        if self.energy_left >= self.max_calorie * self.threshold_birth :
            if 1 - self.birth_rate < random.random():
                self.make_child()

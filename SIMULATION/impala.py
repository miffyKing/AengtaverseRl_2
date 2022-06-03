import random
from animal import Animals, Grid_size, Grid_Grass, Grid, Animal, Site_list_random, Site_list_ordered, next_dir


class Impala(Animals):
    max_life = 150  # 600
    min_life = 100  # 400
    site = 3
    birth_rate = 0.85
    hunting_rate = 1
    predator = ["Lion", "Leopard"]
    food = ["Grass"]
    calorie = 300
    calorie_waste_rate = 0  # 초식동물의 경우, 칼로리 소모를 없애고, 번식하는 경우를 제한했다.
    max_calorie = 600  # 1000

    name = "Impala"

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
                    a = Impala(child_x, child_y, self.energy_left / 2)
                    self.energy_left /= 2
                    return

    def eat_food(self, x, y):
        # (x, y)의 있는 먹이를 먹어서 본인의 칼로리를 올리고, 해당 Grid의 원소를 0으로 바꾼다.
        # self.cnt += 1
        self.energy_left += Grid_Grass[x][y].calorie
        if(self.energy_left > self.max_calorie) :
            self.energy_left = self.max_calorie
        Grid_Grass[x][y] = 0
        if (1 - self.birth_rate) < random.random():
            self.make_child()

    def check_site(self):  # 틱에서 결국 실행되는 함수
        # 포식자 검색 & 먹이 검색
        # temp 로 표시 된 것 string으로 바꼈으니까 . grid[][]로 바꿔야함

        # 포식자 검색도 일단 가까이부터 하도록 변경
        for i in range(1, self.site + 1):
            k = random.randint(0, len(Site_list_random[i]) - 1)
            for j in range(0, len(Site_list_random[i])):
                next_x = self.x + Site_list_random[i][k - j][0]
                next_y = self.y + Site_list_random[i][k - j][1]
                if (next_x >= Grid_size):
                    next_x -= Grid_size
                if (next_y >= Grid_size):
                    next_y -= Grid_size

                if Grid[next_x][next_y] != 0:
                    for temp in self.predator:  # 포식자 검색
                        if Grid[next_x][next_y] != 0 and Grid[next_x][next_y].name == temp:
                            if Grid[next_x][next_y].hunting_rate > random.random():  # 포식자 감지 성공
                                # next_x, y가 포식자의 위치
                                # 검사할 사분면의 결정
                                if (self.x - next_x < 0):
                                    x_sign = -1
                                else:
                                    x_sign = 1
                                if (self.y - next_y < 0):  #
                                    y_sign = -1
                                else:
                                    y_sign = 1

                                for a in range(int(self.site / 2) + 1, 1, -1):
                                    t = random.randint(0, len(Site_list_ordered[a]) - 1)
                                    for b in range(0, len(Site_list_ordered[a])):
                                        # 비어있음을 검사
                                        temp_x = self.x + x_sign * Site_list_ordered[a][t - b][0]
                                        temp_y = self.y + y_sign * Site_list_ordered[a][t - b][1]
                                        if (temp_x >= Grid_size or temp_y >= Grid_size):
                                            temp_x = temp_x % Grid_size
                                            temp_y = temp_y % Grid_size
                                        if (Grid[temp_x][temp_y] == 0):
                                            self.move(temp_x - self.x, temp_y - self.y)
                                            return
                                # 포식자 검사에는 성공했지만, 도망가는 방향에 빈자리가 하나도 없어서 제자리에 정지
                                self.move(0, 0)
                                return

        for i in range(0, self.site + 1):
            k = random.randint(0, len(Site_list_random[i]) - 1)
            for j in range(0, len(Site_list_random[i])):
                next_x = self.x + Site_list_random[i][k - j][0]
                next_y = self.y + Site_list_random[i][k - j][1]
                if (next_x >= Grid_size):
                    next_x -= Grid_size
                if (next_y >= Grid_size):
                    next_y -= Grid_size

                min_distance = self.site + 1  # 먹이 탐색 최소 거리의 초기값 설정
                min_dirx = 0
                min_diry = 0

                for temp in self.food:  # 먹이 list 순회
                    if Grid_Grass[next_x][next_y] != 0 and Grid_Grass[next_x][next_y].name == temp:  # 해당 칸에 먹이 존재시
                        if Grid[next_x][next_y] == 0 or (next_x == self.x and next_y == self.y):
                            if max(abs(i), abs(j)) < min_distance: # 최소 거리 먹이 검사
                                min_distance = max(abs(i), abs(j))
                                min_dirx = next_x
                                min_diry = next_y
                                what_to_eat = temp
                if min_distance != self.site + 1:  # 발견한 경우,
                    # 해당 방향으로 move한다
                    if min_distance == 1:
                        # eat하고 move한다.
                        Animal[what_to_eat].remove(Grid_Grass[next_x][next_y])
                        self.eat_food(next_x, next_y)
                        self.move(min_dirx - self.x, min_diry - self.y)
                    else:
                        # move만 한다. (아직 충분히 가까이 있지 않음)
                        vec_x = min_dirx - self.x
                        vec_y = min_diry - self.y
                        x_sign = 0;
                        y_sign = 0
                        if (vec_x < 0):
                            x_sign = -1
                        elif (vec_x > 0):
                            x_sign = 1

                        if (vec_y < 0):
                            y_sign = -1
                        elif (vec_y > 0):
                            y_sign = 1

                        for a in range(1, int(self.site / 2) + 1):
                            t = random.randint(0, len(Site_list_ordered[a]) - 1)
                            for b in range(0, len(Site_list_ordered[a])):
                                # 비어있음을 검사
                                temp_x = self.x + x_sign * Site_list_ordered[a][t - b][0]
                                temp_y = self.y + y_sign * Site_list_ordered[a][t - b][1]
                                if (temp_x >= Grid_size or temp_y >= Grid_size):
                                    temp_x = temp_x % Grid_size
                                    temp_y = temp_y % Grid_size
                                if (Grid[temp_x][temp_y] == 0):
                                    self.move(temp_x - self.x, temp_y - self.y)
                                    return
                        # 포식자 검사에는 성공했지만, 도망가는 방향에 빈자리가 하나도 없어서 제자리에 정지
                        self.move(0, 0)
                    return

        # 포식자도 없고, 먹이 못 찾았을 경우
        for i in range(1, self.site + 1):
            k = random.randint(0, len(Site_list_random[i]) - 1)
            for j in range(0, len(Site_list_random[i])):
                next_x = self.x + Site_list_random[i][k - j][0]
                next_y = self.y + Site_list_random[i][k - j][1]
                if (next_x >= Grid_size):
                    next_x -= Grid_size
                if (next_y >= Grid_size):
                    next_y -= Grid_size
                if (Grid[next_x][next_y] == 0):
                    self.move(next_x - self.x, next_y - self.y)
                    return

        # 만약 이동하려햇는데 주변이 다 차있는 경우에는 제자리 이동
        self.move(0, 0)


    def use_turn(self):  # 결국 매 틱 실행되는 함수
        self.check_site()

import random
from animal import Grid, Grid_size, Grid_Grass, Animal, Site_list_random


class Animals_eat_plants:

    x = 0  # 동물의 X좌표
    y = 0  # 동물의 Y좌표
    energy_left = 0  # 동물의 남은 에너지(칼로리)
    calorie = 0  # 동물이 먹혔을 때 포식자가 얻는 칼로리
    site = 0  # 동물의 시야 범위
    birth_rate = 0  # 동물의 번식율 (%)
    hunting_rate = 0  # 동물의 사냥 성공 확률 (%)
    predator = []  # class의 객체의 포식자 name 담고 있을 list
    food = []  # class의 먹이 name를 담고 있을 list
    calorie_waste_rate = 0  # 동물의 tick 당 칼로리 소모량
    max_calorie = 0
    threshold_birth = 0.5

    name = "Animal_plant"

    def __init__(self, x, y, energy_left):
        self.energy_left = energy_left
        self.x = x
        self.y = y
        Grid[x][y] = self
        Animal[self.name].append(self)

    def move(self, x, y):  # 동물의 이동 함수 (self.x + x, self.y+y) 로 이동

        Grid[self.x][self.y] = 0  # 이동 전의 위치 비우기
        self.x = self.x + x  # x 좌표 이동
        self.y = self.y + y  # y 좌표 이동
        Grid[self.x][self.y] = self  # 이동

        if self.x < 0:
            self.x += Grid_size
        if self.y < 0:
            self.y += Grid_size

    def eat_food(self, x, y):
        # (x, y)의 있는 풀을 먹어서 본인의 칼로리를 올리고, 해당 Grid의 원소를 0으로 바꾼다.
        self.energy_left += Grid_Grass[x][y].calorie
        if self.energy_left > self.max_calorie:
            self.energy_left = self.max_calorie
        Grid_Grass[x][y] = 0

    def use_turn(self):  # 틱에서 결국 실행되는 함수
        # 포식자 검색 & 먹이 검색
        # temp 로 표시 된 것 string으로 바꼈으니까 . grid[][]로 바꿔야함

        # 시야 내를 다 검색하고,
        # (이 과정에서 정보를 저장해서 효율적으로 도주 경로 or 접근 경로를 구할 수 없나?)
        # 포식자 발견하면 바로 1번 액션 취하고
        # 먹이 발견하면 바로 2번 액션 취하고
        # 다 못 찾으면 가장 먼저 찾은 빈칸으로 이동

        # Map list = [Predator List, Food List, Free Space List] 를 저장?
        # Map List 원소를 넣을 때 label을 달아서 넣도록 하자
        next_x = 0
        next_y = 0
        move_flag = 0
        P_list = []  # Predator list
        F_list = []  # Food list
        Blank_list = []

        for i in range(0, self.site + 1):
            k = random.randint(0, len(Site_list_random[i]) - 1)
            for j in range(0, len(Site_list_random[i])):
                label = 0
                next_x = self.x + Site_list_random[i][k - j][0]
                next_y = self.y + Site_list_random[i][k - j][1]

                if next_x >= self.x and next_y > self.y: # (x >= 0, y > 0)
                    label = 1
                elif next_x < self.x and next_y >= self.y: # (x < 0, y >= 0)
                    label = 2
                elif next_x <= self.x and next_y < self.y: # (x <= 0, y < 0)
                    label = 4
                elif next_x > self.x and next_y <= self.y: # (x > 0, y <= 0)
                    label = 3

                if (next_x >= Grid_size):
                    next_x -= Grid_size
                if (next_y >= Grid_size):
                    next_y -= Grid_size

                if Grid[next_x][next_y] == 0:
                    Blank_list.append([next_x, next_y, label])
                elif Grid[next_x][next_y].name in self.predator:
                    P_list.append([next_x, next_y, label, Grid[next_x][next_y].name])

                if Grid_Grass[next_x][next_y] != 0:  # (next_x, next_y)에 풀이 있는 경우
                    F_list.append([next_x, next_y, label, "Grass"])


        # check PF list
        for Element in P_list:
            next_x = Element[0]
            next_y = Element[1]
            if Grid[next_x][next_y].hunting_rate < random.random():  # 포식자 감지 성공
                for Blank in Blank_list:  # 빈칸 검사
                    if (5 - Blank[2]) == Element[2]:  # 반대편 사분면에 있는 가까운 빈칸 발견시
                        next_x = Blank[0]
                        next_y = Blank[1]
                        move_flag = 1
                        break
            if move_flag == 1 :
                break

        for Element in F_list:
            if move_flag == 1:
                break
            next_x = Element[0]
            next_y = Element[1]

            # 풀 Grid가 비어있다는 보장이 없다..
            if max(abs(next_x - self.x), abs(next_y - self.y)) == 0:
                Animal["Grass"].remove(Grid_Grass[next_x][next_y])
                self.eat_food(next_x, next_y)
                move_flag = 1
                break
            elif max(abs(next_x - self.x), abs(next_y - self.y)) == 1:
                if Grid[next_x][next_y] == 0: # 풀이 있는 칸이 비어서 이동이 가능한 경우
                    Animal["Grass"].remove(Grid_Grass[next_x][next_y])
                    self.eat_food(next_x, next_y)
                    if 1 - self.birth_rate < random.random():
                        self.make_child(self.x, self.y)
                else : # 그 위에 다른 동물이 있는 경우? 일단 대기
                    next_x = self.x
                    next_y = self.y
                move_flag = 1
                break
            else:  # 먹이를 발견했지만 그렇게 가까이 있지는 않다면
                for Blank in Blank_list:  # 빈칸 검사
                    if Blank[2] == Element[2]:  # 같은 사분면에 있는 가까운 빈칸 발견시
                        next_x = Blank[0]
                        next_y = Blank[1]
                        move_flag = 1
                        break

        if move_flag == 0:  # 포식자도, 먹이도 찾지 못한 경우
            if (len(Blank_list) != 0):  # Blank 존재시
                next_x = Blank_list[0][0]
                next_y = Blank_list[0][1]

        previous_x = self.x
        previous_y = self.y
        self.move(next_x - previous_x, next_y - previous_y)

        # make child 를 여기 하면?
        # 1. 내가 (x,y)로 이동했다 => 가장 가까운 빈칸이 (x, y)일 것이다.
        # 2. 내가 이동 못 했다. => 주변이 꽉 차 있음 => 애초에 make child 불가
        # 3. 쫓기는 도중이면 번식 X
        # move 이후 삭제 됐는지 검사 (사망 검사)

    def make_child(self, x, y):
        # 일정 칼로리이상이면 번식한다.
        # 움직이고나서 실행된다
        a = Animals_eat_plants(x, y, self.energy_left / 2)
        self.energy_left /= 2


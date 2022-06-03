import random

Grid_size = 100
Grid = [[0] * Grid_size for i in range(Grid_size)]
Grid_Grass = [[0] * Grid_size for i in range(Grid_size)]
# 종의 Object들이 들어갈 리스트
Lion_list = []
Impala_list = []
Baboon_list = []
Rhino_list = []
Grass_list = []
Leopard_list = []
Mouse_list = []
Grasshopper_list = []
Skunk_list = []
Snake_list = []

# 이름을 통해 리스트에 접근할 수 있도록 해주는 딕셔너리, 새로운 종의 추가마다 추가 필요
Animal = {"Lion" : Lion_list, "Impala" : Impala_list, "Baboon" : Baboon_list,
          "Rhino" : Rhino_list, "Grass" : Grass_list, "Leopard" : Leopard_list,
          "Mouse" : Mouse_list, "Grasshopper": Grasshopper_list, "Skunk": Skunk_list,
          "Snake" : Snake_list}
# 종의 이름들을 담고 있는 리스트
Animal_Name = ["Lion", "Impala", "Baboon", "Rhino",
               "Leopard", "Mouse", "Grasshopper",
               "Skunk", "Snake", "Grass" ]
# 종들의 리스트들을 모아놓은 리스트
Animal_lists = [Lion_list, Impala_list, Baboon_list,
                Rhino_list, Leopard_list, Mouse_list,
                Grasshopper_list, Skunk_list, Snake_list, Grass_list]
# 시야 내의 검색을 위한 list 2개
# 내 주위를 랜덤하게 검색
Site_list_random = [ [0]  for i in range(0, 7)] # 최대 5까지 했는데, 동물들의 site를 구해서 다시 최대값을 바꿀 필요가 있을수도
Site_list_ordered = [ [0]  for i in range(0, 7)] # 부호마다 사분면을 검색하기 위해 사용되는 리스트

# 방향 지정을 위한 함수
def next_dir(x):
    if x > 0:
        x = 1
    elif x < 0:
        x = -1
    else:
        x = 0
    return x


# 위의 리스트의 값을 초기화
def make_Site_list_random(k):

    if k==0:
        Site_list_random[0] = [[0, 0]]
        return

    for i in range(-k, k+1):
        for j in range(-k, k+1):
            tmp = [i, j]
            if i**2 + j**2 >= k**2 :
                Site_list_random[k].append(tmp)
    Site_list_random[k].remove(0)

def make_Site_list_ordered(k):

    if k==0:
        Site_list_random[0] = [[0, 0]]
        return

    for i in range(0, k+1):
        for j in range(0, k+1):
            tmp = [i, j]
            if(i**2 + j**2 >= k**2):
                Site_list_ordered[k].append(tmp)
    Site_list_ordered[k].remove(0)


class Animals:

    x = 0  # 동물의 X좌표
    y = 0  # 동물의 Y좌표
    energy_left = 0  # 동물의 남은 에너지(칼로리)
    time_left = 0  # 동물의 남은 수명 (단위: tick)
    calorie = 0  # 동물이 먹혔을 때 포식자가 얻는 칼로리
    site = 0  # 동물의 시야 범위
    birth_rate = 0  # 동물의 번식율 (%)
    hunting_rate = 0  # 동물의 사냥 성공 확률 (%)
    predator = ["Lion"]  # class의 객체의 포식자 name 담고 있을 list
    food = []  # class의 먹이 name를 담고 있을 list
    calorie_waste_rate = 0  # 동물의 tick 당 칼로리 소모량
    max_life = 0
    min_life = 0
    max_calorie = 0
    threshold_birth = 0.8
    cnt = 0

    name = "Animals"

    def __init__(self, x, y, energy_left):
        self.time_left = random.randint(self.min_life, self.max_life)
        self.energy_left = energy_left
        self.x = x
        self.y = y
        Animal[self.name].append(self)
        Grid[x][y] = self

    def move(self, x, y):  # 동물의 이동 함수 (self.x + x, self.y+y) 로 이동

        Grid[self.x][self.y] = 0 # 이동 전의 위치 비우기
        self.x = self.x + x  # x 좌표 이동
        self.y = self.y + y  # y 좌표 이동
        Grid[self.x][self.y] = self # 이동
        self.energy_left -= self.calorie_waste_rate  #이동하느라 에너지 소모
        self.time_left -= 1 # 수명 깍임

        if self.time_left <= 0 or self.energy_left <= 0: #  수명 다 살았다면
            #여기서 죽는거 구현, 애니멀 리스트에서 빼주고, 좌표 0으로 바꿔주기git add
            Grid[self.x][self.y] = 0
            Animal[self.name].remove(self)
            return
        if self.x < 0:
            self.x += Grid_size
        if self.y < 0:
            self.y += Grid_size

    def eat_food(self, x, y):
        # (x, y)의 있는 먹이를 먹어서 본인의 칼로리를 올리고, 해당 Grid의 원소를 0으로 바꾼다.
        self.cnt += 1
        self.energy_left += Grid[x][y].calorie
        Grid[x][y] = 0
        # 해당 리스트 역시 순회해서

    def check_site(self):  # 틱에서 결국 실행되는 함수
        # 포식자 검색 & 먹이 검색
        # temp 로 표시 된 것 string으로 바꼈으니까 . grid[][]로 바꿔야함

        # 포식자 검색도 일단 가까이부터 하도록 변경
        for i in range(0, self.site + 1):
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
                                # self.move(self.x - next_x, self.y - next_y, 2)
                                # 검사할 사분면의 결정
                                x_sign = 0; y_sign = 0
                                if (self.x - next_x < 0):
                                    x_sign = -1
                                elif (self.x - next_x > 0):
                                    x_sign = 1
                                if (self.y - next_y < 0):
                                    y_sign = -1
                                elif (self.y - next_y > 0):
                                    y_sign = 1

                                for a in range(1, int(self.site/2) + 1):
                                    t = random.randint(0, len(Site_list_ordered[a]) - 1)
                                    for b in range(0, len(Site_list_ordered[a])):
                                        # 비어있음을 검사
                                        temp_x = self.x + x_sign * Site_list_ordered[a][t - b][0]
                                        temp_y = self.y + y_sign * Site_list_ordered[a][t - b][1]
                                        if(temp_x >= Grid_size or temp_y >= Grid_size):
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
                    if Grid[next_x][next_y] != 0 and Grid[next_x][next_y].name == temp:  # 해당 칸에 먹이 존재시
                        if max(abs(i), abs(j)) < min_distance:  # 최소 거리 먹이 검사
                            min_distance = max(abs(i), abs(j))
                            min_dirx = next_x
                            min_diry = next_y
                            what_to_eat = temp
                if min_distance != self.site + 1:  # 발견한 경우,
                    #해당 방향으로 move한다
                    if min_distance == 1:
                        # eat하고 move한다.
                        Animal[what_to_eat].remove(Grid[min_dirx][min_diry])
                        self.eat_food(min_dirx, min_diry)
                        self.move(min_dirx - self.x, min_diry - self.y)
                        return
                    else:
                        #move만 한다. (아직 충분히 가까이 있지 않음)
                        vec_x = min_dirx - self.x
                        vec_y = min_diry - self.y
                        x_sign = 0; y_sign = 0
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
                        # 먹이 검사에는 성공했지만, 먹이로 가는 방향에 빈자리가 하나도 없어서 제자리에 정지
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
                    a = Animals(child_x, child_y, self.energy_left / 2)
                    self.energy_left /= 2
                    Grid[child_x][child_y] = a
                    return
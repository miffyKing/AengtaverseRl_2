import random
from lion import Lion
from impala import Impala
from baboon import Baboon
from animal import Grid, Grid_size, Animal_lists, Grid_Grass, make_Site_list_random, make_Site_list_ordered, Animal_Name
from rhino import Rhino
from grass import Grass
from leopard import Leopard
from mouse import Mouse
from grasshopper import Grasshopper
from skunk import Skunk
from snake import Snake
import numpy as np
cnt = 0
def print_Grid(cnt):
    print("Printing Grid ", cnt)
    for i in range(0, Grid_size):
        for j in range(0, Grid_size):
            if(Grid[i][j] == 0) :
                print(0, end=' ')
            elif Grid[i][j].name == "Lion":
                print(1, end=' ')
            elif Grid[i][j].name == "Impala":
                print(2, end=' ')
            elif Grid[i][j].name == "Baboon":
                print(3, end=' ')
            elif Grid[i][j].name == "Rhino":
                print(4, end=' ')
            elif Grid[i][j].name == "Leopard":
                print(5, end=' ')
            elif Grid[i][j].name == "Mouse":
                print(6, end=' ')
            elif Grid[i][j].name == "Grasshopper":
                print(7, end=' ')
            elif Grid[i][j].name == "Skunk":
                print(8, end=' ')
            elif Grid[i][j].name == "Snake":
                print(9, end=' ')

        print()
    print()

Animal_class = [Lion, Impala, Baboon, Rhino, Leopard, Mouse, Grasshopper, Skunk, Snake, Grass]

def init_background():
    for i in range(0, Grid_size):
        for j in range(0, Grid_size):
            Grid[i][j] = 0
            Grid_Grass[i][j] = 0

    for i in Animal_lists:
        i.clear()

def init_simul():
    for i in range(0, 7):
        make_Site_list_random(i)
        make_Site_list_ordered(i)


def gen_species(idx, num):
    # Animal_Class[idx]의 종을 num만큼 생성
    # 초기 생성 위치는 남은 자리 중에서 랜덤하게, 초기 에너지는 최대 에너지의 절반
    Grid_tmp = []
    for i in range(0, Grid_size):
        for j in range(0, Grid_size):
            tmp = [i, j]
            if Grid[i][j] == 0:
                Grid_tmp.append(tmp)

    length_Grid_left = len(Grid_tmp)
    for i in range(0, num):
        if(length_Grid_left == 0):
            break
        rand = random.randint(0, len(Grid_tmp) - 1)
        x = Grid_tmp[rand][0]
        y = Grid_tmp[rand][1]
        a = Animal_class[idx](x, y, int(Animal_class[idx].max_calorie/2))
        del Grid_tmp[rand]
        length_Grid_left -= 1

def gen_grass(idx, num):
    Grid_tmp = []
    for i in range(0, Grid_size):
        for j in range(0, Grid_size):
            tmp = [i, j]
            if Grid_Grass[i][j] == 0:
                Grid_tmp.append(tmp)

    length_Grid_left = len(Grid_tmp)

    for i in range(0, num):
        if (length_Grid_left == 0):
            break
        rand = random.randint(0, len(Grid_tmp) - 1)
        x = Grid_tmp[rand][0]
        y = Grid_tmp[rand][1]
        a = Animal_class[idx](x, y, int(Animal_class[idx].max_calorie / 2))
        del Grid_tmp[rand]
        length_Grid_left -= 1

def gen_animals(lists):
    # lists 내부의 숫자만큼 각 종을 생성
    length = len(lists)
    for i in range(0, length - 1):
        gen_species(i, lists[i])
    gen_grass(length-1 ,lists[length-1])

def simulate(lists):

    init_background()
    gen_animals(lists)
    cnt = 0
    length = len(lists)
    while(cnt < 1000):
        # print(cnt, end=" ")
        cnt+=1
        # Problem is removing lion during the iteration

        for i in range(0, length-1):
            list_of_animal = Animal_lists[i]
            tmp = len(list_of_animal)
            j = 0
            while j < len(list_of_animal):
                list_of_animal[j].use_turn()
                j+=1
                if tmp != len(list_of_animal):
                    tmp = len(list_of_animal)
                    j -= 1
                if (tmp == 0):
                    break
            # print(len(list_of_animal), end=" ")
        # make grass
        gen_grass(length -1, 50)
        # print(len(Animal_lists[length-1]), end=" ")
        # print()
        # # 7~14, 21~28, 35~42
        if (cnt % 28 > 14) and (cnt % 28 < 28):
            gen_grass(length - 1, 50)
        for i in range(0, 10):
            if len(Animal_lists[i]) == 0:
                #print("No", end=" ")
                #print(Animal_Name[i])
                #for i in range(0, len(Animal_lists)):
                #    print(len(Animal_lists[i]), end=" ")
                #print()
                return cnt

    return cnt

def simulate2(lists):
    tick = 0
    for i in range(0,10):
        tick += lists[i]*i
    tick = tick%17 * 10 + np.random.randint(0,31)- 15
    return tick


#[Lion, Impala, Baboon, Rhino,  Leopard, Mouse, Grasshopper, Skunk,Snake, Grass,]
input = [35, 80, 75, 40, 35, 50, 50, 75, 50, 1250]
#Threshold  [50, 200, 150, 80, 50, 100, 150, 150, 100, 2500]

init_simul()
print("simulate with array : ", input)
for i in range(0, 5):
    print("simulation", i, ":", simulate(input))
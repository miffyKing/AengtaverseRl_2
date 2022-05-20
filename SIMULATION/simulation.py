import random
from lion import Lion
from impala import Impala
from baboon import Baboon
from animal import Grid, Grid_size, Animal_lists, Grid_Grass, make_Site_list_random, make_Site_list_ordered
from rhino import Rhino
from grass import Grass
from leopard import Leopard
from mouse import Mouse
from grasshopper import Grasshopper
from skunk import Skunk
from snake import Snake

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
        Animal_lists[idx].append(a)
        Grid[x][y] = a
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
        Animal_lists[idx].append(a)
        Grid_Grass[x][y] = a
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
        #print(cnt, end=" ")
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
            #print(len(list_of_animal), end=" ")
        # make grass
        gen_grass(length -1, 10)
        #rint(len(Animal_lists[length-1]), end=" ")
        #print()
        if(len(Animal_lists[0]) == 0):
            #print("No Lions");
            return cnt
        if(len(Animal_lists[1])==0):
            #print("No Impala")
            return cnt
        if (len(Animal_lists[2]) == 0):
            #print("No Baboon")
            return cnt
        if (len(Animal_lists[3]) == 0):
            #print("No Rhino")
            return cnt
        if (len(Animal_lists[4]) == 0):
            #print("No Grass")
            return cnt
        if (len(Animal_lists[5]) == 0):
            #print("No Leopard")
            return cnt
        if (len(Animal_lists[6]) == 0):
            #print("No Mouse")
            return cnt
        if (len(Animal_lists[7]) == 0):
            #print("No Grasshopper")
            return cnt
        if (len(Animal_lists[8]) == 0):
            #print("No Skunk")
            return cnt
        if (len(Animal_lists[9]) == 0):
            #print("No Snake")
            return cnt

            #나중에 for문으로 고쳐!
    return cnt

#input = [50, 200, 80, 80, 80, 80, 80, 80, 80, 1000 ]
#[Lion, Impala, Baboon, Rhino,  Leopard, Mouse, Grasshopper, Skunk,Snake, Grass,]

#print(simulate(input))
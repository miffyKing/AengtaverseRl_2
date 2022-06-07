from typing import Union

import numpy as np

import gym
from gym import spaces
import sys, os
sys.path.append("C:\\Users\\kenny\\PycharmProjects\\CartpoleDQN\\SIMULATION")
from SIMULATION import simulation
#sys.path.append("C:\\Users\\82103\\PycharmProjects\\pythonProject3\\AengtaverseRl_2\\SIMULATION")
#from AengtaverseRl_2.SIMULATION import simulation

class EcoSystemEnv(gym.Env[np.ndarray, Union[int, np.ndarray]]):
    def __init__(self):
        self.threshold = np.array([50, 200, 150, 80, 50, 100, 150, 150, 100, 2500], dtype=np.int,)
        self.action_space = spaces.Discrete(20)  # 10 species inc/dec 0~19
        self.observation_space = spaces.Box(0, self.threshold, dtype=np.int)
        self.state = None
        self.tick = 0

    def step(self, action):
        a0, a1, a2, a3, a4, a5, a6, a7, a8, a9 = self.state
        if action == 0:
            a0 -= self.threshold[0]/10
        elif action == 1:
            a1 -= self.threshold[1]/10
        elif action == 2:
            a2 -= self.threshold[2]/10
        elif action == 3:
            a3 -= self.threshold[3]/10
        elif action == 4:
            a4 -= self.threshold[4]/10
        elif action == 5:
            a5 -= self.threshold[5]/10
        elif action == 6:
            a6 -= self.threshold[6]/10
        elif action == 7:
            a7 -= self.threshold[7]/10
        elif action == 8:
            a8 -= self.threshold[8]/10
        elif action == 9:
            a9 -= self.threshold[9]/10
        elif action == 10:
            a0 += self.threshold[0]/10
        elif action == 11:
            a1 += self.threshold[1]/10
        elif action == 12:
            a2 += self.threshold[2]/10
        elif action == 13:
            a3 += self.threshold[3]/10
        elif action == 14:
            a4 += self.threshold[4]/10
        elif action == 15:
            a5 += self.threshold[5]/10
        elif action == 16:
            a6 += self.threshold[6]/10
        elif action == 17:
            a7 += self.threshold[7]/10
        elif action == 18:
            a8 += self.threshold[8]/10
        elif action == 19:
            a9 += self.threshold[9]/10
        self.state = (a0, a1, a2, a3, a4, a5, a6, a7, a8, a9)
        sim_tick = simulation.simulate(np.array(self.state, dtype=np.int))
        done = bool( # done -> 충분한 시간이 흐름 Good / 한 종의 멸종 bad/ 한 종이 오바 bad
            (sim_tick >= 160) or
            (not (a0 and a1 and a2
             and a3 and a4
             and a5 and a6
             and a7 and a8 and a9)) or
            (a0 > self.threshold[0] or a1 > self.threshold[1] or
             a2 > self.threshold[2] or a3 > self.threshold[3] or
             a4 > self.threshold[4] or a5 > self.threshold[5] or
             a6 > self.threshold[6] or a7 > self.threshold[7] or
             a8 > self.threshold[8] or a9 > self.threshold[9]
            )
        )

        print("Lasted tick : ",sim_tick)
        if not done:  #생태계 : 초기값이 simul 결과 goal을 넘기지 못했지만 범위 내
            reward = (sim_tick - 159)/10
        elif sim_tick >= 160: #생태계 : 초기값이 simul 결과 goal을 넘김
            reward = (sim_tick - 159) * 10
        else: #생태계 : 초기값이 simul 결과 goal을 넘기지 못했고 범위를 넘겼다.
            reward = -3000

        return np.array(self.state, dtype=np.int), reward, done

    def reset(self, animal_array):
        self.state = animal_array
        return self.state

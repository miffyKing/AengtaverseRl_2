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
    """
    ### Description
    This environment corresponds to the version of the cart-pole problem
    described by Barto, Sutton, and Anderson in ["Neuronlike Adaptive Elements That Can Solve Difficult Learning Control Problem"](https://ieeexplore.ieee.org/document/6313077).
    A pole is attached by an un-actuated joint to a cart, which moves along a
    frictionless track. The pendulum is placed upright on the cart and the goal is to balance the pole by applying forces in the left and right direction on the cart.
    ### Action Space
    The action is a `ndarray` with shape `(1,)` which can take values `{0, 1}` indicating the direction of the fixed force the cart is pushed with.
    | Num | Action                 |
    |-----|------------------------|
    | 0   | Push cart to the left  |
    | 1   | Push cart to the right |
    **Note**: The velocity that is reduced or increased by the applied force is not fixed and it depends on the angle the pole is pointing. The center of gravity of the pole varies the amount of energy needed to move the cart underneath it
    ### Observation Space
    The observation is a `ndarray` with shape `(4,)` with the values corresponding to the following positions and velocities:
    | Num | Observation           | Min                  | Max                |
    |-----|-----------------------|----------------------|--------------------|
    | 0   | Cart Position         | -4.8                 | 4.8                |
    | 1   | Cart Velocity         | -Inf                 | Inf                |
    | 2   | Pole Angle            | ~ -0.418 rad (-24°)  | ~ 0.418 rad (24°)  |
    | 3   | Pole Angular Velocity | -Inf                 | Inf                |
    **Note:** While the ranges above denote the possible values for observation space of each element, it is not reflective of the allowed values of the state space in an unterminated episode. Particularly:
    -  The cart x-position (index 0) can be take values between `(-4.8, 4.8)`, but the episode terminates if the cart leaves the `(-2.4, 2.4)` range.
    -  The pole angle can be observed between  `(-.418, .418)` radians (or **±24°**), but the episode terminates if the pole angle is not in the range `(-.2095, .2095)` (or **±12°**)
    ### Rewards
    Since the goal is to keep the pole upright for as long as possible, a reward of `+1` for every step taken, including the termination step, is allotted. The threshold for rewards is 475 for v1.
    ### Starting State
    All observations are assigned a uniformly random value in `(-0.05, 0.05)`
    ### Episode Termination
    The episode terminates if any one of the following occurs:
    1. Pole Angle is greater than ±12°
    2. Cart Position is greater than ±2.4 (center of the cart reaches the edge of the display)
    3. Episode length is greater than 500 (200 for v0)
    ### Arguments
    ```
    gym.make('CartPole-v1')
    ```
    No additional arguments are currently supported.
    """

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 50}

    def __init__(self):
        self.threshold = np.array([50, 200, 150, 80, 50, 100, 150, 150, 100, 2500], dtype=np.int,)
        self.action_space = spaces.Discrete(20)  # 10 species inc/dec 0~19
        #self.action_space = spaces.Discrete(8)  # test

        self.observation_space = spaces.Box(0, self.threshold, dtype=np.int)
        self.state = None
        self.tick = 0

    def step(self, action):
        #print("action : ",action)
        a0, a1, a2, a3, a4, a5, a6, a7, a8, a9 = self.state
        if action == 0:
            a0 -= 5
        elif action == 1:
            a1 -= 20
        elif action == 2:
            a2 -= 15
        elif action == 3:
            a3 -= 8
        elif action == 4:
            a4 -= 5
        elif action == 5:
            a5 -= 10
        elif action == 6:
            a6 -= 15
        elif action == 7:
            a7 -= 15
        elif action == 8:
            a8 -= 10
        elif action == 9:
            a9 -= 250
        elif action == 10:
            a0 += 5
        elif action == 11:
            a1 += 20
        elif action == 12:
            a2 += 15
        elif action == 13:
            a3 += 8
        elif action == 14:
            a4 += 5
        elif action == 15:
            a5 += 10
        elif action == 16:
            a6 += 15
        elif action == 17:
            a7 += 15
        elif action == 18:
            a8 += 10
        elif action == 19:
            a9 += 250
        #print("B : ",self.state)
        self.state = (a0, a1, a2, a3, a4, a5, a6, a7, a8, a9)
        #print("A : ", self.state)
        sim_tick = simulation.simulate(np.array(self.state, dtype=np.int))
        done = bool( # done -> 충분한 시간이 흐름 Good / 한 종의 멸종 bad/ 한 종이 오바 bad
            (sim_tick >= 150) or
            (not (a0 and a1 and a2
             and a3 and a4
             and a5 and a6
             and a7 and a8 and a9)) or #Max 값 넘어가는 것도 설정해야함
            (a0 > self.threshold[0] or a1 > self.threshold[1] or
             a2 > self.threshold[2] or a3 > self.threshold[3] or
             a4 > self.threshold[4] or a5 > self.threshold[5] or
             a6 > self.threshold[6] or a7 > self.threshold[7] or
             a8 > self.threshold[8] or a9 > self.threshold[9]
            )
        )

        print("Lasted tick : ",sim_tick)
        if not done:  #생태계 : 초기값이 범위 내 #임의의 식 학습 : 범위 안에 있지만 tick 이 0을 못넘겼다
            reward = (sim_tick - 149)/10 #simulation 이면 sim_tick 줘도 될듯
        elif sim_tick >= 150:
            reward = (sim_tick - 149) * 10 # 이거는 진짜 잘한거니깐 sim_tick * 5 줘도 될듯?
        else:
            reward = -3000

        return np.array(self.state, dtype=np.int), reward, done

    def reset(self, animal_array):
        self.state = animal_array
        return self.state
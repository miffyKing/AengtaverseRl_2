import Env
import numpy as np
import tensorflow as tf
from keras.layers import Dense
from keras.initializers.initializers_v2 import RandomUniform
from keras.optimizers.optimizer_v2.adam import Adam

import sys, os
sys.path.append("C:\\Users\\kenny\\PycharmProjects\\CartpoleDQN\\SIMULATION")
from SIMULATION import simulation

#sys.path.append("C:\\Users\\82103\\PycharmProjects\\pythonProject3\\AengtaverseRl_2\\SIMULATION")
#from AengtaverseRl_2.SIMULATION import simulation

class A2C(tf.keras.Model):
    def __init__(self, action_size):
        super(A2C, self).__init__()
        self.actor_fc = Dense(24, activation='tanh')
        self.actor_out = Dense(action_size, activation='softmax',
                               kernel_initializer=RandomUniform(-1e-3, 1e-3))
        self.critic_fc1 = Dense(24, activation='tanh')
        self.critic_fc2 = Dense(24, activation='tanh')
        self.critic_out = Dense(1,
                                kernel_initializer=RandomUniform(-1e-3, 1e-3))

    def call(self, x):
        actor_x = self.actor_fc(x)
        policy = self.actor_out(actor_x)

        critic_x = self.critic_fc1(x)
        critic_x = self.critic_fc2(critic_x)
        value = self.critic_out(critic_x)
        return policy, value

class A2CAgent:
    def __init__(self, action_size):
        self.render = False
        # 행동의 크기 정의
        self.action_size = action_size

        # 액터-크리틱 하이퍼파라미터
        self.discount_factor = 0.99
        self.learning_rate = 0.001

        # 정책신경망과 가치신경망 생성
        self.model = A2C(self.action_size)
        # 최적화 알고리즘 설정, 미분값이 너무 커지는 현상을 막기 위해 clipnorm 설정
        self.optimizer = Adam(learning_rate=self.learning_rate, clipnorm=5.0)

    # 정책신경망의 출력을 받아 확률적으로 행동을 선택
    def get_action(self, state):
        policy, _ = self.model(state)
        policy = np.array(policy[0])
        return np.random.choice(self.action_size, 1, p=policy)[0]

    # 각 타임스텝마다 정책신경망과 가치신경망을 업데이트
    def train_model(self, state, action, reward, next_state, done):
        model_params = self.model.trainable_variables
        with tf.GradientTape() as tape:
            policy, value = self.model(state)
            _, next_value = self.model(next_state)
            target = reward + (1 - done) * self.discount_factor * next_value[0]

            # 정책 신경망 오류 함수 구하기
            one_hot_action = tf.one_hot([action], self.action_size)
            action_prob = tf.reduce_sum(one_hot_action * policy, axis=1)
            cross_entropy = - tf.math.log(action_prob + 1e-5)
            advantage = tf.stop_gradient(target - value[0])
            actor_loss = tf.reduce_mean(cross_entropy * advantage)

            # 가치 신경망 오류 함수 구하기
            critic_loss = 0.5 * tf.square(tf.stop_gradient(target) - value[0])
            critic_loss = tf.reduce_mean(critic_loss)

            # 하나의 오류 함수로 만들기
            loss = 0.2 * actor_loss + critic_loss

        # 오류함수를 줄이는 방향으로 모델 업데이트
        grads = tape.gradient(loss, model_params)
        self.optimizer.apply_gradients(zip(grads, model_params))
        return np.array(loss)


if __name__ == "__main__":
    env = Env.EcoSystemEnv()
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n

    # 액터-크리틱(A2C) 에이전트 생성
    agent = A2CAgent(action_size)

    scores, episodes = [], []
    score_avg = 0
    success_in_row = 0
    fin_ep = False
    # [Lion, Impala, Baboon, Rhino,  Leopard, Mouse, Grasshopper, Skunk,Snake, Grass,]
    animal_array = [25, 100, 75, 40, 25, 50, 75, 75, 50, 1250]
    prev_state = animal_array
    prev_state = np.reshape(prev_state, [1, state_size])
    num_episode = 3000
    simulation.init_simul()

    step_list = []
    step_list_fail = []
    f = open("Test4.txt", 'w')

    for e in range(num_episode):
        done = False
        score = 0
        loss_list = []
        state = env.reset(animal_array)
        state = np.reshape(state, [1, state_size])
        step_in_ep = 0
        while not done:
            step_in_ep += 1
            if agent.render:
                env.render()

            action = agent.get_action(state)
            next_state, reward, done = env.step(action)
            next_state = np.reshape(next_state, [1, state_size])

            loss = agent.train_model(state, action, reward, next_state, done)
            loss_list.append(loss)
            state = next_state
            print("Episode", e, "step",step_in_ep,"Simulated with state : ", state)
            if done:
                # 에피소드마다 학습 결과 출력
                if reward != -3000:
                    print("Success, Ecosystem's Animal Number : ",state)
                    f.writelines(["Success, Ecosystem's Animal Number : ",str(state),"\n"])
                    if np.array_equal(prev_state,state):
                        success_in_row += 1
                        if success_in_row == 5:
                            fin_ep = True
                            break
                    else :
                        success_in_row = 0
                    step_list.append([e, step_in_ep])
                else:
                    success_in_row = 0
                    print("Fail, Ecosystem's Animal Number : ",state)
                    f.writelines(["Fail, Ecosystem's Animal Number : ",str(state),"\n"])
                    step_list_fail.append([e, step_in_ep])
                print("SUCCESS : ", step_list)
                print("FAIL ", step_list_fail)
                prev_state = state
                step_in_ep = 0

        if fin_ep:
            f.close()
            break

    if not fin_ep:
        print("Decrease the goal or increase the number of episodes")
        f.close()
    else:
        f = open("animal_array.txt", 'w')
        f.writelines(str(prev_state))
        f.close()



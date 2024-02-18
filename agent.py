import numpy as np
import pickle

class QLearningAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.q_table = [[0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0]]

        self.learning_rate = 0.1
        self.discount_factor = 0.99
        self.epsilon = 1.0
        self.epsilon_decay = 0.999
        self.epsilon_min = 0.01

    def choose_action(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        else:
            return self.q_table[state].index(max(self.q_table[state]))

    def learn(self, state, action, reward, next_state, done):
        q_value = self.q_table[state][action]
        next_max = self.q_table[next_state][self.q_table[next_state].index(max(self.q_table[next_state]))]
        target = reward + (1 - done) * self.discount_factor * next_max
        self.q_table[state][action] += self.learning_rate * (target - q_value)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save_model(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_model(self, filename):
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)

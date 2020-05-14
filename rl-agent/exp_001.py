#!/usr/bin/env python
# coding: utf-8

# # Experiment 1
#
#
# **Overview**:
#
# Two virtual networks, one with IDS one with IPS. Hosts running a Google Search for benign and a SYN attack for malicious.
#
# **Actions**: toggle VN
#
# **State**: where (which VN) each host is + last N IDS alerts for each host
#
# **Reward**: XNOR of current VN state and desired state (dumb)

# In[1]:


from bella.ciao import GemelEnv

import time
import os
import threading
import gym
import multiprocessing
import numpy as np
from queue import Queue
import argparse
import matplotlib.pyplot as plt
import enum

from keras.models import Sequential
from keras.layers import Dense, BatchNormalization
from keras.optimizers import Adam
from keras.backend import tensorflow_backend as K

from IPython.core.display import display, HTML, clear_output


# In[2]:


EPSILON = 0.1
EXPLORATION_DECAY = 0.99
GAMMA = 0.99


# In[3]:


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()



# ## DQN Agent

# In[4]:


class DQNAgent:

    class StateModel(enum.Enum):
        VN_ONLY = 1
        IDS = 2

    def __init__(self, env, max_eps, period=10,
                 state_mode=StateModel.IDS, model=None,
                 gamma=GAMMA, max_epsilon=EPSILON,
                 epsilon_decay=EXPLORATION_DECAY):

        self.env = env
        self.max_episodes = max_eps
        self.epsilon = max_epsilon
        self.max_epsilon = max_epsilon
        self.epsilon_dacay = epsilon_decay
        self.period = period
        self.state_mode = state_mode
        self.gamma = gamma
        self.model = model or self._create_model()


    def _create_model(self):
        """
        Builds a neural net model to digest the state
        """
        model = Sequential()
        model.add(Dense(
            5,
            # input_shape=,
            input_shape=(len(self.env._hosts_sorted_by_id),) \
                    if self.state_mode == DQNAgent.StateModel.VN_ONLY \
                    else self.env.observation_shape(),
            activation="relu"
        ))
        # model.add(Dense(20, activation="relu"))
        model.add(Dense(self.env.action_space.n, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=0.001))
        model.summary()
        return model

    def _to_feature_vector(self, state):
        if self.state_mode == DQNAgent.StateModel.VN_ONLY:
            return state[0]
        elif self.state_mode == DQNAgent.StateModel.IDS:
            return np.concatenate((state[0], state[1].flatten()))
        else:
            raise Exception(f"state model {self.state_mode} unknown")

    def train(self):

        histories = []

        # train for max_eps episodes
        for episode in range(1, self.max_episodes + 1):

            printProgressBar(episode, self.max_episodes)

            # start at random position
            _, terminal, step = self.env.reset(), False, 0

            time.sleep(self.period)

            state = self.env.state()

            # flatten state
            state = self._to_feature_vector(state)

            history = []

            # iterate step-by-step
            while not terminal:

                step += 1

                # pick action based on policy
                action, is_random = self.policy(state)

                print()
                print(f"Taking action {action}")

                # run action and get reward
                state_next_raw, reward, terminal = self.env.step(action)

                # instead of using the immediate next state, wait for it to simmer
                if self.period > 0:
                    time.sleep(self.period)
                    state_next_raw = self.env.state()

                # flatten state
                state_next = self._to_feature_vector(state_next_raw)

                print()
                print(f"Step {step} reward={reward} new_state={state_next_raw}")

                # # this makes sense in an episodic environement
                # # where a terminal state means "losing"
                # if terminal:
                #    reward *= -1

                preds = self.model.predict([[state_next]])
                next_scores_prediction = preds[0]

                print(f"Predicted scores for each action in next step: {next_scores_prediction}")

                # compute target Q
                q_target = ( reward + self.gamma * np.amax(next_scores_prediction) )                         if not terminal else reward

                # update model
                q_updated = self.model.predict([[state]])[0]
                q_updated[action] = q_target
                self.model.fit([[state]], [[q_updated]], verbose=0)

                # update current state
                state = state_next

                # update history
                history.append({
                    "time": step,
                    "action": action,
                    "reward": reward,
                    "state": state_next_raw[0].tolist(),
                    "random": is_random,
                    "prediction": preds,
                })

            histories.append(history)

            # apply exploration decay
            self.epsilon *= self.epsilon_dacay
            print(f"Epsilon reduced to {self.epsilon}")

        return histories

    def policy(self, state):
        if np.random.rand() < self.epsilon:
            print("PERFORMING RANDOM ACTION")
            return np.random.randint(self.env.action_space.n), True
        else:
            expected_rewards = self.model.predict([[state]])[0]
            return np.argmax(expected_rewards), False

    def test(self):

        state, done = self.env.reset(), False
        total_reward = 0

        while not done:
            exp_rew = self.model.predict([[state]])[0]
            action = np.argmax(exp_rew)
            new_state, reward, done = self.env.step(action)
            total_reward += reward
            self.env.render()
            time.sleep(0.05)
            state = new_state

        # self.env.close()
        print(f"Total reward: {total_reward}")


# In[30]:


def create_model_1(env):
    """
    Builds a neural net model to digest the state
    """
    model = Sequential()
    model.add(Dense(
        5,
        # input_shape=,
        input_shape=(2,),
        activation="relu"
    ))
    model.add(Dense(20, activation="relu"))
    model.add(Dense(env.action_space.n, activation="linear"))
    model.compile(loss="mse", optimizer=Adam(lr=0.001))
    model.summary()
    return model


# # Running DQN

# ## Experiment 001
#
# State: just where each host is
# Model: 3 dense layers
#
# ![zena](https://i.imgflip.com/2fw0fb.jpg)

# In[4]:


env = GemelEnv(interval=10, max_steps=500)
env.reset()

agent = DQNAgent(env, max_eps=1, period=5, state_mode=DQNAgent.StateModel.VN_ONLY, model=create_model_1(env))
hist = agent.train()

hist


# In[5]:


plt.plot([x['reward'] for x in hist[0]])


# ## Experiment 002

# smaller middle layer

# In[28]:


def create_model_2(env):
    model = Sequential()
    model.add(Dense(
        5,
        input_shape=(len(env._hosts_sorted_by_id),),
        activation="relu"
    ))
    model.add(Dense(env.action_space.n, activation="linear"))
    model.compile(loss="mse", optimizer=Adam(lr=0.001))
    model.summary()
    return model


# In[24]:


env = GemelEnv(interval=10, max_steps=500)
env.reset()

agent = DQNAgent(env, max_eps=1, period=5, state_mode=DQNAgent.StateModel.VN_ONLY, model=create_model_2(env))
hist = agent.train()

hist


# ## Experiment 003

# Is it about not having enough time? Let's find out.
#
# Forget about IDS feedback. instaed of letting it soak we would just get the fake reward and let it continue.

# In[33]:


env = GemelEnv(interval=10, max_steps=500)
env.reset()

agent = DQNAgent(env, max_eps=1, period=0, state_mode=DQNAgent.StateModel.VN_ONLY, model=create_model_2(env))
hist = agent.train()

hist


# In[34]:


plt.plot([x['reward'] for x in hist[0]])


# ## Experiment 004

# In[39]:


def create_model_4(env):
    model = Sequential()
    model.add(BatchNormalization(input_shape=(len(env._hosts_sorted_by_id),)))
    model.add(Dense(5, activation="relu"))
    model.add(Dense(5, activation="relu"))
    model.add(Dense(env.action_space.n, activation="linear"))
    model.compile(loss="mse", optimizer=Adam(lr=0.01))
    model.summary()
    return model


# In[42]:


env = GemelEnv(interval=10, max_steps=500)
env.reset()

agent = DQNAgent(env, max_eps=1, period=0, state_mode=DQNAgent.StateModel.VN_ONLY, model=create_model_3(env))
hist = agent.train()

hist


# In[43]:


plt.plot([x['reward'] for x in hist[0]])


# ## Experiment 005

# In[46]:


def create_model_5(env):
    model = Sequential()
#     model.add(Dense(
#         5,
#         input_shape=(len(env._hosts_sorted_by_id),),
#         activation="relu"
#     ))
    model.add(Dense(env.action_space.n, input_shape=(len(env._hosts_sorted_by_id),), activation="linear"))
    model.compile(loss="mse", optimizer=Adam(lr=0.01))
    model.summary()
    return model


# In[47]:


env = GemelEnv(interval=10, max_steps=500)
env.reset()

agent = DQNAgent(env, max_eps=1, period=0, state_mode=DQNAgent.StateModel.VN_ONLY, model=create_model_4(env))
hist = agent.train()

hist


# In[50]:


plt.plot([x['reward'] for x in hist[0]])


# ## Experiment 006
#
# EXP-005 + Batch Normalization

# In[58]:


def create_model_6(env):
    model = Sequential()
    model.add(BatchNormalization(input_shape=(len(env._hosts_sorted_by_id),)))
#     model.add(Dense(
#         5,
#         input_shape=(len(env._hosts_sorted_by_id),),
#         activation="relu"
#     ))
    model.add(Dense(env.action_space.n, activation="linear"))
    model.compile(loss="mse", optimizer=Adam(lr=0.01))
    model.summary()
    return model


# In[59]:


env = GemelEnv(interval=10, max_steps=200)
env.reset()

agent = DQNAgent(env, max_eps=1, period=0, state_mode=DQNAgent.StateModel.VN_ONLY, model=create_model_6(env))
hist = agent.train()

hist


# In[67]:


plt.plot([x['reward'] for x in hist[0]])


# ## Experiment 007

# Trying to fix the oscillations by tuning gamma

# In[68]:


def create_model_7(env):
    model = Sequential()
    model.add(BatchNormalization(input_shape=(len(env._hosts_sorted_by_id),)))

    model.add(Dense(env.action_space.n, activation="linear"))
    model.compile(loss="mse", optimizer=Adam(lr=0.01))
    model.summary()
    return model


# In[71]:


env = GemelEnv(interval=10, max_steps=200)
env.reset()

agent = DQNAgent(env, max_eps=1, period=0, state_mode=DQNAgent.StateModel.VN_ONLY, gamma=0.5, model=create_model_7(env))
hist = agent.train()

hist


# In[73]:


plt.plot([x['reward'] for x in hist[0]])


# ## Experiment 008

# In[85]:


env = GemelEnv(interval=10, max_steps=100)
env.reset()

agent = DQNAgent(env, max_eps=1, period=0, state_mode=DQNAgent.StateModel.VN_ONLY, gamma=0.1, model=create_model_7(env))
hist = agent.train()

hist


# We can see that it's a tat too slow in learning bad actions (see steps ~20)

# In[86]:


plt.plot([x['reward'] for x in hist[0]])


# # Experiment 009

# In[87]:


def create_model_9(env):
    model = Sequential()
    model.add(BatchNormalization(input_shape=(len(env._hosts_sorted_by_id),)))

    model.add(Dense(env.action_space.n, activation="linear"))
    model.compile(loss="mse", optimizer=Adam(lr=0.1))
    model.summary()
    return model


# In[90]:


env = GemelEnv(interval=10, max_steps=100)
env.reset()

agent = DQNAgent(env, max_eps=1, period=0, state_mode=DQNAgent.StateModel.VN_ONLY, gamma=0.8, model=create_model_9(env))
hist = agent.train()

hist


# In[91]:


plt.plot([x['reward'] for x in hist[0]])


# It seems like the single layer model does not have the capacity to learn toggles easily. it's always toggling between two states for solving such a simplistic set-up.
#
# Also, the "toggling" scheme seemed at first like a clever trick to contorl the action-space but it's wasting a lot of training time to be learned.

# ## Experiment 010

# In[10]:


def create_model_10(env):
    model = Sequential()
    # model.add(BatchNormalization(input_shape=(len(env._hosts_sorted_by_id),)))

    model.add(Dense(
        4,
        activation="relu",
        input_shape=(len(env._hosts_sorted_by_id),)
    ))

    model.add(Dense(
        env.action_space.n,
        activation="linear",
    ))

    model.compile(loss="mse", optimizer=Adam(lr=0.01))
    model.summary()

    return model


# In[12]:


env = GemelEnv(interval=10, max_steps=100)
env.reset()

agent = DQNAgent(env, max_eps=1, period=0, state_mode=DQNAgent.StateModel.VN_ONLY, gamma=0.8, model=create_model_10(env))
hist = agent.train()

hist


# In[13]:


plt.plot([x['reward'] for x in hist[0]])


# In[16]:


K.set_value(agent.model.optimizer.lr, 0.001)
hist = agent.train()


# In[17]:


plt.plot([x['reward'] for x in hist[0]])


# In[20]:


K.set_value(agent.model.optimizer.lr, 0.0001)
hist = agent.train()


# In[21]:


plt.plot([x['reward'] for x in hist[0]])


# In[25]:


agent.env.max_steps = 500
hist = agent.train()


# In[26]:


plt.plot([x['reward'] for x in hist[0]])


# The oscillations are ameliorated but still, the model seems clueless about what it is doing

# ## Experiment 11

# In[27]:


def create_model_11(env):
    model = Sequential()
    # model.add(BatchNormalization(input_shape=(len(env._hosts_sorted_by_id),)))

    model.add(Dense(
        4,
        activation="relu",
        input_shape=(len(env._hosts_sorted_by_id),)
    ))

    model.add(Dense(4, activation="relu"))

    model.add(Dense(
        env.action_space.n,
        activation="linear",
    ))
        model.compile(loss="mse", optimizer=Adam(lr=0.01))
    model.summary()

    return model


# In[28]:


env = GemelEnv(interval=10, max_steps=500)
env.reset()

agent = DQNAgent(env, max_eps=1, period=0, state_mode=DQNAgent.StateModel.VN_ONLY, gamma=0.8, model=create_model_11(env))
hist = agent.train()

hist


# In[29]:


plt.plot([x['reward'] for x in hist[0]])


# In[30]:


K.set_value(agent.model.optimizer.lr, 0.001)
hist = agent.train()
plt.plot([x['reward'] for x in hist[0]])


# In[39]:


ticks = [idx for idx, x in enumerate(hist[0]) if x["random"]]

for xc in ticks:
    plt.axvline(x=xc, color='y')

plt.plot([x['reward'] for x in hist[0]])


# Congrats! the model has learned the concept of "toggles".
#
# ### Why Toggles?
#
# A good approach would just have a more-security and a less-security button for each host, this is more in line with the multi (>2) VN approach and it wouldn't burden the model unnecessarily.
#
# Let's let the model run for a few more epochs at finer grain steps.

# In[40]:


K.set_value(agent.model.optimizer.lr, 0.0001)
hist = agent.train()


# In[41]:


ticks = [idx for idx, x in enumerate(hist[0]) if x["random"]]

for xc in ticks:
    plt.axvline(x=xc, color='y')

plt.plot([x['reward'] for x in hist[0]])


# ## Experiment 012

# In[56]:


def create_model_12(env):
    model = Sequential()
    print(f"Input shape={env.observation_shape()}\n\n")
    model.add(Dense(4, activation="relu", input_shape=env.observation_shape()))
    model.add(Dense(4, activation="relu"))
    model.add(Dense(env.action_space.n, activation="linear"))
    model.compile(loss="mse", optimizer=Adam(lr=0.01))
    model.summary()
    return model


# In[57]:


model=create_model_12(env)

env = GemelEnv(interval=10, max_steps=200)
env.reset()
env.observation_shape()

agent = DQNAgent(env, max_eps=1, period=5, state_mode=DQNAgent.StateModel.IDS, gamma=0.8, model=model)
hist = agent.train()

hist


# In[58]:


ticks = [idx for idx, x in enumerate(hist[0]) if x["random"]]
for xc in ticks: plt.axvline(x=xc, color='y')
plt.plot([x['reward'] for x in hist[0]])


# In[59]:


K.set_value(agent.model.optimizer.lr, 0.001)
agent.env.max_steps = 500
hist = agent.train()


# In[61]:


ticks = [idx for idx, x in enumerate(hist[0]) if x["random"]]
for xc in ticks: plt.axvline(x=xc, color='y')
plt.plot([x['reward'] for x in hist[0]])


# In[62]:


K.set_value(agent.model.optimizer.lr, 0.0001)
agent.env.max_steps = 500
hist = agent.train()


# In[63]:


ticks = [idx for idx, x in enumerate(hist[0]) if x["random"]]
for xc in ticks: plt.axvline(x=xc, color='y')
plt.plot([x['reward'] for x in hist[0]])


# Disappointing.

# ## Experiment 013

# Let's try the "Double Button" state model.

# In[5]:


def create_model_13(env):
    model = Sequential()
    print(f"Input shape={env.observation_shape()}\n\n")
    model.add(Dense(4, activation="relu", input_shape=env.observation_shape()))
    # model.add(Dense(4, activation="relu"))
    model.add(Dense(env.action_space.n, activation="linear"))
    model.compile(loss="mse", optimizer=Adam(lr=0.01))
    model.summary()
    return model


# In[8]:


env = GemelEnv(interval=10, max_steps=200, actions=GemelEnv.ActionSpace.DOUBLE_BUTTON)
env.reset()
env.observation_shape()

model=create_model_13(env)

agent = DQNAgent(env, max_eps=1, period=5, state_mode=DQNAgent.StateModel.IDS, gamma=0.8, model=model, epsilon_decay=0.9)
hist = agent.train()

hist


# In[9]:


ticks = [idx for idx, x in enumerate(hist[0]) if x["random"]]
for xc in ticks: plt.axvline(x=xc, color='y')
plt.plot([x['reward'] for x in hist[0]])


# In[10]:


env.max_setps = 50
agent.max_episodes = 6
agent.train()


# In[11]:


env.max_setps = 50
agent.max_episodes = 1
hist = agent.train()


# In[12]:


ticks = [idx for idx, x in enumerate(hist[0]) if x["random"]]
for xc in ticks: plt.axvline(x=xc, color='y')
plt.plot([x['reward'] for x in hist[0]])


# This definitely looks better

# In[22]:


model.epsilon_decay = 0.8
env.max_setps = 50
agent.max_episodes = 2
hist = agent.train()


# In[21]:


flat_hist = [x for h in hist for x in h]
ticks = [idx for idx, x in enumerate(flat_hist) if x["random"]]
for xc in ticks: plt.axvline(x=xc, color='y')
plt.plot([x['reward'] for x in flat_hist])


# In[23]:


model.epsilon_decay = 0.8
env.max_setps = 50
agent.max_episodes = 1
agent.epsilon = 0.01
hist = agent.train()


# <br/>

# In[24]:

print("Done.")

# In[ ]:





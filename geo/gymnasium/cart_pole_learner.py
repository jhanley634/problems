#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# Q-learner, from https://towardsdatascience.com/deep-q-learning-for-the-cartpole-44d761085c2f

from pathlib import Path
import random

from numpy.typing import NDArray
from tqdm import tqdm
import gymnasium as gym
import numpy as np

TEMP = Path("/tmp")
TABLE = TEMP / "q-table.npy"


def discretize_state(state: np.ndarray, bins: list) -> tuple:
    """Bin the continuous state into discrete state."""
    state_discretized = []
    for i, value in enumerate(state):
        state_discretized.append(np.digitize(value, bins[i]))
    return tuple(state_discretized)


def epsilon_greedy(
    state: tuple,
    env: int,
    q_table: NDArray[np.float64],
    epsilon: float,
) -> int:
    """Choose action using epsilon-greedy strategy."""
    if random.uniform(0, 1) < epsilon:
        return env.action_space.sample()  # Explore: random action

    # Exploit: choose action with highest Q-value
    return np.argmax(q_table[state])


def learn_a_balancing_policy(
    num_episodes: int = 5,
    alpha: float = 0.1,
    gamma: float = 0.99,
) -> None:
    env = gym.make("CartPole-v1", render_mode="human")

    # Discretize the state space
    bins = [
        np.linspace(-1, 1, 10),  # Position (Cart position)
        np.linspace(-1, 1, 10),  # Velocity (Cart velocity)
        np.linspace(-0.418, 0.418, 10),  # Angle (Pole angle)
        np.linspace(-3, 3, 10),  # Angular velocity (Pole velocity)
    ]

    if TABLE.exists():
        q_table = np.load(TABLE)
    else:
        # Initialize Q-table with all zeros (discretized state-action pairs)
        q_table = np.zeros(
            [len(bin_edges) + 1 for bin_edges in bins] + [env.action_space.n]
        )

    for _ in tqdm(range(num_episodes)):
        state, _info = env.reset()
        state = discretize_state(state, bins)
        epsilon = 0.1
        done = False

        while not done:
            action = epsilon_greedy(state, env, q_table, epsilon)
            epsilon *= 0.999
            next_state, reward, done, _, _ = env.step(action)
            next_state = discretize_state(next_state, bins)

            # Q-learning update rule
            next_max = np.max(q_table[next_state])  # Max Q-value for next state
            q_table[state][action] = q_table[state][action] + alpha * (
                reward + gamma * next_max - q_table[state][action]
            )

            state = next_state
            env.render()

        np.save(TABLE, q_table)

    env.close()


if __name__ == "__main__":
    learn_a_balancing_policy(1000)

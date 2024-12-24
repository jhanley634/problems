#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# Q-learner, from https://towardsdatascience.com/deep-q-learning-for-the-cartpole-44d761085c2f

from pathlib import Path
import random

from beartype import beartype
from gymnasium import Env
from gymnasium.spaces import Discrete
from numpy import float32, float64, int64
from numpy.typing import NDArray
from tqdm import tqdm
import gymnasium as gym
import numpy as np

TEMP = Path("/tmp")
TABLE = TEMP / "q-table.npy"


@beartype
def discretize_state(
    state: NDArray[float32],
    bins: tuple[
        NDArray[float64],
        NDArray[float64],
        NDArray[float64],
        NDArray[float64],
    ],
) -> NDArray[int64]:
    """Bin the continuous state into discrete state."""
    state_discretized = []
    for i, value in enumerate(state):
        state_discretized.append(np.digitize(value, bins[i]))
    return np.array(state_discretized, dtype=int64)


@beartype
def epsilon_greedy(
    state: NDArray[int64],
    env: Env[NDArray[float32], int],
    q_table: NDArray[float32],
    epsilon: float,
) -> int:
    """Choose action using epsilon-greedy strategy."""
    if random.uniform(0, 1) < epsilon:
        return int(env.action_space.sample())  # Explore: random action

    # Exploit: choose action with the highest Q-value
    return int(np.argmax(q_table[tuple(state)]))


@beartype
def learn_a_balancing_policy(
    num_episodes: int = 5,
    alpha: float = 0.1,
    gamma: float = 0.99,
) -> None:
    env = gym.make("CartPole-v1", render_mode="human")

    # Discretize the state space
    bins = (
        np.linspace(-1.0, 1.0, 10),  # Position (Cart position)
        np.linspace(-1.0, 1.0, 10),  # Velocity (Cart velocity)
        np.linspace(-0.418, 0.418, 10),  # Angle (Pole angle)
        np.linspace(-3.0, 3.0, 10),  # Angular velocity (Pole velocity)
    )

    if TABLE.exists():
        q_table = np.load(TABLE)
    else:
        # Initialize Q-table with all zeros (discretized state-action pairs)
        assert isinstance(env.action_space, Discrete)
        q_table = np.zeros(
            [len(bin_edges) + 1 for bin_edges in bins] + [env.action_space.n],
            dtype=float32,
        )

    epsilon = 0.2
    progress = tqdm(range(num_episodes), desc="training progress")

    for episode in progress:
        state, info = env.reset()
        state = np.array(discretize_state(state, bins), dtype=np.int64)
        cum_reward = max_reward = 0
        epsilon *= 0.99
        done = False

        while not done:
            action = epsilon_greedy(state, env, q_table, epsilon)
            epsilon *= 0.99
            next_state, reward, done, _, _ = env.step(action)
            next_state = discretize_state(next_state, bins)
            cum_reward += reward

            # Q-learning update rule
            next_max = float(
                np.max(q_table[tuple(next_state)])
            )
            q_table[state][action] = q_table[state][action] + alpha * (
                float(reward) + gamma * next_max - q_table[state][action]
            )

            state = next_state

        if max_reward < cum_reward:
            max_reward = cum_reward
            progress.set_postfix(
                cum_reward=f"{cum_reward:.0f}", epsilon=f"{epsilon:.4f}"
            )
            np.save(TABLE, q_table)
            env.render()

    env.close()


if __name__ == "__main__":
    learn_a_balancing_policy(1000)

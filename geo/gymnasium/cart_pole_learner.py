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
def _discretize_state(
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
def _epsilon_greedy(
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

    @beartype
    def get_q_table(env: Env[NDArray[float32], int]) -> NDArray[float32]:
        if TABLE.exists():
            return np.array(np.load(TABLE), dtype=float32)

        # Initialize Q-table with all zeros (discretized state-action pairs)
        assert isinstance(env.action_space, Discrete)
        return np.zeros(
            [len(bin_edges) + 1 for bin_edges in bins] + [env.action_space.n],
            dtype=float32,
        )

    render_mode = "rgb_array" if num_episodes > 1000 else "human"
    env = gym.make("CartPole-v1", render_mode=render_mode)

    # Discretize the state space
    num_bins = 10
    bins = (
        np.linspace(-1.0, 1.0, num_bins).astype(np.float64),  # cart position
        np.linspace(-1.0, 1.0, num_bins).astype(np.float64),  # cart velocity
        np.linspace(-0.418, 0.418, num_bins).astype(np.float64),  #  pole angle
        np.linspace(-3.0, 3.0, num_bins).astype(np.float64),  # angular pole velocity
    )

    max_reward = 0
    epsilon = 0.1
    q_table = get_q_table(env)
    progress = tqdm(range(num_episodes), desc="training progress")

    for episode in progress:
        state, _info = env.reset()
        state = np.array(_discretize_state(state, bins), dtype=np.int64)
        cum_reward = 0
        done = False

        while not done:
            action = _epsilon_greedy(state, env, q_table, epsilon)
            next_state, reward, done, _, _ = env.step(action)
            next_state = _discretize_state(next_state, bins)
            cum_reward += int(float(reward))

            # Q-learning update rule
            next_max = float(np.max(q_table[tuple(next_state)]))
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
        if episode % 1000 == 0:
            progress.set_postfix(
                cum_reward=f"{cum_reward:.0f}", epsilon=f"{epsilon:.4f}"
            )
            np.save(TABLE, q_table)
    env.close()  # type: ignore [no-untyped-call]


if __name__ == "__main__":
    learn_a_balancing_policy(1_000)

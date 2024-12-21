#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

from time import sleep

import gymnasium as gym
import numpy as np


def main(num_episodes: int = 5) -> None:
    env = gym.make("CartPole-v1", render_mode="human")  # or render_mode="rgb_array"

    for _ in range(num_episodes):

        env.reset(options={"low": -0.1, "high": 0.1})
        term = False
        while not term:
            env.render()
            obs, reward, term, _trunc, _info = env.step(env.action_space.sample())
            print(reward, np.array(obs))

        sleep(1.0)

    env.close()


if __name__ == "__main__":
    main()

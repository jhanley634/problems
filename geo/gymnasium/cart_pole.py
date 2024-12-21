#! /usr/bin/env python

import gymnasium as gym
import numpy as np


def main() -> None:
    env = gym.make("CartPole-v1", render_mode="human")  # or render_mode="rgb_array"
    env.reset(seed=42, options={"low": -0.1, "high": 0.1})
    term = False

    while not term:
        env.render()
        obs, reward, term, _trunc, _info = env.step(env.action_space.sample())
        print(reward, np.array(obs))

    env.reset()
    env.close()


if __name__ == "__main__":
    main()

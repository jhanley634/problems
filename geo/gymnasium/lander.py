#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
import gymnasium as gym


def lander() -> None:
    env = gym.make("LunarLander-v2", render_mode="human")
    _observation, info = env.reset(seed=42)
    for _ in range(1000):
        action = env.action_space.sample()  # this is where you would insert your policy
        _observation, _reward, terminated, truncated, info = env.step(action)

        if terminated or truncated:
            _observation, _info = env.reset()

    env.close()


if __name__ == "__main__":
    lander()

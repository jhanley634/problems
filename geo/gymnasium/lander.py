#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
import gymnasium as gym


def lander() -> None:
    with gym.make("LunarLander-v2", render_mode="human") as env:
        _observation, _info = env.reset(seed=42)
        for _ in range(1000):
            action = (
                env.action_space.sample()
            )  # this is where you would insert your policy
            _observation, _reward, terminated, truncated, _info = env.step(action)

            if terminated or truncated:
                _observation, _info = env.reset()


if __name__ == "__main__":
    lander()

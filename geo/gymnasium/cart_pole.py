#! /usr/bin/env python

from tqdm import tqdm
import gymnasium as gym


def main() -> None:
    env = gym.make("CartPole-v1", render_mode="rgb_array")
    env.reset(seed=42, options={"low": -0.1, "high": 0.1})
    print(env)
    for _ in tqdm(range(1000)):
        env.render()
        env.step(env.action_space.sample())
    env.close()


if __name__ == "__main__":
    main()

#! /usr/bin/env python
"""
A jogger is heading north on a highway.
To the east and west there are corn fields,
where a uniform distribution of dozens of zombies are just waking up.
When they notice the jogger they first head toward the highway,
and then make a 90-degree turn to head north, pursuing the jogger.
"""
from dataclasses import dataclass
import math
import random

import pygame


@dataclass
class Agent:
    """An Agent is capable of motion, and can be rendered on-screen."""

    x: float
    y: float
    speed: float
    color: tuple[int, int, int]
    size: int

    @property
    def position(self) -> tuple[float, float]:
        return self.x, self.y


class Jogger(Agent):
    pass


class Zombie(Agent):
    pass


WIDTH, HEIGHT = 800, 600
JOGGER_SIZE = 10
ZOMBIE_SIZE = 8
ZOMBIE_COUNT = 30
SPEED = 2
ZOMBIE_SPEED = 1


class ZombieRunnerBoard:

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Jogger vs Zombies Simulation")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        green = (0, 255, 0)
        self.jogger = Jogger(WIDTH // 2, HEIGHT // 2, SPEED, green, JOGGER_SIZE)
        self.zombies = self.init_zombies()

    def init_zombies(self) -> list[Zombie]:
        zombies = []
        for _ in range(ZOMBIE_COUNT):
            # Randomly place zombies in corn fields (either left or right of the highway)
            x = random.choice(
                [
                    random.randint(0, WIDTH // 2 - 50),
                    random.randint(WIDTH // 2 + 50, WIDTH),
                ]
            )
            y = random.randint(0, HEIGHT)
            red = (255, 0, 0)
            zombies.append(Zombie(x, y, ZOMBIE_SPEED, red, ZOMBIE_SIZE))
        return zombies

    def move_zombies(self) -> None:
        for zombie in self.zombies:
            speed = ZOMBIE_SPEED * random.uniform(0.8, 1.0)
            # Move zombie towards the jogger's x position, then head north
            direction = int(math.copysign(1, self.jogger.x - zombie.x))
            zombie.x += direction * speed

            # Zombie moves north along the highway towards the jogger
            if zombie.x == self.jogger.x:
                zombie.y -= speed

    def draw(self) -> None:
        black = (0, 0, 0)
        self.screen.fill(black)  # clear screen

        jogger = self.jogger
        pygame.draw.circle(self.screen, jogger.color, jogger.position, jogger.size)

        for zombie in self.zombies:
            pygame.draw.circle(self.screen, zombie.color, zombie.position, zombie.size)

        pygame.display.flip()


def main() -> None:
    game = ZombieRunnerBoard()
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move jogger north
        game.jogger.y -= SPEED
        if game.jogger.y < 0:  # Reset jogger position if it goes off-screen
            game.jogger.y = HEIGHT

        game.move_zombies()
        game.draw()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()

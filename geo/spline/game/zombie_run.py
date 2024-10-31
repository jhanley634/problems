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
    x: float
    y: float
    speed: float
    color: tuple[int, int, int]
    size: int


class Jogger(Agent):
    pass


class Zombie(Agent):
    pass


# Constants
WIDTH, HEIGHT = 800, 600
JOGGER_SIZE = 10
ZOMBIE_SIZE = 8
ZOMBIE_COUNT = 30
SPEED = 2
ZOMBIE_SPEED = 1

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogger vs Zombies Simulation")
clock = pygame.time.Clock()

# Jogger starting position
jogger = Jogger(WIDTH // 2, HEIGHT // 2, SPEED, (0, 255, 0), JOGGER_SIZE)  # green

# Initialize zombies
zombies = []
for _ in range(ZOMBIE_COUNT):
    # Randomly place zombies in corn fields (either left or right of the highway)
    x_pos = random.choice(
        [random.randint(0, WIDTH // 2 - 50), random.randint(WIDTH // 2 + 50, WIDTH)]
    )
    y_pos = random.randint(0, HEIGHT)
    zombies.append(Zombie(x_pos, y_pos, ZOMBIE_SPEED, (255, 0, 0), ZOMBIE_SIZE))  # red

def move_zombies() -> None:
    for zombie in zombies:
        # Move zombie towards the jogger's x position, then head north
        direction = int(math.copysign(1, jogger.x - zombie.x))
        zombie.x += direction * ZOMBIE_SPEED

        # Zombie moves north along the highway towards the jogger
        if zombie.x == jogger.x:
            zombie.y -= ZOMBIE_SPEED


def draw() -> None:
    screen.fill((0, 0, 0))  # Clear screen with black
    pygame.draw.circle(screen, jogger.color, (jogger.x, jogger.y), jogger.size)

    for zombie in zombies:
        pygame.draw.circle(screen, zombie.color, (zombie.x, zombie.y), zombie.size)

    pygame.display.flip()


def main() -> None:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move jogger north
        jogger.y -= SPEED
        if jogger.y < 0:  # Reset jogger position if it goes off screen
            jogger.y = HEIGHT

        move_zombies()
        draw()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()

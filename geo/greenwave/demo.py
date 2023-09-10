#! /usr/bin/env python
from time import time

from pygame import Rect, Surface, Vector2
import pygame

GRID_SIZE_PX: int = 3


class City:
    """Terrain that cars drive through.

    Comprised of WIDTH x HEIGHT city blocks,
    with 4-way traffic signals.
    Traffic flows seemlessly into neighboring cities,
    which appear to be infinite sinks or sources.
    """

    BLOCK_SIZE: int = 50  # number of grids per (square) block

    def __init__(self, width: int = 4, height: int = 3):
        scale = self.BLOCK_SIZE * GRID_SIZE_PX
        self.blocks = [
            Block(150 + scale * i, 100 + scale * j)
            for i in range(width)
            for j in range(height)
        ]


class Block:
    """A city block."""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


def main():
    city = City(1, 1)
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    player_pos = Vector2(screen.get_width() / 2, screen.get_height() / 2)

    while running:
        for event in pygame.event.get():
            match event.type:
                case (pygame.QUIT | pygame.KEYDOWN):
                    if event.type == pygame.KEYDOWN and event.key != pygame.K_q:
                        continue
                    running = False

        screen.fill("grey")
        draw(city, screen)
        pygame.draw.circle(screen, "red", player_pos, 40)

        pygame.display.flip()
        dt = clock.tick(60) / 1e3  # FPS
        if not (0.016 <= dt < 0.020):
            print(dt, "\t", time())

    pygame.quit()


def draw(city: City, screen: Surface):
    size = city.BLOCK_SIZE * GRID_SIZE_PX - GRID_SIZE_PX
    for block in city.blocks:
        pygame.draw.rect(screen, "white", Rect((block.x, block.y), (size, size)))


if __name__ == "__main__":
    main()

#! /usr/bin/env PYGAME_HIDE_SUPPORT_PROMPT=1 python
from time import time
from typing import Tuple

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

    def __init__(self, width: int, height: int):
        scale = self.BLOCK_SIZE * GRID_SIZE_PX
        self.blocks = [
            Block(
                150 + scale * i + GRID_SIZE_PX,
                100 + scale * j,
                self.BLOCK_SIZE * GRID_SIZE_PX - 3 * GRID_SIZE_PX,
            )
            for i in range(width)
            for j in range(height)
        ]


class Block:
    """A city block."""

    def __init__(self, x: int, y: int, size: int):
        self.x = x
        self.y = y
        self.size = size
        self.roads = [Road((x, y), (x + size, y))]

    def render(self, screen):
        rect = Rect((self.x, self.y), (self.size, self.size))
        pygame.draw.rect(screen, "white", rect)
        for road in self.roads:
            road.render(screen)


class Road:
    """A one-lane roadway, a directed edge in a graph."""

    def __init__(self, start: Tuple[int, int], end: Tuple[int, int]):
        self.start = Vector2(*start)
        self.end = Vector2(*end)

    def render(self, screen):
        pygame.draw.line(screen, "black", self.start, self.end, GRID_SIZE_PX)


class GreenWave:
    def __init__(self, city_size=(2, 1)) -> None:
        self.city: City = City(*city_size)
        self.running: bool = True

    def main_loop(self, window_size=(1280, 720)) -> None:
        pygame.init()
        self.screen: Surface = pygame.display.set_mode(window_size)
        clock = pygame.time.Clock()

        player_pos = Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)

        while self.running:
            self.handle_events()

            self.screen.fill("grey")
            self.render()
            pygame.draw.circle(self.screen, "red", player_pos, 40)
            self.flipit()

            dt = clock.tick(60) / 1e3  # FPS
            if not (0.016 <= dt < 0.020):
                print(dt, "\t", time())

        pygame.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            match event.type:
                case (pygame.QUIT | pygame.KEYDOWN):
                    if event.type == pygame.KEYDOWN and event.key != pygame.K_q:
                        continue
                    self.running = False

    def render(self) -> None:
        for block in self.city.blocks:
            block.render(self.screen)

    def flipit(self) -> None:
        """Put the origin at lower left, as Descartes intended."""
        s: Surface = pygame.transform.flip(self.screen, flip_x=False, flip_y=True)
        self.screen.blit(s, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    GreenWave().main_loop()

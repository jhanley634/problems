#! /usr/bin/env PYGAME_HIDE_SUPPORT_PROMPT=1 python
from enum import Enum, auto
from operator import attrgetter
from time import time
from typing import Tuple

from pygame import Rect, Surface, Vector2
from sortedcontainers import SortedKeyList
import pygame

GRID_SIZE_PX: int = 3

# seconds, how long we run during an interactive edit / compile / run cycle
DURATION = 4.0


class City:
    """Terrain that cars drive through.

    Comprised of WIDTH x HEIGHT city blocks,
    with 4-way traffic signals.
    Traffic flows seamlessly into neighboring cities,
    which appear to be infinite sinks or sources.
    """

    BLOCK_SIZE: float = 50.0  # number of grids per (square) block

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
        western_road_segment = self.blocks[0].road_segments[0]
        western_road_segment.obstacles.add(
            Car(western_road_segment, self.BLOCK_SIZE * GRID_SIZE_PX / DURATION)
        )

    @property
    def cars(self):
        for block in self.blocks:
            for segment in block.road_segments:
                for item in segment.obstacles:
                    if isinstance(item, Car):
                        yield item


class Block:
    """A city block."""

    def __init__(self, x: float, y: float, size: float):
        self.x = x
        self.y = y
        self.size = size
        self.road_segments = [RoadSegment((x, y), (x + size, y))]

    def render(self, screen):
        rect = Rect((self.x, self.y), (self.size, self.size))
        pygame.draw.rect(screen, "white", rect)
        for segment in self.road_segments:
            segment.render(screen)


class RoadSegment:
    """Segment of a one-lane roadway, a directed edge in a graph.

    A long "road" may consist of several linked segments.
    """

    def __init__(self, start: Tuple[float, float], end: Tuple[float, float]) -> None:
        self.start = Vector2(*start)
        self.end = Vector2(*end)
        self.length = self.start.distance_to(self.end)
        self.control = Control(self.length)

        # One cannot drive through certain obstacles.
        self.obstacles = SortedKeyList(key=attrgetter("position"))

    def render(self, screen) -> None:
        pygame.draw.line(screen, "black", self.start, self.end, GRID_SIZE_PX)


class Control:
    """A traffic control, or signal light, at an intersection.

    It faces just one way and controls exactly one lane of traffic."""

    class Color(Enum):
        RED = auto()
        GREEN = auto()

    def __init__(self, position: float) -> None:
        self.position = position  # distance from start, in px
        self.color = self.Color.GREEN


class Car:
    """A vehicle on a road segment."""

    def __init__(self, road_segment: RoadSegment, speed_px_per_sec: float) -> None:
        self.road_segment = road_segment
        self.position: float = 0.0  # distance from start, in px
        self.velocity: float = speed_px_per_sec

    def update(self, dt: float) -> None:
        seg = self.road_segment
        assert seg.start.y == seg.end.y  # horizontal
        next_obstacle = seg.obstacles.bisect_key(self.position)

        self.position += self.velocity * dt

        print(f"{self.position:6f}  {self.velocity}  {next_obstacle}  {seg.obstacles}")

    def render(self, screen: Surface) -> None:
        start = self.road_segment.start
        pos = Vector2(start.x + self.position, start.y)
        pygame.draw.circle(screen, "red", pos, 2 * GRID_SIZE_PX)


class GreenWave:
    def __init__(self, city_size=(2, 1)) -> None:
        self.city: City = City(*city_size)
        self.running: bool = True

    def main_loop(self, window_size=(1280, 720)) -> None:
        pygame.init()
        self.screen: Surface = pygame.display.set_mode(window_size)
        clock = pygame.time.Clock()

        # while self.running:
        FPS = 60
        NUM_FRAMES = int(DURATION * FPS)
        for _ in range(NUM_FRAMES):
            dt = clock.tick(FPS) / 1e3
            if dt > 0.022:
                print(dt, "\t", time())
            self.handle_events()

            self.screen.fill("grey")
            self.render(dt)
            self.flip_it()

        pygame.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            match event.type:
                case (pygame.QUIT | pygame.KEYDOWN):
                    if event.type == pygame.KEYDOWN and event.key != pygame.K_q:
                        continue
                    self.running = False

    def render(self, dt: float) -> None:
        for block in self.city.blocks:
            block.render(self.screen)
        for car in self.city.cars:
            car.update(dt)
            car.render(self.screen)

    def flip_it(self) -> None:
        """Put the origin at lower left, as Descartes intended."""
        s: Surface = pygame.transform.flip(self.screen, flip_x=False, flip_y=True)
        self.screen.blit(s, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    GreenWave().main_loop()

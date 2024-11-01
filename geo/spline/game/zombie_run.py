#! /usr/bin/env PYGAME_HIDE_SUPPORT_PROMPT=1 python
"""
A jogger is heading north on a highway.
To the east and west there are corn fields,
where a uniform distribution of dozens of zombies are just waking up.
When they notice the jogger they first head toward the highway,
and then make a 90-degree turn to head north, pursuing the jogger.
"""
from dataclasses import dataclass
from functools import partial
import math
import random

from pygame import Rect
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

    def __lt__(self, other: object) -> bool:
        assert isinstance(other, Zombie), other
        return self.position < other.position

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, Zombie), other
        return self.position == other.position


WIDTH, HEIGHT = 800, 600
LANE_WIDTH = 40  # it's a two lane highway
JOGGER_SIZE = 10
ZOMBIE_SIZE = 8
ZOMBIE_COUNT = 500
SPEED = 2
ZOMBIE_SPEED = 1
SEPARATION_DISTANCE = 4 * ZOMBIE_SIZE  # minimum distance between zombies
TARGET_FRAME_RATE = 60  #   frames per second
ACCEPTABLE_FRAME_RATE = 20  # visually this is barely acceptably smooth
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
TWILIGHT_LAVENDER = (230, 230, 250)


class ZombieRunnerSim:

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Jogger vs Zombies Simulation")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.fps = 0.0
        green = (0, 255, 0)
        self.jogger = Jogger(WIDTH // 2, HEIGHT // 2, SPEED, green, JOGGER_SIZE)
        self.zombies = self.init_zombies()

        z_ids = list(self.zombies.keys())
        random.shuffle(z_ids)
        z_ids = z_ids[: len(self.zombies) // 2]
        # from zombie ID to IDs of its nearby neighbors (initially all are "near")
        self.nbrs = {z_id: set(z_ids) for z_id in self.zombies}
        for z_id in z_ids:
            self.nbrs[z_id].remove(z_id)

    def init_zombies(self) -> dict[int, Zombie]:
        zombies = {}
        for i in range(ZOMBIE_COUNT):
            # Randomly place zombies in corn fields (either left or right of the highway)
            x = random.choice(
                [
                    random.randint(0, WIDTH // 2 - 50),
                    random.randint(WIDTH // 2 + 50, WIDTH),
                ]
            )
            y = random.randint(0, HEIGHT)
            speed = ZOMBIE_SPEED * random.uniform(0.3, 1.0)
            red = (255, 0, 0)
            zombies[i] = Zombie(x, y, speed, red, ZOMBIE_SIZE)

        return zombies

    def move_zombies(self) -> None:
        culls = []

        for z_id, zombie in self.zombies.items():
            # Move zombie towards the jogger's x position, then head north
            direction = int(math.copysign(1, self.jogger.x - zombie.x))
            zombie.x += direction * zombie.speed
            # Half the population leans left, half right, to avoid single-file.
            yaw = math.copysign(1.0, z_id % 2 - 0.5)  # +/- 1, so Right or Left
            zombie.x += 0.19 * yaw * zombie.speed

            # Zombie moves north along the highway towards the jogger
            if abs(zombie.x - self.jogger.x) < LANE_WIDTH:
                zombie.y -= zombie.speed
            if zombie.y < 0:
                culls.append(z_id)

            self._apply_repulsive_force_field(z_id)

        # Remove zombies that have gone off-screen
        for z_id in culls:
            del self.zombies[z_id]

    def _update_neighbors(self, z_id: int) -> None:

        self._add_random_neighbors(z_id)

        zombie = self.zombies[z_id]

        for other_id in list(self.nbrs[z_id]):
            assert other_id != z_id
            if other_id not in self.zombies:
                self.nbrs[z_id].discard(other_id)
                continue
            other = self.zombies[other_id]
            if self.distance(zombie, other) > 4 * SEPARATION_DISTANCE:
                self.nbrs[z_id].discard(other_id)

    # ruff: noqa: B006
    def _add_random_neighbors(
        self,
        z_id: int,
        count: int = 40,
        permuted_ids: list[int] = [],
    ) -> None:
        """Adds `count` neighbors to a given zombie, completely at random.

        This helper promises to complete in O(1) constant time.
        Sometimes we get lucky, we choose another zombie that truly
        is nearby, and it sticks around for a while.
        """
        if not permuted_ids:
            permuted_ids[:] = list(self.zombies.keys())  # persistent across calls
            random.shuffle(permuted_ids)

        if self.fps < ACCEPTABLE_FRAME_RATE:
            count //= 10  # speed things up until we're working on an easier problem

        zombie = self.zombies[z_id]

        for _ in range(min(count, 1 + len(permuted_ids) // 2)):
            if permuted_ids:
                other_id = permuted_ids.pop()
                if self.near(zombie, other_id):
                    self.nbrs[z_id].add(other_id)
                    self.nbrs[other_id].add(z_id)

    def near(self, zombie: Zombie, other_id: int, epsilon: float = 1e-9) -> bool:
        other = self.zombies.get(other_id)
        if other is None:
            return False
        return epsilon < self.distance(zombie, other) < SEPARATION_DISTANCE

    def _apply_repulsive_force_field(self, z_id: int) -> None:

        if random.uniform(0, 1) < 0.03:
            self._update_neighbors(z_id)
        zombie = self.zombies[z_id]

        near = partial(self.near, zombie)
        nearby_zombies = [self.zombies[z_id] for z_id in filter(near, self.nbrs[z_id])]

        if nearby_zombies:

            # occasional random perturbation
            if random.uniform(0, 1) < 0.02:
                kick = 3.0 * zombie.speed
                zombie.x += random.uniform(-kick, kick)

            repulsive_force_x = 0.0
            repulsive_force_y = 0.0

            # Calculate sum of repulsive forces from nearby zombies
            for other in nearby_zombies:
                distance = self.distance(zombie, other)
                if 0 < distance < SEPARATION_DISTANCE:
                    # Calculate the repulsion vector
                    dx = zombie.x - other.x
                    dy = zombie.y - other.y
                    sep_dist = SEPARATION_DISTANCE
                    repulsion_strength = (sep_dist - distance) / sep_dist
                    repulsive_force_x += (dx / distance) * repulsion_strength * 3.0
                    repulsive_force_y += (dy / distance) * repulsion_strength * 3.0

            # Update zombie's position by applying cohesion and repulsive forces
            # print(zombie.speed, "\t", repulsive_force_x)
            zombie.x += repulsive_force_x
            zombie.y += repulsive_force_y

    @staticmethod
    def distance(a: Agent, b: Agent) -> float:
        return math.hypot(a.x - b.x, a.y - b.y)

    def draw(self, fps: dict[str, float] = {"prev": 0.0}) -> None:
        acceptable = ACCEPTABLE_FRAME_RATE
        got_faster = fps["prev"] < acceptable and self.fps >= acceptable
        bg_color = TWILIGHT_LAVENDER if got_faster else BLACK  # flash at transition
        self.screen.fill(bg_color)  # clear screen

        jogger = self.jogger
        pygame.draw.circle(self.screen, jogger.color, jogger.position, jogger.size)

        for zombie in self.zombies.values():
            pygame.draw.circle(self.screen, zombie.color, zombie.position, zombie.size)

        bar_height = 10
        scale_factor = 5
        population_indicator = Rect(
            2 * WIDTH // 3, len(self.zombies), WIDTH // 3, bar_height
        )
        pygame.draw.rect(self.screen, TWILIGHT_LAVENDER, population_indicator)

        speed_indicator = Rect(
            0, scale_factor * (TARGET_FRAME_RATE - self.fps), WIDTH // 3, bar_height
        )
        pygame.draw.rect(self.screen, PURPLE, speed_indicator)
        fps["prev"] = self.fps  # persistent across calls

        pygame.display.flip()


def main() -> None:
    game = ZombieRunnerSim()
    clock = pygame.time.Clock()

    running = True
    while running and len(game.zombies) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move jogger north
        game.jogger.y -= SPEED
        if game.jogger.y < 0:  # Reset jogger position if it goes off-screen
            game.jogger.y = HEIGHT

        game.move_zombies()
        game.draw()

        # Even without flushing, we'll see plenty of updates.
        game.fps = clock.get_fps()
        print(f"\r{game.fps:4.1f} fps    {len(game.zombies)} zombies   ", end="")
        clock.tick(TARGET_FRAME_RATE)

    pygame.quit()
    print()


if __name__ == "__main__":
    main()

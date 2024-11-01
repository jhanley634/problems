#! /usr/bin/env PYGAME_HIDE_SUPPORT_PROMPT=1 python
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
        for z_id, zombie in self.zombies.items():
            # Move zombie towards the jogger's x position, then head north
            direction = int(math.copysign(1, self.jogger.x - zombie.x))
            zombie.x += direction * zombie.speed

            # Zombie moves north along the highway towards the jogger
            if abs(zombie.x - self.jogger.x) < LANE_WIDTH:
                zombie.y -= zombie.speed

            # Boids behavior: Cohesion and Separation
            self._flock_like_boids(z_id)

        # Remove zombies that have gone off-screen
        for z_id, zombie in list(self.zombies.items()):
            if zombie.y < 0:
                del self.zombies[z_id]

    def _update_neighbors(self, z_id: int) -> None:

        zombie = self.zombies[z_id]

        self._add_random_neighbors(z_id)

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
        Distant ones will be immediately pruned, so no harm done.
        """
        if not permuted_ids:
            permuted_ids[:] = list(self.zombies.keys())  # persistent across calls
            random.shuffle(permuted_ids)

        acceptable_frame_rate = 20  # visually this is barely acceptably smooth
        if self.fps < acceptable_frame_rate:
            count //= 10  # speed things up until we're working on an easier problem

        for _ in range(min(count, len(permuted_ids) // 2)):
            if permuted_ids:
                other_id = permuted_ids.pop()
                if other_id in self.zombies and other_id != z_id:
                    self.nbrs[z_id].add(other_id)

    def _flock_like_boids(self, z_id: int) -> None:

        if random.uniform(0, 1) < 0.01:
            self._update_neighbors(z_id)
        zombie = self.zombies[z_id]

        def near(other_id: int, epsilon: float = 1e-9) -> bool:
            other = self.zombies.get(other_id)
            if other is None:
                return False
            return epsilon < self.distance(zombie, other) < SEPARATION_DISTANCE

        nearby_zombies = [self.zombies[z_id] for z_id in filter(near, self.nbrs[z_id])]

        if nearby_zombies:
            # Cohesion: Calculate the average position of nearby zombies
            avg_x = sum(z.x for z in nearby_zombies) / len(nearby_zombies)
            avg_y = sum(z.y for z in nearby_zombies) / len(nearby_zombies)

            # Move towards the average position (cohesion)
            zombie.x += (avg_x - zombie.x) * 0.05  # Adjust the factor for smoothness
            zombie.y += (avg_y - zombie.y) * 0.05

            # Separation: Move away from nearby zombies
            for other in nearby_zombies:
                distance = self.distance(zombie, other)
                if distance < SEPARATION_DISTANCE:
                    # Calculate a separation vector
                    dx = zombie.x - other.x
                    dy = zombie.y - other.y
                    norm = math.hypot(dx, dy)
                    if norm > 0:
                        # Push away.
                        zombie.x += (dx / norm) * (SEPARATION_DISTANCE - distance) * 0.1
                        zombie.y += (dy / norm) * (SEPARATION_DISTANCE - distance) * 0.1

    @staticmethod
    def distance(a: Agent, b: Agent) -> float:
        return math.hypot(a.x - b.x, a.y - b.y)

    def draw(self) -> None:
        black = (0, 0, 0)
        self.screen.fill(black)  # clear screen

        jogger = self.jogger
        pygame.draw.circle(self.screen, jogger.color, jogger.position, jogger.size)

        for zombie in self.zombies.values():
            pygame.draw.circle(self.screen, zombie.color, zombie.position, zombie.size)

        purple = (128, 0, 128)
        scale_factor = 5
        speed_indicator = Rect(0, scale_factor * (60 - self.fps), WIDTH // 3, 10)
        pygame.draw.rect(self.screen, purple, speed_indicator)

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
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()

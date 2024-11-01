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
    id_: int

    # ruff: noqa: PLR0913
    def __init__(
        self,
        x: float,
        y: float,
        speed: float,
        color: tuple[int, int, int],
        size: int,
        id_: int,
    ) -> None:
        super().__init__(x, y, speed, color, size)
        self.id_ = id_

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
ZOMBIE_COUNT = 200
SPEED = 2
ZOMBIE_SPEED = 1
SEPARATION_DISTANCE = 4 * ZOMBIE_SIZE  # minimum distance between zombies


class ZombieRunnerSim:

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Jogger vs Zombies Simulation")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        green = (0, 255, 0)
        self.jogger = Jogger(WIDTH // 2, HEIGHT // 2, SPEED, green, JOGGER_SIZE)
        self.zombies = self.init_zombies()
        self.nbrs: dict[int, set[Zombie]] = {}

    def init_zombies(self) -> list[Zombie]:
        zombies = []
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
            zombies.append(Zombie(x, y, speed, red, ZOMBIE_SIZE, i))

        return zombies

    def move_zombies(self) -> None:
        for zombie in self.zombies:
            # Move zombie towards the jogger's x position, then head north
            direction = int(math.copysign(1, self.jogger.x - zombie.x))
            zombie.x += direction * zombie.speed

            # Zombie moves north along the highway towards the jogger
            if abs(zombie.x - self.jogger.x) < LANE_WIDTH:
                zombie.y -= zombie.speed

            # Boids behavior: Cohesion and Separation
            self.flock_like_boids(zombie)

        # Remove zombies that have gone off-screen
        self.zombies = [z for z in self.zombies if z.y >= 0]

    def _update_quadtree(self, zombie: Zombie) -> None:
        pass

    def flock_like_boids(self, zombie: Zombie) -> None:
        def near(other: Zombie, epsilon: float = 1e-9) -> bool:
            return epsilon < self.distance(zombie, other) < SEPARATION_DISTANCE

        nearby_zombies = sorted(filter(near, self.zombies))

        if random.uniform(0, 1) < 0.01:
            self._update_quadtree(zombie)
        # p1 = FPoint(zombie.x - SEPARATION_DISTANCE, zombie.y - SEPARATION_DISTANCE)
        # p2 = FPoint(zombie.x + SEPARATION_DISTANCE, zombie.y + SEPARATION_DISTANCE)
        # nearby_zombies = self.qt.query(Rectangle(p1, p2))
        # nearby_zombies.remove(Point(*zombie.position))
        # nearby_zombies = list(filter(near, nearby_zombies))
        # assert sorted(map(attrgetter("zombie"), nearby_zombies)) == nearby_zombies1

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

        for zombie in self.zombies:
            pygame.draw.circle(self.screen, zombie.color, zombie.position, zombie.size)

        pygame.display.flip()


def main() -> None:
    game = ZombieRunnerSim()
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

        # Even without flushing, we'll see plenty of updates.
        print(f"\r{clock.get_fps():4.1f} fps    {len(game.zombies)} zombies   ", end="")
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()

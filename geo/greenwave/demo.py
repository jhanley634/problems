#! /usr/bin/env python

import pygame


class City:
    """Terrain that cars drive through.

    Comprised of WIDTH x HEIGHT city blocks,
    with 4-way traffic signals.
    Traffic flows seemlessly into neighboring cities,
    which appear to be infinite sinks or sources.
    """

    WIDTH: int = 4
    HEIGHT: int = 3
    BLOCK_SIZE: int = 20  # number of grids per (square) block
    GRID_SIZE_PX: int = 3


def main():
    screen = pygame.display.set_mode((1280, 720))
    pygame.init()
    clock = pygame.time.Clock()
    running: bool = True

    while running:
        for event in pygame.event.get():
            match event.type:
                case (pygame.QUIT | pygame.KEYDOWN):
                    if event.type == pygame.KEYDOWN and event.key != pygame.K_q:
                        continue
                    running = False

        screen.fill("purple")

        pygame.display.flip()  # Refresh on-screen display
        clock.tick(60)  # wait until next frame (at 60 FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

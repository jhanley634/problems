#! /usr/bin/env python
from time import sleep

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
    pygame.display.set_mode()
    sleep(2)


if __name__ == "__main__":
    main()

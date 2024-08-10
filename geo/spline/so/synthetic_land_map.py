#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://stackoverflow.com/questions/78857047/optimizing-numpy-vectorization-for-map-generation
import numpy as np


class MapDataGen:
    """
    Procedurally generates a world map and returns a numpy array representation of it.

    Water proceeds from borders to inland.
    Water percentage increases with each iteration.
    """

    def __init__(self, start_size: int, seed: int) -> None:
        """
        Initialize starting world map.

        start_size: size of the map (start_size x start_size).
        seed: used for reproducible randomness.
        """
        # Starting map, filled with 0, start_size by start_size big.
        self.world_map = np.zeros((start_size, start_size), dtype=np.uint8)
        # Random number generator.
        self.rng = np.random.default_rng(seed)
        # List to store border tile indexes.
        self.borders = []
        self.newborders = []

    def add_land(self, land_id, from_index, to_index):
        """
        Add land to the world map at any time and at any map resolution.

        land_id: non-zero uint8, id of the new land tile (0 is reserved for water).
        from_index: starting index (inclusive) for the land area.
        to_index: ending index (exclusive) for the land area.
        """

        row_size, column_size = self.world_map.shape

        from_row = max(0, from_index[0])
        to_row = min(to_index[0], row_size)
        from_col = max(0, from_index[1])
        to_col = min(to_index[1], column_size)

        self.world_map[
            from_row:to_row,
            from_col:to_col,
        ] = land_id

        for row in range(from_row, to_row):
            for column in range(from_col, to_col):
                self.borders.append((row, column))

    def neighbours(self, index, radius) -> np.ndarray:
        """
        Returns neighbour tiles within the given radius of the index.

        index: tuple representing the index of the tile.
        radius: the radius to search for neighbours.
        """

        row_size, column_size = self.world_map.shape
        return self.world_map[
            max(0, index[0] - radius) : min(index[0] + radius + 1, row_size),
            max(0, index[1] - radius) : min(index[1] + radius + 1, column_size),
        ]

    def upscale_map(self) -> np.ndarray:
        """
        Divide each tile into 4 pieces and upscale the map by a factor of 2.

        """
        row, column = self.world_map.shape
        rs, cs = self.world_map.strides
        x = np.lib.stride_tricks.as_strided(
            self.world_map, (row, 2, column, 2), (rs, 0, cs, 0)
        )
        self.newmap = x.reshape(row * 2, column * 2)
        # \/Old version\/.
        # self.newmap = np.repeat(np.repeat(self.worldmap, 2, axis=0), 2, axis=1)

    def check_tile(self, index: tuple):
        """
        Texturize borders and update new borders.

        index: tuple representing the index of the tile to check.
        """
        # Corresponding land id to current working tile.
        tile = self.world_map[index]
        # If tile at the index is surrounded by identical tiles within a 2-tile range.
        if np.all(self.neighbours(index, 2) == tile):
            # Don't store it; this tile cannot become water because it is surrounded by 2-tile wide same land as itself.
            pass
        else:
            # The values of unique tiles and their counts.
            values, counts = np.unique_counts(self.neighbours(index, 1))
            # Randomly change each of the 4 newly descended tiles of the original tile to either water or not.
            for row in range(2):
                for column in range(2):
                    # One of the four descended tile's index.
                    new_tile_index = (index[0] * 2 + row, index[1] * 2 + column)
                    # Calculate the probability of turning into other tiles for descended tiles.
                    probability = counts.astype(np.float16)
                    probability /= np.sum(probability)
                    # Randomly chose a value according to its probability.
                    random = self.rng.choice(values, p=probability)
                    if random == 0:  # If tile at the index became water.
                        # Update it on the new map.
                        self.newmap[new_tile_index] = random
                        # Don't store it because it is a water tile and no longer a border tile.
                    elif random == tile:  # If the tile remained the same.
                        # Store it because it is still a border tile.
                        self.newborders.append(new_tile_index)
                    else:  # If the tile changed to a different land.
                        # Update it on the new map.
                        self.newmap[new_tile_index] = random
                        # Store it because it is still a border tile.
                        self.newborders.append(new_tile_index)

    def default_procedure(self):
        """
        Default procedure: upscale (or zoom into) the map and texturize borders.

        """
        self.upscale_map()
        for index in self.borders:
            self.check_tile(index)
        self.borders = self.newborders
        self.newborders = []
        self.world_map = self.newmap

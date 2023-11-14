#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.


from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

from homl3.ch02.show_counties import color_of, get_housing


def show_voronoi(want_show=False):
    housing = get_housing().to_pandas()  # We need pandas, for color support.
    housing["color"] = housing["county"].apply(color_of)
    assert len(set(housing.county)) == 58

    points = housing[["longitude", "latitude"]].to_numpy()
    assert points.shape == (20640, 2)  # dtype is float64

    vor = Voronoi(points)
    assert vor.npoints == len(points)
    fig = voronoi_plot_2d(vor)
    fig.savefig("/tmp/voronoi.png")
    if want_show:
        plt.show()


if __name__ == "__main__":
    show_voronoi()

#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.


from collections.abc import Generator

from scipy.spatial import ConvexHull, Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import pandas as pd

from homl3.ch02.show_counties import color_of, get_housing


def show_voronoi(show: bool = False) -> None:
    housing = get_housing().to_pandas()  # We need pandas, for color support.
    housing["color"] = housing["county"].apply(color_of)
    assert len(set(housing.county)) == 58

    housing["interior"] = False
    housing = discard_interior_observations(housing)
    print(len(housing))

    points = housing[["longitude", "latitude"]].to_numpy()
    assert points.shape == (20640, 2)  # dtype is float64

    vor = Voronoi(points)
    assert vor.npoints == len(points)
    fig = voronoi_plot_2d(vor)
    fig.savefig("/tmp/voronoi.png")
    if show:
        plt.show()
        print(housing[["county", "population"]].groupby("county").count())
        # San_Joaquin has 422 census tract observations; L.A. has 5861


def discard_interior_observations(housing: pd.DataFrame) -> pd.DataFrame:
    for county, num_districts in _get_large_counties(housing):
        if num_districts < 400:
            continue  # no need to prune clutter from the little ones

        h = housing
        assert 0 == sum(h.interior)
        h.loc[h.county == county, "interior"] = True

        points = h[["longitude", "latitude"]].to_numpy()
        hull = ConvexHull(points)
        print(sum(h.interior), len(h), len(hull.vertices))
        for i in hull.vertices:
            print(sum(h.interior), i, h.loc[i].longitude, h.loc[i].latitude)
            h.loc[(h.longitude == h.loc[i].longitude), "interior"] = False
        h = pd.DataFrame(h[not h.interior])

        print(county.ljust(15), len(h), len(hull.vertices), hull.volume)

    return h


def _get_large_counties(
    housing: pd.DataFrame,
) -> Generator[tuple[str, int]]:
    for county, row in (
        housing[["county", "population"]].groupby("county").count().iterrows()
    ):
        num_districts = row.population
        yield str(county), num_districts


if __name__ == "__main__":
    show_voronoi()

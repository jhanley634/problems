#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
# from https://stackoverflow.com/questions/76028510/convert-regularly-geographic-points-into-a-matrix

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
import pandas as pd

dataset = {
    "freguesia": {
        0: "Parque das Nações",
        1: "Parque das Nações",
        2: "Parque das Nações",
        3: "Parque das Nações",
        4: "Parque das Nações",
        5: "Parque das Nações",
        6: "Parque das Nações",
        7: "Parque das Nações",
        8: "Parque das Nações",
        9: "Parque das Nações",
        10: "Parque das Nações",
        11: "Parque das Nações",
        12: "Parque das Nações",
        13: "Parque das Nações",
        14: "Parque das Nações",
    },
    "Datetime": {
        0: "2022-09-07 09:30:00+00:00",
        1: "2022-09-07 09:30:00+00:00",
        2: "2022-09-07 09:30:00+00:00",
        3: "2022-09-07 09:30:00+00:00",
        4: "2022-09-07 09:30:00+00:00",
        5: "2022-09-07 09:30:00+00:00",
        6: "2022-09-07 09:30:00+00:00",
        7: "2022-09-07 09:30:00+00:00",
        8: "2022-09-07 09:30:00+00:00",
        9: "2022-09-07 09:30:00+00:00",
        10: "2022-09-07 09:30:00+00:00",
        11: "2022-09-07 09:30:00+00:00",
        12: "2022-09-07 09:30:00+00:00",
        13: "2022-09-07 09:30:00+00:00",
        14: "2022-09-07 09:30:00+00:00",
    },
    "C1": {
        0: 72.37,
        1: 4.65,
        2: 433.18,
        3: 274.43,
        4: 212.09,
        5: 49.86,
        6: 3.82,
        7: 173.22,
        8: 75.16,
        9: 506.67,
        10: 433.19,
        11: 136.86,
        12: 2.24,
        13: 0.0,
        14: 0.0,
    },
    "latitude": {
        0: 38.7537686909,
        1: 38.7537686909,
        2: 38.7551697675,
        3: 38.7551697675,
        4: 38.7551697675,
        5: 38.7551697675,
        6: 38.7551697675,
        7: 38.7565708166,
        8: 38.7565708166,
        9: 38.7565708166,
        10: 38.7565708166,
        11: 38.7565708166,
        12: 38.7565708166,
        13: 38.7565708166,
        14: 38.7565708166,
    },
    "longitude": {
        0: -9.09566985629,
        1: -9.09387322572,
        2: -9.10105974799,
        3: -9.09926311742,
        4: -9.09746648685,
        5: -9.09566985629,
        6: -9.09387322572,
        7: -9.10285637856,
        8: -9.10105974799,
        9: -9.09926311742,
        10: -9.09746648685,
        11: -9.09566985629,
        12: -9.09387322572,
        13: -9.09207659515,
        14: -9.09027996458,
    },
}


def main(show: bool = False) -> None:
    df = pd.DataFrame(dataset)
    df["Datetime"] = pd.to_datetime(df.Datetime)
    print(make_grid(df))

    crs = {"init": "epsg:4326"}
    gps_data = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.longitude, df.latitude, crs=crs)
    )
    gps_data.plot()
    if show:
        plt.show()


def make_grid(df: pd.DataFrame) -> npt.NDArray[np.int_]:
    lat_start = df.latitude.min()
    lng_start = df.longitude.min()
    lat_delta = df.latitude.diff().max()
    lng_delta = df.longitude.diff().max()
    i_max = j_max = 0
    d = {}
    for _, row in df.iterrows():
        i = round((row.latitude - lat_start) / lat_delta)
        j = round((row.longitude - lng_start) / lng_delta)
        d[(i, j)] = row.C1
        i_max = max(i, i_max)
        j_max = max(j, j_max)

    g = np.zeros((i_max + 1, j_max + 1))
    for (i, j), v in d.items():
        g[i_max - i, j] = v

    return np.array(g)


if __name__ == "__main__":
    main()

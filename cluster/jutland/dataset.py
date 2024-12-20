# Copyright 2021 John Hanley. MIT licensed.
from collections import Counter
from pathlib import Path
import re

from ydata_profiling import ProfileReport
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


class Dataset:
    TMP = Path("/tmp")
    SPATIAL = TMP / "3D_spatial_network.txt"

    @classmethod
    def get_df(cls) -> pd.DataFrame:
        """Densifies (filters) the somewhat sparse UCI roadway dataset."""
        base = re.sub(r"\.txt$", "", f"{cls.SPATIAL}")
        cache = Path(f"{base}.parquet")
        if not cache.exists():
            cols = "osm_id lon lat alt"  # Open Street Map ID, deg, deg, meters
            df = pd.read_csv(cls.SPATIAL, names=cols.split())
            assert (df.alt < 135).all()  # All mentioned roads are near sea level.
            assert (df.lat > 56.58).all()
            assert (df.lat < 57.76).all()
            assert (df.lon > 8.14).all()
            assert (df.lon < 11.20).all()
            assert 434874 == len(df), len(df)

            df = cls.filter_short_segments(df)
            # assert 405_241 == len(df), len(df)  # 3
            assert 388_147 == len(df), len(df)  # 4
            # assert 352_220 == len(df), len(df)  # 6
            # assert 287_331 == len(df), len(df)  # 10
            # assert 55_972 == len(df), len(df)  # 50

            df = df[df.lat > 57.55]
            assert 25_431 == len(df), len(df)

            cls.profile(df, Path(f"{base}.html"))
            pq.write_table(pa.Table.from_pandas(df), cache)

        # Elapsed time is less than two seconds.
        return pd.DataFrame(pq.read_table(cache).to_pandas())

    @staticmethod
    def filter_short_segments(df: pd.DataFrame, k: int = 4) -> pd.DataFrame:
        """Demands that a given osm_id shall have at least K segments.

        So e.g. singleton "roads", containing just a single point, are discarded.
        """
        counts = Counter(df.osm_id)
        small_roads = {osm_id for osm_id, count in counts.items() if count < k}
        return df[~df.osm_id.isin(small_roads)]

    @staticmethod
    def profile(df: pd.DataFrame, out: Path) -> None:
        if not out.exists():
            ProfileReport(df).to_file(out)

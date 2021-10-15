
from collections import Counter
from pathlib import Path
import re

from pandas_profiling import ProfileReport
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


class Dataset:

    TMP = Path('/tmp')
    SPATIAL = TMP / '3D_spatial_network.txt'

    @classmethod
    def get_df(cls):
        """Densifies (filters) the somewhat sparse UCI roadway dataset."""
        base = re.sub(r'\.txt$', '', f'{cls.SPATIAL}')
        cache = Path(f'{base}.parquet')
        if not cache.exists():
            cols = 'osm_id lon lat alt'  # Open Street Map ID, deg, deg, meters
            df = pd.read_csv(cls.SPATIAL, names=cols.split())
            assert (df.alt < 135).all()  # All mentioned roads are near sea level.
            assert 434874 == len(df), len(df)

            df = cls.filter_short_segments(df)
            assert 287331 == len(df), len(df)

            cls.profile(df, Path(f'{base}.html'))
            pq.write_table(pa.Table.from_pandas(df), cache)

        return pq.read_table(cache).to_pandas()  # Elapsed time is less than two seconds.

    @staticmethod
    def filter_short_segments(df: pd.DataFrame, k=10):
        """Demands that a given osm_id shall have at least K segments.

        So e.g. singleton "roads", containing just a single point, are discarded.
        """
        counts = Counter(df.osm_id)
        small_roads = set(osm_id
                          for osm_id, count in counts.items()
                          if count < k)
        return df[~df.osm_id.isin(small_roads)]

    @staticmethod
    def profile(df: pd.DataFrame, out: Path):
        if not out.exists():
            ProfileReport(df).to_file(out)

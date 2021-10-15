
from pathlib import Path
import re

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


class Dataset:

    TMP = Path('/tmp')
    SPATIAL = TMP / '3D_spatial_network.txt'

    @classmethod
    def get_df(cls):
        """Densifies (filters) the somewhat sparse UCI roadway dataset."""
        cache = Path(re.sub(r'\.txt$', '.parquet', f'{cls.SPATIAL}'))
        if not cache.exists():
            cols = 'osm_id lon lat alt'  # Open Street Map ID, deg, deg, meters
            df = pd.read_csv(cls.SPATIAL, names=cols.split())
            pq.write_table(pa.Table.from_pandas(df), cache)

        return pq.read_table(cache).to_pandas()  # Elapsed time is less than two seconds.

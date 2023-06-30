#! /usr/bin/env _TYPER_STANDARD_TRACEBACK=1 python
# Copyright 2023 John Hanley. MIT licensed.
from pathlib import Path
import struct

from pydub import AudioSegment
from scipy.fftpack import rfft
from typer import Option
from typing_extensions import Annotated
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import typer


def main(mp3_file: Annotated[Path, Option(help="input audio file", default=None)]):
    sound1 = AudioSegment.from_file(mp3_file.expanduser())
    msec_per_sec = 1000
    start = 3 * msec_per_sec
    end = 3.25 * msec_per_sec
    sound = AudioSegment.from_mono_audiosegments(sound1[start:end])
    print(sound.frame_rate)  # CD quality, 44100 Hz

    raw_data = sound.raw_data  # needs to be mono
    channels = sound.channels
    assert channels == 1
    assert sound.frame_width == 2
    assert sound.duration_seconds == (end - start) / msec_per_sec == 0.25

    fmt = "%ih" % sound.frame_count() * channels
    df = pd.DataFrame()
    df["amplitudes"] = struct.unpack(fmt, raw_data)
    df["y"] = np.abs(rfft(df.amplitudes))
    print(df.iloc[170:190])
    assert len(df) == sound.frame_count()

    print(df.dtypes)
    ax = sns.scatterplot(df)
    ax.set_xlim([0, 1040])
    plt.show()


if __name__ == "__main__":
    typer.run(main)

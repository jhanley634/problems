#! /usr/bin/env _TYPER_STANDARD_TRACEBACK=1 python
# Copyright 2023 John Hanley. MIT licensed.
from pathlib import Path
from pprint import pp
import struct

from pyAudioAnalysis import ShortTermFeatures, audioBasicIO
from pydub import AudioSegment
from scipy.fft import rfft, rfftfreq
from typer import Option
from typing_extensions import Annotated
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import typer


def demo_350_440_hz(input_file: Path):
    Fs, x = audioBasicIO.read_audio_file(input_file)
    F, f_names = ShortTermFeatures.feature_extraction(x, Fs, 0.050 * Fs, 0.025 * Fs)
    pp(f_names)
    plt.subplot(2, 1, 1)
    plt.plot(F[0, :])
    plt.xlabel("Frame no")
    plt.ylabel(f_names[0])
    plt.subplot(2, 1, 2)
    plt.plot(F[1, :])
    plt.xlabel("Frame no")
    plt.ylabel(f_names[1])
    plt.show()

    duration = 10  # seconds
    freq = 350  # Hz
    n = 2048
    x = (
        np.sin(2 * np.pi * freq * np.linspace(0, duration, n))
        + np.random.random(n) * 0.1
    )

    z = np.abs(np.fft.rfft(x))  # FFT, peak at .05
    y = np.fft.rfftfreq(len(x), d=1)  # Frequency data

    fig, ax = plt.subplots()
    ax.plot(y, z)

    plt.show()


def demo():
    n = 2048
    x = np.sin(2 * np.pi * 10 * np.linspace(0, 10, n)) + np.random.random(n) * 0.1

    z = np.abs(np.fft.rfft(x))  # FFT, peak at .05
    y = np.fft.rfftfreq(len(x))  # Frequency data

    fig, ax = plt.subplots()
    ax.plot(y, z)

    plt.show()


def main(mp3_file: Annotated[Path, Option(help="input audio file", default=None)]):
    return demo()
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
    amplitudes = struct.unpack(fmt, raw_data)
    df = pd.DataFrame()
    df["y"] = np.abs(rfft(amplitudes))
    print(df.iloc[170:190])

    df["y"] = rfftfreq(len(amplitudes), 1 / sound.frame_rate)
    print(df.dtypes)
    ax = sns.scatterplot(df)
    ax.set_xlim([0, 1040])
    plt.show()


if __name__ == "__main__":
    typer.run(demo_350_440_hz)

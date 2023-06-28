#! /usr/bin/env _TYPER_STANDARD_TRACEBACK=1 python
# Copyright 2023 John Hanley. MIT licensed.
from pathlib import Path

from pydub import AudioSegment
from pylab import legend, linspace, log10, pi, plot, randn, xlabel, ylabel
from spectrum import Periodogram, arma2psd, aryule
from typer import Option
from typing_extensions import Annotated
import matplotlib.pyplot as plt
import scipy.signal
import typer


def main(mp3_file: Annotated[Path, Option(help="input audio file", default=None)]):
    sound1 = AudioSegment.from_file(mp3_file.expanduser())
    print(
        sound1.duration_seconds,
        sound1.channels,
        sound1.frame_rate,
        sound1.sample_width,
        sound1,
        type(sound1),
    )

    # from https://pyspectrum.readthedocs.io/en/latest/tutorial_yulewalker.html

    # Create a AR model
    a = [1, -2.2137, 2.9403, -2.1697, 0.9606]
    # create some data based on these AR parameters
    y = scipy.signal.lfilter([1], a, randn(1, 1024))
    # if we know only the data, we estimate the PSD using Periodogram
    p = Periodogram(y[0], sampling=2)  # y is a list of list hence the y[0]
    p.plot(label="Model ouput")

    # now, let us try to estimate the original AR parameters
    AR, P, k = aryule(y[0], 4)
    PSD = arma2psd(AR, NFFT=512)
    PSD = PSD[len(PSD) : len(PSD) // 2 : -1]
    plot(
        linspace(0, 1, len(PSD)),
        10 * log10(abs(PSD) * 2.0 / (2.0 * pi)),
        label="Estimate of y using Yule-Walker AR(4)",
    )
    xlabel(r"Normalized frequency (\times \pi rad/sample)")
    ylabel("One-sided PSD (dB/rad/sample)")
    legend()
    plt.show()


if __name__ == "__main__":
    typer.run(main)

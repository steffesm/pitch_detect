#  Copyright (c) 2021.

from enum import IntEnum, unique
from collections import namedtuple

import numpy as np
from matplotlib import pyplot as plt

from wave_unify import WaveUnifyData


# region simple types and enums
FreqSignal = namedtuple('FreqSignal', 'freq sig')

# endregion


class FreqDetect:
    _MIN_PER = 5
    _MIN_FREQ = 20  # Hz


    def __init__(self,
                 # wave: WaveUnifyData,
                 samples: np.ndarray,
                 sample_rate,
    ):
        self._smpls = samples
        self._smpl_rate = sample_rate
        self.start = 0
        self.end = (len(self._smpls)-1) / self._smpl_rate

        # fft_peaks = np.r_[True, fft_res[1:] < fft_res[:-1]] & np.r_[fft_res[:-1] < fft_res[1:], True]

    # region FFT functions
    def fft(self, start=None, end=None):
        """returns frequencies and fft-signal from start to end time"""
        start = self.start if start is None else start
        end = self.end if end is None else end

        smpl_start = int(start * self._smpl_rate)
        smpl_end = int(end * self._smpl_rate)
        smpl_len = smpl_end - smpl_start + 1
        smpl_slice = self._smpls[smpl_start:smpl_end]

        # do fft on slice and get associated frequencies
        fft_freqs = np.fft.rfftfreq(len(smpl_slice), self._smpl_rate)
        fft_raw = np.fft.rfft(smpl_slice)

        # match fft to frequencies
        fft_scale = fft_raw / smpl_len * 2
        fft_sig = np.abs(fft_scale).real

        # format for external use
        fft_res = FreqSignal(fft_freqs, fft_sig)
        return fft_res

    # endregion

    # region plots

    def plot_fft(self,
                 signals,
                 title=None,
                 normalize: bool = None):
        """plots result of fft, expects iterable of FreqSignal type"""
        try:
            signals[0][0][0]
        except IndexError:
            signals = (signals, )
        fig1 = plt.figure(title)
        plots = fig1.subplots(len(signals), 1, sharex=True)
        if len(signals) == 1:
            plots = (plots, )
        for i, fft in enumerate(signals):
            freqs_x = fft.freq
            sig_in = fft.sig
            sig_norm = sig_in
            if normalize:
                sig_max = np.max(np.abs(sig_in))
                if sig_max != 0:
                    sig_norm = sig_in.astype('float64') / sig_max
            sig = sig_norm
            ax = plots[i]
            ax.step(freqs_x, sig)
            ax.grid()
            # ax.legend(loc='best')
        return

    # endregion

    # regionblub tbd

if __name__ == "__main__":
    debug_fft = False
    debug_plot = False
    file1 = "440.wav"
    file2 = "Kammerton.wav"

    wave1 = WaveUnifyData(file2)

    fd1 = FreqDetect(wave1.samples_mono, wave1.sample_rate)

    fft1 = fd1.fft()
    fd1.plot_fft(fft1)

    plt.show()

#  Copyright (c) 2021

from enum import IntEnum, unique

import numpy as np
from matplotlib import pyplot as plt
import string
import scipy.io.wavfile as wavfile


class WaveUnifyData:

    # region channels for stereo, surround sound
    @unique
    class Channels(IntEnum):
        FRONT_LEFT = 0
        FRONT_RIGHT = 1
        CENTER = 2
        SUBWOOFER_FREQUENCY = 3
        REAR_LEFT = 4
        REAR_RIGHT = 5
        ALTERNATIVE_REAR_LEFT = 6
        ALTERNATIVE_REAR_RIGHT = 7

    CHANNELS_ALL = (
        Channels.FRONT_LEFT,
        Channels.FRONT_RIGHT,
        Channels.CENTER,
        Channels.SUBWOOFER_FREQUENCY,
        Channels.REAR_LEFT,
        Channels.REAR_RIGHT,
        Channels.ALTERNATIVE_REAR_LEFT,
        Channels.ALTERNATIVE_REAR_RIGHT,
    )

    CHANNELS_CENTER = (
        Channels.CENTER,
        Channels.SUBWOOFER_FREQUENCY,
    )

    CHANNELS_RIGHT = (
        Channels.FRONT_RIGHT,
        Channels.REAR_RIGHT,
        Channels.ALTERNATIVE_REAR_RIGHT,
    )

    CHANNELS_LEFT = (
        Channels.FRONT_LEFT,
        Channels.REAR_LEFT,
        Channels.ALTERNATIVE_REAR_LEFT,
    )

    CHANNELS_FRONT = (
        Channels.FRONT_LEFT,
        Channels.FRONT_RIGHT,
    )

    CHANNELS_REAR = (
        Channels.REAR_LEFT,
        Channels.REAR_RIGHT,
        Channels.ALTERNATIVE_REAR_LEFT,
        Channels.ALTERNATIVE_REAR_RIGHT,
    )
    # endregion

    def __init__(self,
                 filename: string,
                 ):
        # self._filename = filename
        self._wav = wavfile.read(filename)
        self._smpl_rate = self._wav[0]
        self._dat = self._wav[1]
        self.start = 0
        self.end = -1

    # region basic wave-file properties

    # @property
    # def start(self):
    #     return self._index_start
    #
    # @property
    # def end(self):
    #     return self._index_end

    @property
    def sample_rate(self):
        return self._smpl_rate

    @property
    def mono(self) -> bool:
        ret = not len(self._dat.shape) > 1
        return ret

    @property
    def channels(self):
        if self.mono:
            return 1
        return self._dat.shape[1]

    def dat_slice(self, start=None, end=None):
        start = self.start if start is None else start
        end = self.end if end is None else end
        if start == 0 and end == -1:
            return self._dat  # avoid array operations
        return self._dat[start:end]

    def time_slice(self, start=None, end=None):
        start = self.start if start is None else start
        end = self.end if end is None else end
        time_range = range(0, end-start) / self._smpl_rate
        if start == 0 and end == -1:
            return self._dat  # avoid array operations
        return self._dat[start:end]

    # endregion

    # region access to wave-file data
    @property
    def samples_mono(self) -> np.ndarray:
        """return mono signal from wave

        multiple channels are averaged
        """
        dat = self.dat_slice()
        if self.mono:
            # already mono
            return dat
        # convert stereo to mono: average
        dat_sum = np.sum(dat, 1)
        dat_ret = dat_sum / dat.shape[1]
        return dat_ret[self.start:self.end]

    def _get_channels(self, channels) -> dict:
        ch_max = self.channels - 1
        ch_dict = {}
        dat = self.dat_slice()
        for i, ch in enumerate(channels):
            sig = None
            if ch <= ch_max:
                sig = dat[:, ch]
                ch_dict.update({ch: sig})
        return ch_dict

    def _sum_channels(self, channel_sets) -> list:
        sig_set = []
        for ch_set in (channel_sets):
            sig_dict = self._get_channels(ch_set)
            sig_list = list(sig_dict.values())
            sig_sum = np.sum(sig_list, 0)
            sig_set.append(sig_sum)
        return sig_set

    @property
    def stereo_diff(self) -> np.ndarray:
        """provide difference of left and right channels"""
        if self.mono:
            raise TypeError("object does not support stereo-signals")
        channel_sets = (self.CHANNELS_LEFT, self.CHANNELS_RIGHT)
        sig_set = self._sum_channels(channel_sets)
        sig_res = sig_set[1] - sig_set[0]
        return sig_res

    @property
    def stereo_sum(self) -> np.ndarray:
        """provide sum of left and right channels"""
        if self.mono:
            raise TypeError("object does not support stereo-signals")
        channel_sets = (self.CHANNELS_LEFT, self.CHANNELS_RIGHT)
        sig_set = self._sum_channels(channel_sets)
        sig_res = (sig_set[1] + sig_set[0]) / 2
        return sig_res

    # endregion

    # region plots
    def plot_mono(self, **kwargs):
        sig_mono = self.samples_mono
        sig_diff = np.diff(sig_mono)

        self.plot_signals((
            sig_mono,
            sig_diff,
        ),
        **kwargs,
        )
        return

    def plot_signals(self,
                     signals,
                     title=None,
                     normalize: bool = None):
        try:
            signals[0][0]
        except IndexError:
            signals = (signals, )
        fig1 = plt.figure(title)
        plots = fig1.subplots(len(signals), 1, sharex=True)
        if len(signals) == 1:
            plots = (plots, )
        for i, sig_in in enumerate(signals):
            sig_norm = sig_in
            if normalize:
                sig_max = np.max(np.abs(sig_in))
                if sig_max != 0:
                    sig_norm = sig_in.astype('float64') / sig_max
            sig = sig_norm
            sig_rng = np.arange(0, len(sig)) / self._smpl_rate
            ax = plots[i]
            ax.step(sig_rng, sig)
            ax.grid()
            # ax.legend(loc='best')
        return

    # endregion

    # regionblub tbd


if __name__ == "__main__":
    file1 = "440.wav"
    file2 = "Kammerton.wav"

    fm1 = WaveUnifyData(file2)
    stereo_sum = fm1.stereo_sum
    signals = [
        fm1.stereo_diff,
        stereo_sum,
        np.diff(stereo_sum)
    ]
    # fm1.plot_mono()
    fm1.plot_signals(signals, normalize=True)
    plt.show()

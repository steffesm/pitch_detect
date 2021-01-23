#  Copyright (c) 2021.

import pytest
import urllib

import numpy as np
from matplotlib import pyplot as plt

from wave_unify import WaveUnifyData
from freq_detect import FreqDetect

show_plots = False
normalize_plots = True
plot_length = 5000

# region helper functions

def plot_show():
    if show_plots:
        plt.show()

def create_wav_files():
    file_links = {
        'sine1.wav': "https://www3.nd.edu/~dthain/courses/cse20211/fall2013/wavfile/sine.wav",
        'sine2.wav': "https://www3.nd.edu/~dthain/courses/cse20211/fall2013/wavfile/sine2.wav",
        'sine3.wav': "https://www3.nd.edu/~dthain/courses/cse20211/fall2013/wavfile/sine3.wav",
    }
    for name, link in file_links.items():
        # check if file exists,
        try:
            file = open(name)
        except IOError:
            file_exists = False
        else:
            file_exists = True
        finally:
            file.close()
        if not file_exists:
            urllib.request.urlretrieve(link, name)
    return file_links.keys()

def get_waves():
    files = create_wav_files()
    wave_dict = {}
    for file in files:
        wavdat = WaveUnifyData(file)
        wave_dict.update({file: wavdat})
    return wave_dict

def get_freqs():
    freq_dict ={}
    for name, wave in get_waves().items():
        freq_det = FreqDetect(wave.sample_rate, wave.samples_mono)
        freq_dict.update({name: freq_det})
    return freq_dict

# endregion

# region fixtures

@pytest.fixture()
def wav_files():
    return create_wav_files()

# endregion

# region tests

def test_plot_signals(wav_files):
    for filename in wav_files:
        fmi = WaveUnifyData(filename)
        fmi.end = plot_length
        plot_args = {
            'title': "Signal " + filename,
            'normalize': normalize_plots,
        }
        if fmi.mono:
            fmi.plot_mono(**plot_args)
        else:
            stereo_sum = fmi.stereo_sum
            signals = [
                fmi.stereo_diff,
                stereo_sum,
                np.diff(stereo_sum),
            ]
            fmi.plot_signals(
                signals,
                **plot_args,
            )
    plot_show()

def test_plot_fft(wav_files):
    for filename in wav_files:
        wave_i = WaveUnifyData(filename)
        fd1 = FreqDetect(wave_i.samples_mono, wave_i.sample_rate)
        fft_i = fd1.fft()
        fd1.plot_fft(
            fft_i,
            title="FFT "+filename,
            normalize=normalize_plots,
        )
    plot_show()

# endregion

# region exports

files_list = list(create_wav_files())
file1 = files_list[0]

waves_dict = get_waves()
waves_list = list(waves_dict.values())
wave1 = waves_list[0]

freqs_dict = get_freqs()
freqs_list = list(freqs_dict.values())
freq1 = freqs_list[0]

# endregion

# region main

if __name__ == '__main__':
    show_plots = True
    normalize_plots = 2 ** 15
    plot_length = 5000

    pytest.main()

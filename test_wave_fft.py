#  Copyright (c) 2021.

import pytest
import urllib

import numpy as np
from matplotlib import pyplot as plt

from wave_unify import WaveUnifyData

plot_show = True
plot_length = 1000

# region helper functions

def plot_show():
    if plot_show:
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
    waves_dict = {}
    for file in files:
        wavdat = WaveUnifyData(file)
        waves_dict.update({file: wavdat})
    return waves_dict

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
            'normalize': True,
        }
        if fmi.mono:
            fmi.plot_mono(**plot_args)
        else:
            signals = [
                fmi.stereo_diff,
                fmi.stereo_sum,
                np.diff(signals[1]),
            ]
            fmi.plot_signals(
                signals,
                **plot_args,
            )
    plot_show()

def test_plot_fft(wav_files):
    for filename in wav_files:
        fmi = WaveUnifyData(filename)
        fmi.end = plot_length
        if fmi.mono:
            fmi.plot_mono(normalize=False)
        else:
            signals = [
                fmi.stereo_diff,
                fmi.stereo_sum,
                np.diff(signals[1]),
            ]
            fmi.plot_signals(signals, normalize=True)
    plot_show()

# endregion

# region exports

files_list = list(create_wav_files())
file1 = files_list[0]

waves_dict = get_waves()
waves_list = list(waves_dict.values())
wave1 = waves_list[0]

# endregion

# region main

if __name__ == '__main__':
    pytest.main()

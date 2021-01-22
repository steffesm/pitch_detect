import pytest
import urllib

import numpy as np
from matplotlib import pyplot as plt

from wave_unify import WaveUnifyData

plot_show = True
plot_length = 1000

def plot_show():
    if plot_show:
        plt.show()

@pytest.fixture()
def wav_files():
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

def test_plot_signals(wav_files):
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

if __name__ == '__main__':
    pytest.main()

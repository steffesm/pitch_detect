#  Copyright (c) 2021.

import urllib.request


files = {
    'sine1.wav': "https://www3.nd.edu/~dthain/courses/cse20211/fall2013/wavfile/sine.wav",
    'sine2.wav': "https://www3.nd.edu/~dthain/courses/cse20211/fall2013/wavfile/sine2.wav",
    'sine3.wav': "https://www3.nd.edu/~dthain/courses/cse20211/fall2013/wavfile/sine3.wav",
}


def get_files():
    for name, link in files.items():
        print(f"filename={name}, url={link}")
        urllib.request.urlretrieve(link, name)
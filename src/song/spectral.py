from scipy import signal
import numpy as np
from .utils import freq_to_bucket


def my_stft(song, w="hann", win_len=2048, hop_size=128):
    w = signal.get_window(w, win_len)
    short = np.zeros(shape=(4096, (len(song) - win_len) // hop_size), dtype=complex)
    for i in range(0, len(song) - win_len, hop_size):
        windowed = song[i:i + win_len] * w
        this = np.fft.fft(windowed, n=8192)
        this = this[:len(this) // 2]
        short[:, (i // hop_size) - 1] = this
    return short


def refined_log_freq_spec(spect, bins=128):
    # TODO: This function breaks if freq_to_buckets cents is set to anything small as it tries to get negative index
    song_length = len(spect[0])
    new_full = np.zeros(shape=(bins, song_length), dtype='complex')
    for index in range(1, len(spect)):
        print(index)
        if freq_to_bucket(index) >= 128:
            break
        new_full[freq_to_bucket(index)] += spect[index]
    return new_full

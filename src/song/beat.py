import numpy as np
from .utils import log_compression
# import read
from scipy import signal
import matplotlib.pyplot as plt


def half_w_rect(song):
    """Returns the half wave rectification of a song"""
    tes = song.copy()
    tes = np.where(tes < 0, 0, tes)   # Had to add extra abs as was returning some negatives
    return tes


def e_novelty(song, window="hann", win_len=2048, hop_size=512):
    energy = np.empty(shape=(len(song))//hop_size)
    w = signal.get_window(window, win_len)
    # hwr = half_w_rect(song)
    song = abs(song)
    song = np.log(song + 1)
    print(song[-100:])
    for frame in range(0, len(song) - win_len - hop_size, hop_size):
        currf = w * song[frame:frame+win_len]
        # print(np.sum(currf))
        nextf = w * song[frame+hop_size:frame+win_len+hop_size]
        e = (np.mean(nextf)) - (np.mean(currf))
        # e = half_w_rect(e)
        # e = np.sum(e)
        energy[frame//hop_size] = e
    energy = half_w_rect(energy)
    # print(energy.shape)
    # print(energy)
    return energy


def log_e_novelty(song, window="hann", win_len=1024, hop_size=256):
    # TODO: Merge these functions into one with log option
    # TODO: Fix the log
    energy = np.empty(shape=len(song)-1)
    w = signal.get_window(window, win_len)
    hwr = half_w_rect(song)
    for frame in range(0, len(song) - win_len-hop_size, hop_size):
        currf = w * hwr[frame:frame+win_len]
        nextf = w * hwr[frame+hop_size:frame+win_len+hop_size]
        e = np.log(nextf/currf)
        e[e < 0] = 0
        e = np.sum(e)
        energy[frame] = np.abs(e)
    return energy


def spec_novelty(song, window="hann", win_len=1024, hop_size=256):
    # Compute STFT
    _, _, x = signal.stft(song, nperseg=win_len, nfft=4096, noverlap=win_len-hop_size)
    # Log compression
    x = log_compression(x, 100)
    # x = abs(x)
    hop_size = 2
    win_len = 8
    # print(x.shape)

    energy = np.empty(shape=(len(x.T)) // hop_size, dtype="complex")
    print(energy.shape)
    for frame in range(0, len(x.T) - win_len - hop_size, hop_size):
        currf = x[:, frame:frame+win_len]
        # print(currf.shape)
        nextf = x[:, frame+hop_size:frame+win_len+hop_size]
        print(frame//hop_size)
        # print(nextf.shape)
        e = spec_diff(currf, nextf)
        # e = np.mean(nextf) - np.mean(currf)
        e = np.sum(e)
        energy[frame//hop_size] = e
    energy = half_w_rect(energy)
    print(energy)
    return energy


def spec_diff(curr, nextf):
    diff = nextf - curr
    diff = np.sum(diff, axis=0)
    return diff
# sr, song = read.read('../../Songs/440.wav')
#
# song = song[:400]
# plt.plot(song)
# plt.show()
# plt.plot(half_w_rect(song))
# plt.show()
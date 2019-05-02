import numpy as np
from .utils import log_compression
# import read
from scipy import signal
from .read import read, startend
import matplotlib.pyplot as plt
from librosa.beat import tempo


def get_bpm(song):
    sr, song = read(song)
    song = startend(song)
    song = song * 1.0
    bpm = tempo(song, sr=sr)[0]
    return bpm



def half_w_rect(song):
    """Returns the half wave rectification of a song"""
    tes = song.copy()
    tes = np.where(tes > 0, tes, 0)   # Had to add extra abs as was returning some negatives
    return tes


def e_novelty(song, window="hann", win_len=2048, hop_size=512):
    energy = np.empty(shape=(len(song))//hop_size)
    w = signal.get_window(window, win_len)
    # hwr = half_w_rect(song)
    song = abs(song)
    song = np.log(song + 1)
    # print(song[-100:])
    for frame in range(0, len(song) - win_len - hop_size, hop_size):
        currf = w * song[frame:frame+win_len]
        # print(np.sum(currf))
        nextf = w * song[frame+hop_size:frame+win_len+hop_size]
        e = (np.mean(nextf)) - (np.mean(currf))
        energy[frame//hop_size] = e
    energy = half_w_rect(energy)
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


def moving_average(data_set, periods=3):
    weights = np.ones(periods) / periods
    return np.convolve(data_set, weights, mode='valid')


def spec_novelty(song, window="hann", win_len=2048, hop_size=256, spec=False):
    # TODO: Add average
    # TODO: Fix issue with last few frames
    # Compute STFT

    if not spec:
        _, _, x = signal.stft(song, nperseg=win_len, nfft=4096, noverlap=win_len-hop_size)
    else:
        x = song
    # Log compression
    x = log_compression(x, 100)
    hop_size = 1
    win_len = 8
    x = abs(x)
    energy = np.empty(shape=(len(x.T)) // hop_size)
    for frame in range(0, len(x.T) - win_len - hop_size - win_len, hop_size):
        currf = x[:, frame:frame+win_len]
        nextf = x[:, frame+hop_size:frame+win_len+hop_size]
        e = spec_diff(currf, nextf)
        e = np.sum(e)
        energy[frame//hop_size] = e
    # energy = half_w_rect(energy)
    return energy


def spec_diff(curr, nextf):
    diff = nextf - curr
    diff = np.sum(diff, axis=0)
    diff = half_w_rect(diff)
    return diff


def get_onsets(song):
    onset_env = spec_novelty(song)
    onsets, _ = signal.find_peaks(onset_env[:-10], height=np.mean(onset_env))
    return onsets*8

import numpy as np
from scipy.signal import get_window
from .utils import log_compression

def half_w_rect(song):
    """Returns the half wave rectification of a song"""
    tes = song.copy()
    tes = np.where(tes >= 0, np.abs((tes+np.abs(tes))/2), 0)   # Had to add extra abs as was returning some negatives
    return tes


def e_novelty(song, window="hann", win_len=1024, hop_size=512):
    energy = np.empty(shape=len(song)-1)
    w = get_window(window, win_len)
    hwr = half_w_rect(song)
    for frame in range(0, len(song) - win_len - hop_size, hop_size):
        curr = w * hwr[frame:frame+win_len]
        next = w * hwr[frame+hop_size:frame+win_len+hop_size]
        e = next - curr
        e[e < 0] = 0
        e = np.sum(e)
        energy[frame] = np.abs(e)
    return energy


def log_e_novelty(song, window="hann", win_len=1024, hop_size=256):
    # TODO: Merge these functions into one with log option
    # TODO: Fix the log
    energy = np.empty(shape=len(song)-1)
    w = get_window(window, win_len)
    hwr = half_w_rect(song)
    for frame in range(0, len(song) - win_len-hop_size, hop_size):
        curr = w * hwr[frame:frame+win_len]
        next = w * hwr[frame+hop_size:frame+win_len+hop_size]
        e = np.log(next/curr)
        e[e < 0] = 0
        e = np.sum(e)
        energy[frame] = np.abs(e)
    return energy


def spec_novelty(song, window="hann", win_len=1024, hop_size=256):
    pass
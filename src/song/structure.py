from . import utils
from scipy import signal
from scipy.ndimage import median_filter
from scipy.spatial.distance import cdist
from . import spectral
import numpy as np
import matplotlib.pyplot as plt


def split_pos(arr):
    arr = np.array(arr)
    pos = arr.copy()
    neg = arr.copy()
    pos[pos < 0] = 0
    neg[neg > 0] = 0
    return pos, abs(neg)


def chroma_structure(song):
    """
    Creates a self-similarity matrix from a spectrogram for collecting information on the chroma structure
    :param song: a wave representation of a song
    :return: an n*n similarity matrix where n is the number of frames in spectrogram
    """
    _, _, x = signal.stft(song, nperseg=8192, nfft=8192)
    x = np.abs(x)
    x = spectral.log_spec(x)
    x = spectral.chromagram(x)
    dist = cdist(x.T, x.T, metric='cosine')
    dist = 1 - dist
    dist[np.isnan(dist)] = 0
    np.fill_diagonal(dist, 1)
    return dist


def sim_to_lag(sim):
    lag = sim.copy()
    idx_slice = [slice(None)] * lag.ndim
    for i in range(1, len(sim)):
        idx_slice[1] = i
        lag[tuple(idx_slice)] = np.roll(lag[tuple(idx_slice)], -i)
    lag = median_filter(abs(lag), size=(1, 250))
    return lag


def get_energy(lag):
    energy = np.zeros(shape=len(lag))
    for frame in range(0, len(lag) - 1):
        energy[frame] = np.linalg.norm(lag[:, frame + 1]) - np.linalg.norm(lag[:, frame])
    return energy


def find_segments(song, bpm):
    dist = chroma_structure(song)
    footie = np.zeros(shape=(100, 100))
    np.fill_diagonal(footie, 1)

    mask = median_filter(abs(dist), footprint=footie)
    mask[mask < .75] = 0
    mask[mask > 0] = 1
    dist = dist * mask
    lag = sim_to_lag(dist)
    energy = get_energy(lag)
    p, n = split_pos(energy)

    gaps = utils.beats_to_frames(16, bpm, 4096, 44100)

    starts, _ = signal.find_peaks(p, distance=gaps)  # , prominence=0.04)
    srpeaks = starts * 4096
    srpeaks = list(srpeaks)
    plt.pcolormesh(dist)
    for peak in starts:
        plt.axhline(y=peak)
        plt.axvline(x=peak)
    plt.savefig("ummmmm", quality=95)
    return srpeaks

from scipy import signal
import numpy as np
from .utils import freq_to_bucket, select_peaks
import matplotlib.pyplot as plt
from scipy.ndimage.filters import uniform_filter1d
import math


# def my_stft(song, w="hann", win_len=2048, hop_size=128):
#     w = signal.get_window(w, win_len)
#     short = np.zeros(shape=(4097, (len(song) - win_len) // hop_size), dtype=complex)
#     for i in range(0, len(song) - win_len, hop_size):
#         windowed = song[i:i + win_len] * w
#         this = np.fft.rfft(windowed, n=8192)
#         short[:, (i // hop_size) - 1] = this
#     return short


# def refined_log_freq_spec(spect, bins=128, nfft=8192):
#     song_length = len(spect[0])
#     new_full = np.zeros(shape=(bins, song_length))
#     for index in range(1, len(spect)):
#         if freq_to_bucket(index) >= 128:
#             break
#         new_full[freq_to_bucket(index)] += spect[index]
#     return new_full


def log_spec(spect, bins=128, nfft=8192, sr=44100):
    song_length = len(spect[0])
    new_full = np.zeros(shape=(bins, song_length))
    for frame in range(1, len(spect.T)):
        avg = uniform_filter1d(abs(spect[:, frame]), 100)
        peaks, _ = signal.find_peaks(abs(spect[:, frame]), height=avg, prominence=5)
        # peaks, _ = signal.find_peaks(abs(spect[:, frame]), height=np.mean(abs(spect[:, frame])), prominence=avg)
        # peaks, _ = signal.find_peaks(abs(spect[:, frame]))
        for peak in peaks:
            # offset = np.angle(spect[peak, frame] - spect[peak, frame-1] - (((2 * np.pi * 256) / 8192) * frame)) * \
            #          (8192 / (2 * np.pi * 256))
            if freq_to_bucket(peak, nfft=nfft, sr=sr) >= 128:
                break
            new_full[freq_to_bucket(peak, nfft=nfft, sr=sr), frame] += abs(spect[peak, frame])
    return new_full


def get_phase(points, frame):
    return frame[points] - frame[points].real


def salience(spec, logged=True):
    """
    Take log spec
    pick peaks
    remove lower peaks
    sum harms
    remove all lower value peaks
    """
    for frame in range(len(spec.T)):
        peaks, spec[:, frame] = select_peaks(spec.T[frame], threshold=lambda x: x, keep=True)
        test = spec[:, frame]
        # test[test > 0] = 1
        spec[:, frame] = test
        harmonic_summation(spec[:, frame], peaks, [1, .5, .33, .25], logged=logged)
    return spec


# def temp_function(spec):
#     spec = refined_log_freq_spec(spec)
#     spec[spec > np.max(spec)/80] = 0
#     spec = maximum_filter(abs(spec), size=(1, 4))
#     mask = median_filter(abs(spec), size=(1, 32))
#     mask[mask > 0] = 1
#     spec = spec * mask
#     return spec


def harmonic_summation(frame, peaks, weights, logged=True):
    """
    :param frame: a frame of your stft
    :param peaks: the location of the peaks
    :param weights: the weights for each harmonic
    :param logged: where the spectrogram has been binned into midi bins
    """
    for peak in peaks:
        harms = np.array(([peak]*4))
        if logged:
            harms += np.array([12, 19, 24, 28])
            fbins = 128
        else:
            harms = (harms+1) * np.array([2, 3, 4, 5])
            fbins = 4096
        for harm, weight in zip(harms, weights):
            if harm < fbins:
                frame[peak] += frame[harm]*weight


def chromagram(logspec):
    chroma = np.zeros(shape=(12, len(logspec[0])))
    for i in range(0, len(logspec), 12):
        try:
            chroma += logspec[i:i+12]
        except:
            chroma[0:8] += logspec[i:i+8]
    return chroma


def display(spec, text="STFT", color='Greys'):
    plt.pcolormesh(np.abs(spec), cmap=plt.cm.get_cmap(color))
    plt.colorbar()
    plt.title(text)
    # plt.ylabel('Frequency ')
    # plt.xlabel('Time ')
    plt.show()


def octave_weak(frame):
    for f in range(len(frame)-12):
        if frame[f] > 0:
            frame[f+12] *= 1/frame[f]


def non_zero_average_std(arr):
    nonz = np.nonzero(arr)[0]
    if nonz.any():
        return np.mean(arr[nonz]), np.std(arr[nonz])
    else:
        return 0, 0

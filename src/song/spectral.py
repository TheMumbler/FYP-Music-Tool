from scipy import signal
import numpy as np
from .utils import freq_to_bucket, select_peaks
import matplotlib.pyplot as plt
from scipy.ndimage import maximum_filter
from scipy.ndimage import median_filter


def my_stft(song, w="hann", win_len=2048, hop_size=128):
    # TODO: Too inefficient
    w = signal.get_window(w, win_len)
    short = np.zeros(shape=(4097, (len(song) - win_len) // hop_size), dtype=complex)
    for i in range(0, len(song) - win_len, hop_size):
        windowed = song[i:i + win_len] * w
        this = np.fft.rfft(windowed, n=8192)
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


def log_spec(spect, bins=128):
    # TODO: help, wont use this for now but will come back to it
    song_length = len(spect[0])
    H = 256
    N = 8192
    new_full = np.zeros(shape=(bins, song_length), dtype='complex')
    for frame in range(1, len(spect.T)):
        peaks, _ = signal.find_peaks(spect[:, frame])
        phases = (np.angle(get_phase(peaks, spect[:, frame]) - get_phase(peaks, spect[:, frame-1])-((peaks*H)/N)))/(np.pi*2)
        phases *= N/H
        for old, new in zip(peaks, phases):
            print(old, new)
            if old+new < 0 or freq_to_bucket(old+new) >= 128:
                break
            new_full[freq_to_bucket(old+new), frame] += spect[old, frame]
    return new_full


def get_phase(points, frame):
    return frame[points] - frame[points].real


def salience(spec):
    """
    Take log spec
    pick peaks
    remove lower peaks
    sum harms
    remove all lower value peaks
    """
    l_peaks = []
    for frame in range(len(spec.T)):
        peaks, spec[:, frame] = select_peaks(spec.T[frame], lambda x: np.max(x)/80)
        l_peaks.append(peaks)
        # harmonic_summation(spec[:, frame], peaks, [1, .5, .33, .25])
    return peaks, spec


def temp_function(spec):
    spec = refined_log_freq_spec(spec)
    spec[spec > np.max(spec)/80] = 0
    spec = maximum_filter(abs(spec), size=(1, 4))
    mask = median_filter(abs(spec), size=(1, 32))
    mask[mask > 0] = 1
    spec = spec * mask
    return spec


def harmonic_summation(frame, peaks, weights):
    for peak in peaks:
        harms = np.array(([peak+1]*4))
        harms *= np.array([2, 3, 4, 5])
        for harm, weight in zip(harms, weights):
            if harm < 4094:
                frame[peak] += frame[harm-1]*weight


def display(spec, text="STFT"):
    plt.pcolormesh(np.abs(spec))
    plt.colorbar()
    plt.title(text)
    plt.ylabel('Frequency ')
    plt.xlabel('Time ')
    plt.show()


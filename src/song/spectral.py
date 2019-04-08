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


def refined_log_freq_spec(spect, bins=128, nfft=8192):
    # TODO: This function breaks if freq_to_buckets cents is set to anything small as it tries to get negative index
    song_length = len(spect[0])
    new_full = np.zeros(shape=(bins, song_length))
    for index in range(1, len(spect)):
        if freq_to_bucket(index) >= 128:
            break
        new_full[freq_to_bucket(index)] += spect[index]
    return new_full


def log_spec(spect, bins=128, nfft=8192):
    # TODO: help, wont use this for now but will come back to it
    song_length = len(spect[0])
    new_full = np.zeros(shape=(bins, song_length))
    for frame in range(1, len(spect.T)):
        peaks, _ = signal.find_peaks(spect[:, frame])
        # phases = (np.angle(get_phase(peaks, spect[:, frame]) - get_phase(peaks, spect[:, frame-1])-((peaks*H)/N)))/(np.pi*2)
        # phases *= N/H
        for peak in peaks:
            if freq_to_bucket(peak, nfft) >= 128:
                break
            new_full[freq_to_bucket(peak, nfft), frame] += spect[peak, frame]
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
        peaks, spec[:, frame] = select_peaks(spec.T[frame])
        test = spec[:, frame]
        test[test > 0] = 1
        spec[:, frame] = test
        harmonic_summation(spec[:, frame], peaks, [2, 1, .5, .25], logged=logged)
    return spec


def temp_function(spec):
    spec = refined_log_freq_spec(spec)
    spec[spec > np.max(spec)/80] = 0
    spec = maximum_filter(abs(spec), size=(1, 4))
    mask = median_filter(abs(spec), size=(1, 32))
    mask[mask > 0] = 1
    spec = spec * mask
    return spec


def harmonic_summation(frame, peaks, weights, logged=True):
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
    # TODO: Allow this to take the last 8 notes it is missing at the top
    chroma = np.zeros(shape=(12, len(logspec[0])))
    for i in range(0, len(logspec), 12):
        try:
            chroma += logspec[i:i+12]
        except:
            chroma[0:8] += logspec[i:i+8]
    return chroma


def display(spec, text="STFT"):
    plt.pcolormesh(np.abs(spec))
    plt.colorbar()
    plt.title(text)
    plt.ylabel('Frequency ')
    plt.xlabel('Time ')
    plt.show()


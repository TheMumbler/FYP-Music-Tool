from math import floor, log2
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


def time_coef(frame, hop_size, sr):
    return (frame*hop_size)/sr


def freq_coef(ind, sr=44100, nfft=8192):
    return ind * (sr/nfft)


def mag_to_db(mag):
    # for i in range(len(mag)):
    #     mag[i] = 20 * np.log10(mag[i])
    return np.where(mag > 0, 20 * np.log10(mag), 0)


def midi_to_pitch(note, tuning=440):
    """Takes a midi number and returns the relative frequency. Has a tuning parameter with defaults to 440"""
    return (2 ** ((note - 69) / 12)) * tuning


def note_pitch_midi(tuning=440):
    """Creates a dictionary with has information on every note from C0 to B8 such as midi value and pitch value"""
    note_info = {}
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note_names = note_names * 10
    for midi_num, name in zip(range(12, len(note_names)), note_names):
        note_info[name + str((midi_num // 12) - 1)] = [midi_to_pitch(midi_num, tuning), midi_num]
    return note_info


def log_compression(spect, y=1):
    for i in range(len(spect[0])):
        spect[:, i] = np.log(spect[:, i] * y + 1)
    return spect


def bucket_size():
    # TODO: Maybe try remove this
    for i in np.arange(11.5, 108.5, 1):  # Maybe change 11.5 to zero?
        yield int(i+.5), midi_to_pitch(i), midi_to_pitch(i+1)


def log_freq_spec(spect):
    # TODO: Reduce complexity in this here pal
    song_length = len(spect[0])
    new_full = np.empty(shape=(109, song_length))
    for new_i, left, right in bucket_size():
        new = np.zeros(song_length)
        for index in range(len(spect)):
            if left < index < right:
                new = new + spect[index]
        new_full[new_i] = new
    return new_full


def freq_to_bucket(freq, cents=100, ref=8.66):
    freq = freq_coef(freq)
    return floor((1200/cents)*log2(freq/ref)+1.5)


def select_peaks(frame, threshold=np.mean, keep=False):
    """Takes a frame of stft and only keeps the peaks"""
    normal = np.abs(frame)
    # normal = smooth(normal)
    height = threshold(normal)
    peaks, _ = signal.find_peaks(normal, height)
    if not keep:
        mask = np.zeros_like(frame)
        for peak in peaks:
            mask[peak] = 1
        return peaks, frame * mask
    else:
        return peaks, frame


def magphase(spect, mag_only=False):
    if mag_only:
        return np.abs(spect), 0
    mag = np.abs(spect)
    phase = np.exp(1.j * np.angle(spect))
    return mag, phase


def harmonic_summ(arr):
    # TODO: This is not changing the output at all
    # TODO: IMPORTANT
    # TODO: Change to an inplace list mod
    for i in range(len(arr)-28):
        arr[i] += arr[i+12] + arr[i+19] + arr[i+24] + arr[i+28]
    return arr


def voicing(t, threshold=1):
    """Takes a column of stft and a volume threshold and will return any notes that are present"""
    if np.max(t) > 1000000:
        return np.argmax(t)
    else:
        return -1


def bin_offset(k, kval, kval2, N =8192, sr=44100, H=128):
    first = N/H
    second = np.angle(kval - kval2 - ((k*H)/N))/(np.pi*2)
    return k + (first*second)*(sr/N)


def phase_correct(spec, N=8192, H=128):
    first = N / (np.pi*H)
    for i in range(1, len(spec[0])-1):
        curr = spec[:, i]
        prev = spec[:, i-1].imag
        icurr = curr.imag
        principal = np.angle(icurr - prev - ((np.pi*H)/N)*curr)
        spec[:, i] += (first * principal)
        print("curr", curr)
        print(curr + (first * principal), "\n")
    return spec


def harmsumm(frame):
    for peak in range(len(frame)):
        try:
            frame[peak] += frame[peak + 12] + frame[peak + 19] + frame[peak + 24] + frame[peak + 28]
        except:
            pass
    return frame


def frame_to_time(frame, hop_size=256, sr=44100):
    return (frame*hop_size)/sr


def time_to_beats(time, bpm):
    beat = 60/bpm
    return time/beat


def smooth(x, window_len=11, window='hanning'):
    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window_len < 3:
        return x

    if window not in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s = np.r_[x[window_len - 1:0:-1], x, x[-2:-window_len - 1:-1]]
    # print(len(s))
    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.' + window + '(window_len)')

    y = np.convolve(w / w.sum(), s, mode='valid')
    return y[(window_len//2-1):-(window_len//2)]

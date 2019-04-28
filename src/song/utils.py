from math import floor, log2
import numpy as np
from scipy import signal


def time_coef(frame, hop_size, sr):
    """
    :param frame: the frame index in an STFT
    :param hop_size: the hop size used in creating the STFT
    :param sr: the sample rate of the input to the STFT
    :return: the time in seconds that the frame is referring to
    """
    return (frame*hop_size)/sr


def freq_coef(ind, sr=44100, nfft=8192):
    """
    Returns the correct frequency coefficient of a point in a fourier transform

    :param ind: the index in the fft
    :param sr: the sample rate
    :param nfft: the length of the fft
    :return: the frequency coefficient, will be between 0 and 22050 (Nyquist frequency)
    """
    return ind * (sr/nfft)


# def mag_to_db(mag):
#     # for i in range(len(mag)):
#     #     mag[i] = 20 * np.log10(mag[i])
#     return np.where(mag > 0, 20 * np.log10(mag), 0)


def midi_to_pitch(note, tuning=440):
    """
    Takes a midi number and returns the relative frequency. Has a tuning parameter with defaults to 440
    :param note: the frequency of the note
    :param tuning: the tuning of the note A4
    :return:
    """
    return (2 ** ((note - 69) / 12)) * tuning


def note_pitch_midi(tuning=440):
    """
    :param tuning: the tuning frequency of A4
    :return: a dictionary with has information on every note from C0 to B8 such as midi value and pitch value
    """
    note_info = {}
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note_names = note_names * 10
    for midi_num, name in zip(range(12, len(note_names)), note_names):
        note_info[name + str((midi_num // 12) - 1)] = [midi_to_pitch(midi_num, tuning), midi_num]
    return note_info


def log_compression(spect, y=1):
    """
    Returns a logarithmically compressed version of a spectrogram, allowing smaller energies to become more relevant
    :param spect: a magnitude spectrogram
    :param y: the higher the value of this variable the more relevant smaller energies will become
    :return: a logarithmically compressed version of a spectrogram
    """
    for i in range(len(spect[0])):
        spect[:, i] = np.log(spect[:, i] * y + 1)
    return spect


# def bucket_size():
#     # TODO: Maybe try remove this
#     for i in np.arange(11.5, 108.5, 1):  # Maybe change 11.5 to zero?
#         yield int(i+.5), midi_to_pitch(i), midi_to_pitch(i+1)
#
#
# def log_freq_spec(spect):
#     # TODO: Reduce complexity in this here pal
#     song_length = len(spect[0])
#     new_full = np.empty(shape=(109, song_length))
#     for new_i, left, right in bucket_size():
#         new = np.zeros(song_length)
#         for index in range(len(spect)):
#             if left < index < right:
#                 new = new + spect[index]
#         new_full[new_i] = new
#     return new_full


def freq_to_bucket(freq, cents=100, ref=8.66, nfft=8192, sr=44100):
    """
    Takes a frequency coefficient and a reference for the lowest bucket, default is C0, and returns the relative bucket
    in a log frequency spectrum. The size of each bucket is set by the number of cents. Default is 100, which is a
    semitone.
    :param freq: frequency coefficient
    :param cents: size of each bucket
    :param ref: the reference frequency for the lowest bucket in the log freq spectrum
    :return: the index of the correct bucket
    """
    freq = freq_coef(freq, sr=sr, nfft=nfft)
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
        return np.abs(spect), 1
    mag = np.abs(spect)
    phase = np.exp(1.j * np.angle(spect))
    return mag, phase


def time_to_beats(time, bpm):
    beat = 60/bpm
    return time/beat


def frame_to_beats(frame, hop_size, bpm, sr):
    time = time_coef(frame, hop_size, sr)
    beat = 60/bpm
    return time/beat


def beats_to_frames(beat, bpm, hop_size, sr):
    samples = 60/bpm * sr
    frames = samples / hop_size
    return floor(frames * beat)

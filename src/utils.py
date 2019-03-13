from math import floor, log2
import numpy as np


def midi_to_pitch(note, tuning=440):
    """Takes a midi number and returns the relative frequency. Has a tuning parameter with defaults to 440"""
    return (2 ** ((note - 69) / 12)) * tuning


def note_pitch_midi(tuning=440):
    """Creates a dictionary with has information on every note from C0 to B8 such as midi value and pitch value"""
    note_info = {}
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note_names = note_names * 10
    for midi_num, name in zip(range(12, len(note_names)), note_names):
        # print(name + str((i//12)-1), midi_to_pitch(i))
        # print(midi_num)
        note_info[name + str((midi_num // 12) - 1)] = [midi_to_pitch(midi_num, tuning), midi_num]
    return note_info


def log_compression(spect, y=1):
    for i in range(len(spect[0])):
        spect[:, i] = np.log(spect[:, i] * y + 1)
    return spect


def bucket_size():
    # TODO: Maybe try remove this
    for i in np.arange(11.5, 108.5, 1):  # Maybe change 11.5 to zero?
        # print(midi_to_pitch(i+.5))
        # print(i+.5)
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


def freq_to_bucket(freq, cents=100):
    return floor((1200/cents)*log2(freq/440)+69.5)


def refined_log_freq_spec(spect):
    # TODO: This function breaks if freq_to_buckets cents is set to anything small as it tries to get negative index
    song_length = len(spect[0])
    freq_range = len(spect)
    # print(spect.shape)
    new_full = np.zeros(shape=(freq_to_bucket(freq_range-1), song_length))
    # print(new_full.shape)
    for index in range(1, len(spect)):
        new_full[freq_to_bucket(index)-1] = new_full[freq_to_bucket(index)-1] + spect[index]
        # print(freq_to_bucket(index))
    return new_full


def harmonic_summ(arr):
    # TODO: This is not changing the output at all
    arr= abs(arr)
    # arr = arr[::-1]
    for i in range(1, len(arr)+1):
        if (i+1)*2 < len(arr):
            arr[i-1] += arr[(i+1)*2]
            if (i+1)*3 < len(arr):
                arr[i-1] += arr[(i+1)*3]
                if (i+1)*4 < len(arr):
                    arr[i-1] += arr[(i+1)*4]
                    if (i+1)*5 < len(arr):
                        arr[i-1] += arr[(i+1)*5]
    arr = arr[::-1]
    return arr



def my_stft(song):
    # TODO: Tidy this up
    win_len = 2048
    w = scipy.signal.get_window("hann", win_len)
    hop_size = 128
    short = np.zeros(shape=(4096, (len(song) - win_len) // 128))
    totes = np.ones(shape=w.shape)

    for i in range(0, len(song) - win_len, 128):
        # TODO: Fix the normalisation peak picking
        # TODO: Threshold here is currently just average, find a better solution
        windowed = song[i:i + win_len] * w
        this = np.fft.fft(windowed, n=8192)
        # totes += np.sum(windowed)
        # plt.plot(test)
        # plt.show()
        # print(i//128)
        this = np.abs(this[:len(this) // 2])
        med = np.max(this) / 2
        # print("med", med)
        # plt.plot([med]*len(this))
        # plt.plot(this)
        # plt.show()

        # this = 2*(this/totes)
        # this[this < (np.average(this)*50)] = 0   This worked decently for the piano pieces
        this[this < med] = 0
        short[:, (i // 128) - 1] = this
    return song


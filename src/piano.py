from .song import read
from .song import spectral, structure
from .song import utils
from .song import decomp
from scipy import signal
from scipy.ndimage import median_filter
from scipy.ndimage import maximum_filter
from .song import midi_tools
from librosa.beat import tempo
import numpy as np
from zipfile import ZipFile
import os
from .song.spectral import octave_weak, non_zero_average_std

# print("done importing")
#
#
# print("reading file")
# # sr, song = read.read('../Songs/fur_elise.wav')
# sr, song = read.read('../Songs/river_flows_in_you.wav')
# # sr, song = read.read('../Songs/deadmau5.wav')
# # sr, song = read.read('../Songs/crab.wav')
# # sr, song = read.read('../Songs/billie.wav')
# # sr, song = read.read('../Songs/hungarian.wav')
# song = song*1.0
#
#
# weights = [1.0, 0.5, 0.33, 0.25]
#


# _, _, x = signal.stft(song, nperseg=2048, nfft=8192, noverlap=1792)
#
# x, _ = utils.magphase(x, mag_only=True)

#

def piano_ver1(song, name, user, bpm=None, sections=False, **kwargs):
    # current peak pick for log_spec
    # avg = uniform_filter1d(abs(spect[:, frame]), 100)
    # peaks, _ = signal.find_peaks(abs(spect[:, frame]), height=avg, prominence=5)

    sr, song = read.read(song)
    song = read.startend(song)
    song = song * 1.0

    if not bpm:
        bpm = tempo(song, sr=sr)[0]

    if sections:
        sections = structure.find_segments(song, bpm)

    else:
        sections = []

    sections = [0] + sections + [None]
    i = 0
    for start, end in zip(sections[:-1], sections[1:]):
        section = song[start:end]
        _, _, x = signal.stft(section, nperseg=2048, nfft=8192, noverlap=1536)
        # x, _ = utils.magphase(x, mag_only=True)
        x = np.abs(x)
        log = spectral.log_spec(x, sr=sr)
        log = spectral.salience(log)

        for frame in range(len(log.T)):
            f = log[:, frame]
            avg, sd = non_zero_average_std(f)
            octave_weak(f)
            f[f < avg] = 0
            # avg, sd = non_zero_average_std(f)
            # f[f < avg/2] = 0
            log[:, frame] = f

        mask = median_filter(abs(log), size=(1, 24))
        mask[mask > 0] = 1
        log = mask * log
        log = maximum_filter(abs(log), size=(1, 4))
        log = median_filter(abs(log), size=(1, 8))

        notes = midi_tools.get_notes(log)
        midi_tools.output_midi("piano"+str(i), notes, bpm, sr, hopsize=512, directory=user)


        i += 1


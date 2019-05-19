from .song import read
from scipy import signal
import numpy as np
import os
from .song import decomp
from scipy.io import wavfile


def harmpercsplit(song, name, user, bpm=None, sections=False, **kwargs):
    sr, song = read.read(song)
    song = read.startend(song)
    song = song * 1.0
    _, _, x = signal.stft(song, nperseg=2048, nfft=8192)
    h, p = decomp.hpss(x, pow=2)

    _, reconstructedH = signal.istft(h, sr, nperseg=2048, nfft=8192)
    _, reconstructedP = signal.istft(p, sr, nperseg=2048, nfft=8192)

    rounded_reconstructedH = np.rint(reconstructedH).astype(np.int16)
    rounded_reconstructedP = np.rint(reconstructedP).astype(np.int16)

    harm = os.path.join(user, 'harmonic.wav')
    perc = os.path.join(user, 'percussion.wav')
    wavfile.write(harm, sr, rounded_reconstructedH)
    wavfile.write(perc, sr, rounded_reconstructedP)

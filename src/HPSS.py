import numpy as np
from scipy.ndimage import median_filter
import scipy.io.wavfile
from scipy import signal
import matplotlib.pyplot as plt
from utils import *


def magphase(D, power=1):
    mag = np.abs(D)
    mag **= power
    phase = np.exp(1.j * np.angle(D))

    return mag, phase


def hpss(S):
    """Split the wave into harmonic and percussive"""
    if np.iscomplexobj(S):
        S, phase = magphase(S)
    else:
        phase = 1

    power = 2
    harm = np.empty_like(S)
    harm[:] = median_filter(S, size=(1, 32))
    perc = np.empty_like(S)
    perc[:] = median_filter(S, size=(32, 1))
    # mask_harm = (harm ** power)/ (harm**power + perc**power)
    # mask_perc = (perc ** power)/ (perc**power + harm**power)
    return (S * harm) * phase, (S * perc) * phase

# `M = X**power / (X**power + X_ref**power)`

sr, song = scipy.io.wavfile.read('../Songs/into.wav')
song = song[:5*sr]

_, _, s = signal.stft(song, fs=sr, nperseg=2048, nfft=8192)

# s = refined_log_freq_spec(s)

h, p = hpss(s)

plt.pcolormesh(abs(s))
plt.title('Refined Logged')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()


plt.pcolormesh(abs(p))
plt.title('perc')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

plt.pcolormesh(abs(h))
plt.title('harmonic')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

_, h = scipy.signal.istft(h, fs=sr)
_, p = scipy.signal.istft(p, fs=sr)
print(h)
h = np.asarray(h, dtype=np.int16)
p = np.asarray(p, dtype=np.int16)
scipy.io.wavfile.write('harm.wav', sr, h)
scipy.io.wavfile.write('perc.wav', sr, p)
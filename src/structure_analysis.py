from scipy import signal
from song import read
from song import spectral
from song import structure
from scipy.spatial.distance import cdist
import numpy as np
from scipy.ndimage import median_filter
from song import beat
from scipy.ndimage import maximum_filter
from scipy.ndimage import rotate
from song import midi_tools
from librosa.feature import chroma_stft

# sr, song = read.read('../Songs/fur_elise.wav')
# sr, song = read.read('../Songs/deadmau5.wav')
sr, song = read.read('../Songs/hungarian.wav')
# sr, song = read.read('../Songs/crab.wav')
song = song * 1.0


# B=5
_, _, x = signal.stft(song, nperseg=8192, nfft=8192)  # 1792/1920
x = abs(x)

x = spectral.log_spec(x)

x = spectral.chromagram(x)
# x = chroma_stft(song, sr=sr, n_fft=2048, hop_length=512)


dist = cdist(x.T, x.T, metric='cosine')
dist = 1 - dist
dist[np.isnan(dist)] = 0

footie = np.zeros(shape=(100, 100))
np.fill_diagonal(footie, 1)

spectral.display(dist)

mask = median_filter(abs(dist), footprint=footie)
mask[mask < .9] = 0
mask[mask > 0] = 1
dist = dist*mask


spectral.display(dist)


l = structure.sim_to_lag(dist)
l = median_filter(abs(l), size=(1, 180))
spectral.display(l)

energy = np.zeros(shape=len(l))
for frame in range(0, len(l)-1):
    energy[frame] = np.linalg.norm(l[:, frame+1]) - np.linalg.norm(l[:, frame])

import matplotlib.pyplot as plt
# plt.plot(abs(energy))
# plt.show()

peaks, _ = signal.find_peaks(abs(energy), height=np.mean(energy), distance=150)

# plt.pcolormesh(l)
# for xc in peaks:
#     plt.axvline(x=xc)
#
# plt.show()
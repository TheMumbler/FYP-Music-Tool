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

# sr, song = read.read('../Songs/fur_elise.wav')
# sr, song = read.read('../Songs/deadmau5.wav')
sr, song = read.read('../Songs/hungarian.wav')
# sr, song = read.read('../Songs/crab.wav')
song = read.startend(song)

# song = song[:8192*250*sr]

# B=5
# X=np.random.rand(B*B).reshape((B,B))
_, _, x = signal.stft(song, nperseg=8192, nfft=8192)  # 1792/1920
x = abs(x)
# x = x[:, :-250]

x = spectral.log_spec(x)

# for frame in range(len(x.T)):
#     peaks, x[:, frame] = utils.select_peaks(x.T[frame])

x = spectral.chromagram(x)
# x = utils.log_compression(x)
# spectral.display(x)

dist = cdist(x.T, x.T, metric='cosine')
# dist = dist/np.max(dist)
dist = 1 - dist
dist[np.isnan(dist)] = 0
# dist = np.triu(dist)

footie = np.zeros(shape=(100, 100))
np.fill_diagonal(footie, 1)
#
spectral.display(dist)
#
mask = median_filter(abs(dist), footprint=footie)
mask[mask < .9] = 0
mask[mask > 0] = 1
dist = dist*mask


# dist = cdist(x.T, x.T, metric='euclidean')
# dist = 1-(dist/np.max(dist))
# dist = rotate(dist, 45)
spectral.display(dist)
# K = np.exp(dist)
# ro = (rotate(dist, 45))[:len(dist)/2]

l = structure.sim_to_lag(dist)
l = median_filter(abs(l), size=(1, 180))
spectral.display(l)

energy = np.zeros(shape=len(l))
for frame in range(0, len(l)-1):
    energy[frame] = np.linalg.norm(l[:, frame+1]) - np.linalg.norm(l[:, frame])

import matplotlib.pyplot as plt
plt.plot(abs(energy))
plt.show()

peaks, _ = signal.find_peaks(abs(energy), height=np.mean(energy), distance=150)

plt.pcolormesh(l)
for xc in peaks:
    plt.axvline(x=xc)

plt.show()
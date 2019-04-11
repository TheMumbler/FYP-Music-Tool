from scipy import signal
from song import read
from song import spectral
from song import utils
from scipy.spatial.distance import cdist
import numpy as np
from scipy.ndimage import median_filter
from scipy.ndimage import maximum_filter
from scipy.ndimage import rotate
from song import midi_tools
from librosa.segment import recurrence_to_lag

sr, song = read.read('../Songs/fur_elise.wav')
# sr, song = read.read('../Songs/deadmau5.wav')
# sr, song = read.read('../Songs/hungarian.wav')
song = read.startend(song)
# sr, song = read.read('../Songs/crab.wav')

# song = song[:sr*5]

# B=5
# X=np.random.rand(B*B).reshape((B,B))
_, _, x = signal.stft(song, nperseg=8192, nfft=8192)  # 1792/1920
x = abs(x)

x = spectral.refined_log_freq_spec(x)

# for frame in range(len(x.T)):
#     peaks, x[:, frame] = utils.select_peaks(x.T[frame])

# x = spectral.chromagram(x)
# x = utils.log_compression(x)
# spectral.display(x)

dist = cdist(x.T, x.T, metric='cosine')
dist = 1 - dist
dist[np.isnan(dist)] = 0
# dist = np.triu(dist)

footie = np.zeros(shape=(100, 100))
np.fill_diagonal(footie, 1)
#
#
mask = median_filter(abs(dist), footprint=footie)
mask[mask < .7] = 0
mask[mask > 0] = 1
dist = dist*mask


# dist = cdist(x.T, x.T, metric='euclidean')
# dist = 1-(dist/np.max(dist))
# dist = median_filter(abs(dist), size=(2000, 1))
# dist = rotate(dist, 45)
spectral.display(dist)
# K = np.exp(dist)
# ro = (rotate(dist, 45))[:len(dist)/2]






l = sim_to_lag(dist)
spectral.display(l)

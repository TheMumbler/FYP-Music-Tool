from scipy import signal
from song import read
from song import spectral
from song import utils
from scipy.spatial.distance import cdist
import numpy as np

# sr, song = read.read('../Songs/fur_elise.wav')
# sr, song = read.read('../Songs/deadmau5.wav')
sr, song = read.read('../Songs/crab.wav')

# song = song[:sr*5]
nfft=8192*2
# B=5
# X=np.random.rand(B*B).reshape((B,B))
_, _, x = signal.stft(song, nperseg=nfft, nfft=nfft)  # 1792/1920
x = abs(x)

x = spectral.refined_log_freq_spec(x)
x = spectral.chromagram(x)
# x = utils.log_compression(x)
# spectral.display(x)


# dist = cdist(x.T, x.T, metric='cosine')
# dist = 1 - dist

dist = cdist(x.T, x.T, metric='euclidean')
dist = 1- (dist/np.max(dist))
spectral.display(dist)
# K = np.exp(dist)



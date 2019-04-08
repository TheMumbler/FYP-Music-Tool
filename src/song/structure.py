from scipy import spatial
from scipy.spatial.distance import cdist
from . import spectral
import numpy as np
# dataSetI = [3, 45, 7, 2]
# dataSetII = [2, 54, 13, 15]
# result = 1 - spatial.distance.cosine(dataSetI, dataSetII)


def chroma_structure(x):
    """
    Creates a self-similarity matrix from a spectrogram for collecting information on the chroma structure
    :param x: a spectrogram representing a song
    :return: an n*n similarity matrix where n is the number of frames in spectrogram
    """
    x = abs(x.copy())
    x = spectral.refined_log_freq_spec(x)
    dist = cdist(x.T, x.T, metric='cosine')
    dist = 1 - (dist / np.max(dist))
    return dist


def harmonic_structure(x):
    # TODO: finish this, might need mffc function
    x = abs(x.copy())
    x = spectral.refined_log_freq_spec(x)
    x = spectral.chromagram(x)
    dist = cdist(x.T, x.T, metric='cosine')
    dist = 1 - (dist / np.max(dist))
    return dist

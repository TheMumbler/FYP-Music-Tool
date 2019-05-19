import numpy as np
from scipy.ndimage import median_filter
from .utils import magphase


def hpss(spec, pow=1, soft=True, ksize=32):
    """Split the wave into harmonic and percussive"""
    if np.iscomplexobj(spec):
        spec, phase = magphase(spec)
    else:
        phase = 1
    harm = np.empty_like(spec)
    perc = np.empty_like(spec)
    eps = .1
    harm[:] = median_filter(spec, size=(1, ksize))
    perc[:] = median_filter(spec, size=(ksize, 1))
    if soft:
        mask_h = (((harm + eps)/2)**pow)/((harm + perc + eps)**pow)
        mask_p = (((perc + eps)/2)**pow)/((harm + perc + eps)**pow)
    else:
        mask_h = (harm >= perc).astype(int)
        mask_p = (perc > harm).astype(int)
    return mask_h * spec * phase, mask_p * spec * phase


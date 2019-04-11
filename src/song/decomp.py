import numpy as np
from scipy.ndimage import median_filter
from .utils import magphase


def hpss(spec):
    """Split the wave into harmonic and percussive"""
    # TODO: Add option of binary masking instead of soft masking
    if np.iscomplexobj(spec):
        spec, phase = magphase(spec)
    else:
        phase = 1
    harm = np.empty_like(spec)
    perc = np.empty_like(spec)
    eps = .1
    harm[:] = median_filter(spec, size=(1, 128))
    perc[:] = median_filter(spec, size=(128, 1))
    mask_h = (((harm + eps)/2)*2)/((harm + perc + eps)*2)
    mask_p = (((perc + eps)/2)*2)/((harm + perc + eps)*2)
    return mask_h * spec * phase, mask_p * spec * phase


"""
Read in song
Perform STFT
Log the magnitude to increase importance of lower notes
Bin frequency coefs into midi notes
Perform harmonic summation
Remove notes that are below a certain threshold
Track remaining bins using a voicing function
Tidy up final product with removing notes that show up very quickly then go away (inaccuracies)
Convert final product into midi file
"""

# Read in song
import scipy.io.wavfile
from utils import *
from math import log10
import numpy as np

# sr, song = scipy.io.wavfile.read('../Songs/fur_elise.wav')
sr, song = scipy.io.wavfile.read('../Songs/river_flows_in_you_mono.wav')
# sr, song = scipy.io.wavfile.read('../Songs/deadmau5.wav')
# sr, song = scipy.io.wavfile.read('../Songs/sin.wav')

# We will just take the 1st 5 secs
song = song[:sr*5]

# Peform STFT

spec = my_stft(song)
display(spec)
peaks = []
for i in range(len(spec.T)):
    peak, spec[:, i] = select_peaks(spec[:, i])
    peaks.append(peak)


display(spec)

spec = refined_log_freq_spec(spec)

display(spec)


for i in range(len(spec.T)):
    tes = spec[:, i]
    tes = np.where(20*np.log10(np.max(tes)/tes) < 80, tes, 0)
    spec[:, i] = tes

display(spec)


for i in range(len(spec.T)):
    spec[:, i] = harmsumm(spec[:, i], peaks[i])

display(spec)




# x = mag_to_db(abs(spec))
# for i in range(len(x[0])):
#     tes = x[:, i]
#     tes[tes != np.max(tes)] = 0
#     x[:, i] = tes
# display(x)


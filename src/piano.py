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

sr, song = scipy.io.wavfile.read('../Songs/fur_elise.wav')
# sr, song = scipy.io.wavfile.read('../Songs/sin.wav')

# We will just take the 1st 5 secs
song = song[:sr*5]

# Peform STFT

spec = my_stft(song)
display(spec)
clean = spec.copy()

clean = phase_correct(spec)
display(clean)



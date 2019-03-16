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

# sr, song = scipy.io.wavfile.read('../Songs/fur_elise.wav')
sr, song = scipy.io.wavfile.read('../Songs/sin.wav')

# We will just take the 1st 5 secs
song = song[:sr*5]

# Peform STFT

spec = my_stft(song)

# display(spec, "pre-compression")

# Log the magnitude to increase importance of lower notes

# log1 = log_compression(spec)
# display(log1, "1")

# log2 = log_compression(spec, 10)
# display(log2, "10")

# log3 = log_compression(spec, 100)
# display(log3, "100")




# magdb[magdb < 400] = 0
m, p = magphase(spec)

display(abs(spec))
magdb = mag_to_db(m)
# magdb = m
peaks, _ = signal.find_peaks(np.abs(magdb[:, 200]), height=50)
# magdb = refined_log_freq_spec(magdb)
# magdb = harmonic_summ(magdb)
display(magdb, "magdb")


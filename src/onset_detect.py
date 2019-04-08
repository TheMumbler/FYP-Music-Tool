from song import beat
from song import read
import matplotlib.pyplot as plt
import numpy as np
from song import spectral
from time import sleep
from scipy import signal

# from librosa.feature import rms
# sr, song = read.read('../Songs/river_flows_in_you.wav')
sr, song = read.read('../Songs/fur_elise.wav')
# song = song * 1.0
# t = rms(y=song[:sr*3])
# x = beat.half_w_rect(song[:sr * 3])
song = song[:sr*5]
y = beat.spec_novelty(song)

# ave = beat.moving_average(abs(y[:-0]), 100)
y = y[:-50]
y = abs(y)
p, _ = signal.find_peaks(y)
print(p)
plt.plot(y)
# plt.plot(ave)

plt.show()

# print(beat.get_onsets(song))
# plt.plot(t)
from song import beat
from song import read
import matplotlib.pyplot as plt
import numpy as np
from song import spectral
from time import sleep

# from librosa.feature import rms
# sr, song = read.read('../Songs/river_flows_in_you.wav')
sr, song = read.read('../Songs/fur_elise.wav')
# song = song * 1.0
# t = rms(y=song[:sr*3])
# x = beat.half_w_rect(song[:sr * 3])
song = song[:sr*5]
y = beat.spec_novelty(song)

# ave = beat.moving_average(abs(y[:-41]), 10)
# y = y[:-50]
y = abs(y)

plt.plot(y)

plt.show()

spectral.display(x)
# print(beat.get_onsets(song))
# plt.plot(t)
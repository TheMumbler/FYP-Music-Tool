from song import beat
from song import read
import matplotlib.pyplot as plt
from time import sleep

# from librosa.feature import rms
# sr, song = read.read('../Songs/river_flows_in_you.wav')
sr, song = read.read('../Songs/fur_elise.wav')
# song = song * 1.0
# t = rms(y=song[:sr*3])
# x = beat.half_w_rect(song[:sr * 3])
song = song[:sr*5]
y = beat.spec_novelty(song)
z = beat.e_novelty(song[:sr*3])
# plt.plot(x)
plt.plot(abs(y[:-50]))
plt.show()

plt.plot(abs(z[:-50]))
plt.show()

plt.plot(song)
# sleep(1)
# plt.plot(song[:-50*512])
# plt.show()

# plt.plot(t)
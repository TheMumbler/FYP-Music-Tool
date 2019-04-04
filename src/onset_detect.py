from song import onset, read
import matplotlib.pyplot as plt
from librosa.feature import rms
# sr, song = read.read('../Songs/river_flows_in_you.wav')
sr, song = read.read('../Songs/fur_elise.wav')
song = song * 1.0
t = rms(y=song[:sr*3])
x = onset.half_w_rect(song[:sr*3])
y = onset.e_novelty(song[:sr*5])
# z = onset.log_e_novelty(song[:sr*3])
# plt.plot(x)
plt.plot(y)
# plt.plot(song[:sr*5])
plt.show()
plt.plot(t)
plt.show()

from song import onset, read
import matplotlib.pyplot as plt

# sr, song = read.read('../Songs/river_flows_in_you.wav')
sr, song = read.read('../Songs/fur_elise.wav')

x = onset.half_w_rect(song[:sr*3])
y = onset.e_novelty(song[:sr*10])
# z = onset.log_e_novelty(song[:sr*3])
# plt.plot(x)
plt.plot(y)
plt.plot(song[:sr*3])
plt.show()

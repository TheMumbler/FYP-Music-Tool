from scipy import signal
import matplotlib.pyplot as plt
import scipy.io.wavfile
import numpy as np
from utils import log_freq_spec, refined_log_freq_spec
from math import log


# sr, song = scipy.io.wavfile.read('../Songs/river_flows_in_you_mono.wav')
# sr, song = scipy.io.wavfile.read('../Songs/fur_elise.wav')
sr, song = scipy.io.wavfile.read('../Songs/Deadmau5 - Strobe (Evan Duffy Piano Cover).wav')
song = song[15*sr:40*sr]
plt.plot(song)
plt.show()

# # take first ten seconds  ## THIS WAS A PLAYGROUND FOR LOOKING AT DIFFERENT WINDOWS
# song = song[sr:10*sr]
#
# plt.plot(song)
# plt.show()
# hop = 1024
# sample = song[hop*4:hop*5]
# plt.plot(sample)
# plt.show()
#
# window = scipy.signal.windows.hann(hop)
# sample = window * sample
# plt.plot(sample)
# plt.title('After window applied')
# plt.show()
# # x = np.fft.fft(sample)
# length = int(len(song)//hop)
# print(length)
# peaks = np.zeros(length)
# j = 0
# for i in range(25*hop, len(song), hop):
#     sample = song[i:i+hop]
#     if len(sample) == hop:
#         sample = sample * window
#         x = np.fft.fft(sample)
#         plt.plot(abs(x))
#         plt.show()
#         x_peaks = signal.find_peaks(x[:int(len(x)//2)], height =60000)
#         print(x_peaks)
#         # print(np.argmax(x))
#         # peaks[j] = np.argmax(x)
#     j += 1
#     break
#
# # plt.plot(l)
# # print(np.argmax(x))
# print(peaks)
# print(len(peaks))
# # plt.show()

print(len(song)/128)
print(len(song)/sr)
# 128 is each hop , 8192 is how many freq bins there is
f, t, Zxx = signal.stft(song, fs=sr, nperseg=2048, nfft=8192)
# f, t, Zxx = signal.stf
print(len(Zxx))


new_f = log_freq_spec(Zxx)
new_ref = refined_log_freq_spec(Zxx)
#
# # plt.pcolormesh(t, f, np.log(np.abs(Zxx)), vmin=1)
plt.pcolormesh(np.abs(new_f))
plt.title('Logged')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
#
plt.pcolormesh(np.abs(new_ref))
plt.title('Refined Logged')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()


plt.pcolormesh(np.abs(Zxx))
plt.title('STFT Magnitude')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

# d = note_pitch_midi()
# for key in d:
#     print(key, d[key])

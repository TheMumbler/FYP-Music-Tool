from scipy import signal
import matplotlib.pyplot as plt
import scipy.io.wavfile
import numpy as np
from utils import *
from math import log


# sr, song = scipy.io.wavfile.read('../Songs/river_flows_in_you_mono.wav')
# sr, song = scipy.io.wavfile.read('../Songs/fur_elise.wav')
# sr, song = scipy.io.wavfile.read('../Songs/deadmau5.wav')
# sr, song = scipy.io.wavfile.read('../Songs/into.wav')
sr, song = scipy.io.wavfile.read('../Songs/sin.wav')
songmax = np.max(song)
song = song[:5*sr]
# plt.plot(song)
# plt.show()


print(len(song)/128)
print(len(song)/sr)
# 128 is each hop , 8192 is how many freq bins there is
f, t, Zxx = signal.stft(song, fs=sr, nperseg=2048, nfft=8192)


# TODO: Move this a into my_stft function
win_len = 2048
w = scipy.signal.get_window("hann", win_len)
hop_size = 128
short = np.zeros(shape=(4096, (len(song)-win_len)//hop_size))
totes = 0
thresh = np.zeros(shape=(8192,))
for i in range(0, len(song)-win_len, hop_size):
    # TODO: Fix the normalisation peak picking
    # TODO: Threshold here is currently just average, find a better solution
    windowed = song[i:i+win_len]*w
    this = np.fft.fft(windowed, n=8192)
    this = np.abs(this[:len(this)//2])

    # print(i//128)
    # this = 2*(this/totes)
    # this[this < (np.average(this)*50)] = 0 #   This worked decently for the piano pieces
    short[:, (i//hop_size)-1] = this
print(np.argmax(short))

#normalised ??
# short = 2*(short/totes)
# This is the peak picking for
print(short.shape)



# short = log_compression(short)
# l = np.array(l)
print("SAMPLE RATE: ", sr)
# Parabolic interpolation


def parabolic_ip(freq):
    # TODO : Fix this, too slow. Look at book again
    for p in range(1, len(freq)-1):
        if freq[p - 1] > 0 and freq[p] > 0 and freq[p+1] > 0:
            a1 = 20*log(freq[p-1], 10)
            a2 = 20*log(freq[p], 10)
            a3 = 20*log(freq[p+1], 10)
            print(a1, a2, a3)
            d = .5*((a1-a3)/(a1-(2*a2)+a3))
            print(d)
            freq[i] = a2 - (d/4)*(a1-a3)
    return freq
# print(len(short[:, 1]))
# parabolic_ip(abs(short[:, 1]))


# for i in range(len(short[0])):
#     parabolic_ip(abs(short[:, 1]))
#

print("Window size in ms: ", (win_len/sr)*1000)
# f, t, Zxx = signal.stf
print(len(Zxx[0]), "Length of STFT")

# Zxx = log_compression(Zxx)
# print(Zxx[0])
peaks = refined_log_freq_spec(Zxx)
# for i in range(len(Zxx[0])):
#     test = np.sum((song[i:i+len(w)])*w)
#     # Zxx[:, i] = np.log(Zxx[:, i] * y + 1)
#     peaks[:, i] = 2*(np.abs(Zxx[:, i])/test)

# new_f = log_freq_spec(Zxx)
new_ref = refined_log_freq_spec(short)

for j in range(len(new_ref[0])):
    new_ref[:, j] = harmonic_summ(new_ref[:, j])
# new_ref = log_compression(new_ref)

# # plt.pcolormesh(t, f, np.log(np.abs(Zxx)), vmin=1)
# plt.pcolormesh(np.abs(new_f))
# plt.title('Logged')
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Time [sec]')
# plt.show()
# # this[this < (np.average(this)*50)]
new = mag_to_db(new_ref)
new[new < (np.max(new)-20)] = 0

plt.pcolormesh(np.abs(new_ref))
plt.colorbar()
plt.title('Refined Logged')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
Zxx = refined_log_freq_spec(Zxx)
# for line in new_ref.T:
#     print(voicing(line))
plt.pcolormesh(np.abs(short))
plt.colorbar()
plt.title('MY BOY')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

#
plt.pcolormesh(np.abs(Zxx))
plt.colorbar()
plt.title('STFT Magnitude')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
# #
# plt.pcolormesh(np.abs(peaks))
# plt.title('PEAKS')
# plt.colorbar()
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Time [sec]')
# plt.show()
# d = note_pitch_midi()
# for key in d:
#     print(key, d[key])
print(new.shape)
plt.pcolormesh(np.abs(new))
plt.title('new test')
plt.colorbar()
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

# plt.pcolormesh(np.abs(new_ref))
# plt.colorbar()
# plt.title('Refined Logged')
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Time [sec]')
# plt.show()
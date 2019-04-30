from song import read
from song import spectral
from song import utils
from song import decomp
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import median_filter
from scipy.ndimage import maximum_filter
from scipy.ndimage import minimum_filter
from song import midi_tools
from librosa.beat import tempo
from librosa.onset import onset_detect
print("done importing")


print("reading file")
sr, song = read.read('../Songs/fur_elise.wav')
# sr, song = read.read('../Songs/river_flows_in_you.wav')
# sr, song = read.read('../Songs/deadmau5.wav')
# sr, song = read.read('../Songs/crab.wav')
song = read.startend(song)
# sr, song = read.read('../Songs/billie.wav')
# sr, song = read.read('../Songs/hungarian.wav')
song = song*1.0

print(sr)

bpm = tempo(song, sr=sr) # [0]
# bpm = 130
print("found bpm")
weights = [1.0, 0.5, 0.33, 0.25]
# song = song[:sr*5]
# song = song[sr*43:sr*180]
print(sr)
# onsets = onset_detect(song, hop_length=256, units='frames')
# plt.plot(song)
# onsets *= 256
# for onset in onsets:
#     plt.axvline(x=onset)
# plt.show()


def non_zero_average_std(arr):
    nonz = np.nonzero(arr)[0]
    if nonz.any():
        return np.mean(arr[nonz]), np.std(arr[nonz])
    else:
        return 0, 0


def octave_weak(frame):
    for f in range(len(frame)-12):
        if frame[f] > 0:
            frame[f+12] *= 1/frame[f]


_, _, x = signal.stft(song, nperseg=2048, nfft=8192, noverlap=1536)  # , noverlap=1792)  # 1792/1920

# x, _ = decomp.hpss(x, 2, ksize=16)
x = abs(x)
# x, _ = utils.magphase(x, mag_only=True)

log = spectral.log_spec(x.copy())
# log = spectral.refined_log_freq_spec(x.copy())
# log = utils.log_compression(log, 1000)
# onsets /= 256
# spectral.display(log)



log = spectral.salience(log)
# spectral.display(log)

# spectral.display(log)
# mask = median_filter(abs(log), size=(1, 48))
# mask[mask > 0] = 1
# log = mask * log
# #
#

# log = median_filter(abs(log), size=(1, 32))

for frame in range(len(log.T)):
    f = log[:, frame]
    avg, sd = non_zero_average_std(f)
    f[f < avg] = 0
    octave_weak(f)
    avg, sd = non_zero_average_std(f)
    f[f < avg/2] = 0
    log[:, frame] = f

# log = utils.log_compression(log, 1000)

# spectral.display(log)
# exit()

# exit()

# spectral.display(log)




# avg, sd = non_zero_average_std(log)
# log[log < avg] = 0

# np.mean()
# mask[mask > 0] = 1
# log = mask * log





# log[log < 1] = 0


mask = median_filter(abs(log), size=(1, 16))
mask[mask > 0] = 1
log = mask * log
log = maximum_filter(abs(log), size=(1, 4))
log = median_filter(abs(log), size=(1, 8))

# spectral.display(log)


#
notes = midi_tools.get_notes(log)
midi_tools.output_midi("crab512halfHpss", notes, bpm, sr, hopsize=512)

# mask[mask < np.max(mask)/20] = 0
# mask[mask > 0] = 1
# log = mask * log
# log[log > 0] = 1
# for onset in onsets:
#     plt.axvline(x=onset)
# log = utils.log_compression(log,1000)
# spectral.display(log)


from song import read
from song import spectral
from song import utils
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
# sr, song = read.read('../Songs/fur_elise.wav')
# sr, song = read.read('../Songs/river_flows_in_you_mono.wav')
sr, song = read.read('../Songs/deadmau5.wav')
# sr, song = read.read('../Songs/walker.wav')
song = song*1.0


bpm = tempo(song, sr=sr)[0]
weights = [1.0, 0.5, 0.33, 0.25]
# song = song[:sr*5]
song = song[sr*45:sr*90]


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



_, _, x = signal.stft(song, nperseg=2048, nfft=8192, noverlap=1792)  # 1792/1920

# x = abs(x)
x, _ = utils.magphase(x)

x = spectral.log_spec(x)
spectral.display(x)
log = spectral.salience(x)
log = utils.log_compression(x)

mask = median_filter(abs(log), size=(1, 48))
# mask[mask > 0] = 1
# log = mask * log
# #
#
for frame in range(len(log.T)):
    f = log[:, frame]
    octave_weak(f)
    avg, sd = non_zero_average_std(f)
    f[f < avg+sd] = 0
    log[:, frame] = f







# avg, sd = non_zero_average_std(log)
# log[log < avg] = 0

# np.mean()
# mask[mask > 0] = 1
# log = mask * log





# log[log < 1] = 0


mask = median_filter(abs(log), size=(1, 32))
mask[mask > 0] = 1
log = mask * log
log = maximum_filter(abs(log), size=(1, 8))
log = median_filter(abs(log), size=(1, 16))


notes = midi_tools.get_notes(log)
midi_tools.output_midi("dd", notes, bpm, sr)

# mask[mask < np.max(mask)/20] = 0
# mask[mask > 0] = 1
# log = mask * log
# log[log > 0] = 1
spectral.display(log)


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
from midiutil import MIDIFile

print("done importing")


sr, song = read.read('../Songs/fur_elise.wav')
print("reading file")
# sr, song = read.read('../Songs/river_flows_in_you.wav')
song = song/1.0
print("finding bpm")
bpm = tempo(song, sr=sr)[0]
# freqs= librosa.fft_frequencies(sr=sr, n_fft=8192)
# song = song[:sr*5]
# test = np.abs(librosa.stft(song, hop_length=256, win_length=2048, n_fft=8192)
print("creating stft")
_, _, x = signal.stft(song, nperseg=2048, nfft=8192, noverlap=1792)  # 1792/1920
weights = [1.0, 0.5, 0.33, 0.25]

peaks, x = spectral.salience(x)

# x = spectral.temp_function(x)
# x = median_filter(abs(np.flip(x)), size=(1, 12))
# x = np.flip(x)
# x = median_filter(abs(np.flip(x)), size=(1, 12))
x = spectral.refined_log_freq_spec(x)
spectral.display(x)
mask = median_filter(abs(x), size=(1, 64))
mask[mask < np.max(mask)/20] = 0
mask[mask > 0] = 1
x = x * mask
x = median_filter(abs(x), size=(1, 8))

# for frame in range(len(x.T)):
#     peaks, _ = signal.find_peaks(x[:, frame])
#     for peak in peaks:
#         test = np.array(([peak]*4))
#         test += np.array([12, 19, 24, 28])
#         for p, w in zip(test, weights):
#             if p < 128:
#                 x[peak, frame] += x[p, frame] * w


for frame in range(len(x.T)):
    one = np.argmax(x[:, frame])
    tmp = x[one, frame]
    x[one, frame] = 0
    two = np.argmax(x[:, frame])
    x[two, frame] = 0
    three = np.argmax(x[:, frame])
    x[[one, two, three], frame] = 10000000

x = abs(x)
x[x < 10000000] = 0
x = minimum_filter(abs(x), size=(1, 4))
# x = median_filter(abs(x), size=(1, 32))

# x = utils.log_compression(x)
                    # arr[i] += arr[i+12] + arr[i+19] + arr[i+24] + arr[i+28]
spectral.display(x)
# spectral.display(test)


# print(len(np.nonzero(x[66])[0]))
# print((np.nonzero(x[66])[0]))
for i in np.nonzero(x[66, :]):
    print(str(i[0]) + " " + str(i[-1]))

notes = {}


def get_length(arr):
    return arr[0], arr[-1]


for freq in range(len(x)):
    line = np.nonzero(x[freq])[0]
    for hit in midi_tools.split_notes(line):
        if len(hit) > 1:
            dur = get_length(hit)
            if freq in notes:
                notes[freq].append(dur)
            else:
                notes[freq] = [dur]


# for frame, note in notes:


track = 0
channel = 0
time = 0   # In beats
tempo = bpm  # In BPM
volume = 100  # 0-127, as per the MIDI standard
MyMIDI = MIDIFile(1)
MyMIDI.addTempo(track, time, tempo)

for key, items in notes.items():
    pitch = key
    for item in items:
        start = utils.time_to_beats(utils.frame_to_time(item[0], sr=sr), bpm)
        end = utils.time_to_beats(utils.frame_to_time(item[1], sr=sr), bpm)
        duration = end - start
        MyMIDI.addNote(track, channel, pitch, start, duration, volume)

print("track complete")
with open("fur-elise.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
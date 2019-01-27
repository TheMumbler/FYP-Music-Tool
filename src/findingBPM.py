import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
import numpy as np
import librosa

fs, data = wavfile.read('../Songs/kiss_the_rain.wav')
y, sr = librosa.load('../Songs/kiss_the_rain.wav')

def librosaBPM(wave, samplerate):
    onset_env = librosa.onset.onset_strength(wave, sr=samplerate)
    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=samplerate)
    return(tempo)

x = (librosaBPM(y, sr))
print(x)
# librosa.beat.tempo


# plt.figure(1)
# plt.title('Signal Wave...')
# plt.plot(signal)
# plt.show()

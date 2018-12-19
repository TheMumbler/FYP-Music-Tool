import matplotlib.pyplot as plt
import numpy as np
import wave
import sys

song = spf = wave.open('../Songs/Synthesia/MoonlightSonata1.wav','r')

signal = spf.readframes(-1)
# signal = np.fromstring(signal, 'Int16')
# if spf.getnchannels() == 2:
#     print ('Just mono files')
#     sys.exit(0)

plt.figure(1)
plt.title('Signal Wave...')
plt.plot(signal)
plt.show()
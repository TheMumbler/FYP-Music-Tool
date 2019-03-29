from scipy import signal
import numpy as np
# TODO: Find only necessary librosa packages to lower import time


class Song(object):
    tracks = []

    def __init__(self, filename):
        self.name = filename
        self.sr, self.wave = scipy.io.wavfile.read(filename)
        self.spectro = self.short_time()

    # PREPROCESSING

    def bandpass(wave, bands=1):
        """Return a bandpass filtered version of a wave"""
        return wave

    # TRANSFORM
    def short_time(self, win_len=2048, w='hann', nfft=8192, hop_size=128):
        """Short time fourier transform"""
        # TODO: Tidy this up
        song = self.wave
        w = signal.get_window(w, win_len)
        short = np.zeros(shape=(nfft/2, (len(song) - win_len) // hop_size), dtype=complex)
        for i in range(0, len(song) - win_len, hop_size):
            windowed = song[i:i + win_len] * w
            this = np.fft.fft(windowed, n=8192)
            this = this[:len(this) // 2]
            short[:, (i // hop_size) - 1] = this
        return short

    def constant_q(self):
        """Constant q transform"""
        pass

    # SALIENCE

    def does_salience_stuff(self):
        pass

    # TRACKING (Identifying instruments)

    def kmeanie(self):
        pass

    # VOICING (Determining where notes are present or not)

    def __repr__(self):
        return "filename: {}".format(self.name)


x = Song('../Songs/river_flows_in_you.wav')
print(x)

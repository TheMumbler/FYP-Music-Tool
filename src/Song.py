import librosa
# TODO: Find only necessary librosa packages to lower import time


class Song(object):
    tracks = []

    def __init__(self, filename, bpm=0):
        self.name = filename
        self.wave, self.sr = librosa.load(filename)
        self.onset_env = librosa.onset.onset_detect(self.wave, sr=self.sr)
        # self.spectro = scipy.stft(self.wave)
        if bpm == 0:
            self.bpm = librosa.beat.tempo(onset_envelope=self.onset_env, sr=self.sr)
        else:
            self.bpm = bpm

    # PREPROCESSING

    def bandpass(wave, bands=1):
        """Return a bandpass filtered version of a wave"""
        return wave

    # TRANSFORM
    def short_time(self):
        """Short time fourier transform"""
        pass

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
        return "filename: {}\nbpm: {}".format(self.name, self.bpm)


x = Song('../Songs/river_flows_in_you.wav', bpm=10)
print(x)

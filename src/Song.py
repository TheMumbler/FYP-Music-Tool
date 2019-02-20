import librosa
# TODO: Find only necessary librosa packages to lower import time


class Song(object):
    tracks = []

    def __init__(self, filename, filternum=0, bpm=0):
        self.name = filename
        self.wave, self.sr = librosa.load(filename)
        self.onset_env = librosa.onset.onset_detect(self.wave, sr=self.sr)
        self.no_tracks = filternum
        if bpm == 0:
            self.bpm = librosa.beat.tempo(onset_envelope=self.onset_env, sr=self.sr)
        else:
            self.bpm = bpm

    def filter_bank(self):
        # TODO: Split song into X tracks using band pass filter on self.filternum( use mel freq)
        pass

    def __repr__(self):
        return "filename: {}\nbpm: {}".format(self.name, self.bpm)


x = Song('../Songs/river_flows_in_you.wav', bpm = 10)
print(x)

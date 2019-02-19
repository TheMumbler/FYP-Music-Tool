import librosa


class Track(object):
    def __init__(self, wave, sr):  # maybe takes onset envelope too or maybe create one for each
        self.raw = wave
        self.sr = sr
        self.on
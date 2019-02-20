import librosa
import numpy as np
# TODO: Find only necessary librosa packages to lower import time


class Track(object):
    notes = np.array  # An array of note objects

    def __init__(self, wave, sr):  # maybe takes onset envelope too or maybe create one for each
        self.raw = wave
        self.sr = sr
        self.onsets = []  # TODO: Find onsets, librosa function (maybe use songs envelope)

    def create_notes(self):
        # fills self.notes with note objects
        pass

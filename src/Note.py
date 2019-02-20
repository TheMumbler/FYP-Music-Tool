import librosa
# TODO: Find only necessary librosa packages to lower import time


class Note(object):
    """An object that takes a wave and start point and tries to find the offset of the note
    by tracking the fundamental frequency. This will also store the of the note and its musical
    note and using the bpm and the note length we will be able to find the 'rhythm' value"""
    def __init__(self):
        pass


import numpy as np
from . import utils
from midiutil import MIDIFile
import os


drumMidi = {"Ride" : 51,
            "Kick" : 36,
            "Snare" : 38,
            "Clap" : 39,
            "Tom" : 41,
            "OpenHat" : 46,
            "ClosedHat" : 42,
            "Crash" : 49}


def split_notes(line, gap_allow=15):
    x = (np.diff(line))
    x[x < gap_allow] = 0
    ends = np.nonzero(x)
    notes = []
    start = 0
    end = 0
    for end in ends[0]:
        notes.append(line[start:end+1])
        start = end+1
    notes.append(line[end+1:])
    return notes


def get_notes(spec):
    """

    :param spec: a log freq spectrogram containing non-zero points at only note hits
    :return: a dictionary with an entry for each midi note each containing the beginning and ending of each note hit
    """
    notes = {}
    for freq in range(len(spec)):
        line = np.nonzero(spec[freq])[0]
        for hit in split_notes(line):
            if len(hit) > 1:
                dur = (hit[0], hit[-1])
                if freq in notes:
                    notes[freq].append(dur)
                else:
                    notes[freq] = [dur]
    return notes


def output_midi(name, notes, bpm, sr, hopsize=256, directory="testy"):
    """
    :param name: name of the output file
    :param notes: a dictionary with an entry for each midi note each containing the times of the notes being hit
                  see get_notes
    :param bpm: the bpm of the input song
    :param sr: sample rate
    :param hopsize: the hop size of the spectrogram used

    outputs a midi file to the current directory
    """
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
            start = utils.time_to_beats(utils.time_coef(item[0], hop_size=hopsize, sr=sr), bpm)
            end = utils.time_to_beats(utils.time_coef(item[1], hop_size=hopsize, sr=sr), bpm)
            duration = end - start
            # if duration > .15:
            MyMIDI.addNote(track, channel, pitch, start, duration, volume)

    print("track complete")
    output_path = directory
    file = os.path.join(output_path, name + ".mid")
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, "wb") as output_file:
        MyMIDI.writeFile(output_file)


def out_midi_drums(onsets, drums, bpm, sr, hopsize=512):
    track = 0
    channel = 9
    time = 0  # In beats
    tempo = bpm  # In BPM
    volume = 100  # 0-127, as per the MIDI standard
    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(track, time, tempo)
    # MyMIDI.addProgramChange(track, channel, time, 113)
    for onset, drumList in zip(onsets, drums):
        for drum in drumList:
            start = utils.time_to_beats(utils.time_coef(onset-onsets[0], hop_size=hopsize, sr=sr), bpm)
            pitch = drumMidi[drum]
            duration = 1
            MyMIDI.addNote(track, channel, pitch, start, duration, volume)
    with open("drums.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)


# def quantize(n, beat=16):
#

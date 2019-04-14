import numpy as np
from . import utils
from midiutil import MIDIFile


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


def output_midi(name, notes, bpm, sr):
    """
    :param name: name of the output file
    :param notes: a dictionary with an entry for each midi note each containing the times of the notes being hit
                  see get_notes
    :param bpm: the bpm of the input song
    :param sr: sample rate

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
            start = utils.time_to_beats(utils.frame_to_time(item[0], sr=sr), bpm)
            end = utils.time_to_beats(utils.frame_to_time(item[1], sr=sr), bpm)
            duration = end - start
            if duration > .33:
                MyMIDI.addNote(track, channel, pitch, start, duration, volume)

    print("track complete")
    with open(name+".mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)

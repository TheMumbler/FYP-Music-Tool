import numpy as np


def split_notes(line):
    x = (np.diff(line))
    x -= 1
    ends = np.nonzero(x)
    notes = []
    start = 0
    end = 0
    for end in ends[0]:
        notes.append(line[start:end+1])
        start = end+1
    notes.append(line[end+1:])
    return notes

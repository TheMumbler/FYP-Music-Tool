from src.song import structure, read
import numpy as np

sr, song = read.read("test/testfiles/structure.wav")
song = read.startend(song)
ret = structure.find_segments(song)


def test_split_pos():
    """Check functionality"""
    arr = [1, 1, 1, 1, -1, -1, 1, -1]
    assert np.allclose(structure.split_pos(arr)[0], [1, 1, 1, 1, 0, 0, 1, 0])
    assert np.allclose(structure.split_pos(arr)[1], [0, 0, 0, 0, 1, 1, 0, 1])


def test_chroma_structure_shape():
    """Tests if square"""
    sim = structure.chroma_structure(song)
    assert sim.shape[0] == sim.shape[1]


def test_segments():
    assert type(ret) is list

from src.song import spectral
from src.song import read

sr, testfile = read.read("test\\testfiles\\110.wav")
testfile = testfile[:sr*5]


def test_read():
    assert sr == 44100

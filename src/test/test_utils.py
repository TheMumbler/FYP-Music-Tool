from src.song import utils
import numpy as np


def test_time_coef():
    assert utils.time_coef(100, 512, 44100) == 1.1609977324263039


def test_time_coef1():
    assert utils.time_coef(100, 512, 22050) == 1.1609977324263039*2


def test_freq_coef():
    assert abs(utils.freq_coef(81, 44100, 8192) - 440) < 5
    assert utils.freq_coef(81.73424036281179, 44100, 8192) == 440


def test_freq_to_bucket():
    assert utils.freq_to_bucket(81, 100, 8.66) == 69
    assert utils.freq_to_bucket(81, 100, 8.66, sr=22050) == 57
    assert utils.freq_to_bucket(81, 100, 8.66, nfft=4096) == 81
    assert utils.freq_to_bucket(81, 100, 8.66, sr=22050, nfft=4096) == 69


def test_log_compression():
    pass


def test_magphase():
    inp = np.array([[1.+1.j, 2.+2.j, 3.+3.j],
                    [4.+4.j, 5.+5.j, 6.+6.j],
                    [7.+7.j, 8.+8.j, 9.+9.j]])
    mag, phase = utils.magphase(inp)
    assert np.allclose(mag, np.abs(inp))


def test_time_to_beats():
    assert utils.time_to_beats(.5, 120) == 1



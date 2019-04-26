from src.song import utils


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


def test_bin_offset():
    pass


def test_bucket_size():
    pass


def test_frame_to_time():
    pass


def test_log_compression():
    pass


def test_log_freq_spec():
    pass


def test_mag_to_db():
    pass


def test_magphase():
    pass


def test_midi_to_pitch():
    pass


def test_time_to_beats():
    pass



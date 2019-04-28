from src.song import read
from shutil import copyfile
import numpy as np

def test_filename_raw():
    assert read.get_filename(r"C:\Users\P\PycharmProjects\2019-ca400-ferryp2\src\test\test.mp3") == "test.mp3"
    assert read.get_filename(r"C:\Users\P\PycharmProjects\2019-ca400-ferryp2\src\test\te st.mp3") == "te st.mp3"


def test_filename_standard():
    assert read.get_filename("src\\test\\te st.mp3") == "te st.mp3"


def test_filepath_raw():
    assert read.get_path(r"src\test\test.mp3") == "src\\test\\"


def test_filepath_standard():
    assert read.get_path("src\\test\\te st.mp3") == "src\\test\\"


def test_read_wav():
    assert read.read("test/testfiles/test_wav.wav")


def test_read_mp3():
    file = "test\\testfiles\\testmp3.mp3"
    newfile = file[:-4] + "copy" + file[-4:]
    copyfile(file, newfile)
    assert read.read(newfile)


def test_startend():
    arr = [0] * 5 + [1] * 5 + [0] * 10
    assert read.startend(arr) == [1, 1, 1, 1, 1]


def test_startend_np():
    arr = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
    after = read.startend(arr)
    assert np.allclose(after, np.array([1, 1, 1, 1, 1]))
    assert type(after) is np.ndarray

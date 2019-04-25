import scipy.io.wavfile
import subprocess
import os


def read(file):
    # TODO: Use ffmpeg to convert song to mono and Wav format
    if file.endswith(".wav"):
        sr, song = scipy.io.wavfile.read(file)
        song = startend(song)
    else:
        newfile = "converted.wav"
        path = get_path(file)
        new = os.path.join(path, newfile)
        subprocess.call("ffmpeg -loglevel panic -i " + file + " -ac 1 -f wav " + new)
        sr, song = scipy.io.wavfile.read(new)
        song = startend(song)
        os.remove(file)
    return sr, song


def startend(song):
    for i in range(len(song)):
        if song[i] != 0:
            break
    start = i
    for i in range(1, len(song)):
        if song[-i] != 0:
            break
    song = song[start:-i+1]
    return song


def get_filename(address):
    name = address.split("\\")
    return name[-1]


def get_path(address):
    path = address.split("\\")
    return "\\".join(path[:-1]) + "\\"

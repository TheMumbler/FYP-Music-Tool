import scipy.io.wavfile
import subprocess
import os
from pytube import YouTube


def read(file, delete=True):
    file = os.path.abspath(file)
    if file.endswith(".wav"):
        sr, song = scipy.io.wavfile.read(file)
    else:
        newfile = "converted.wav"
        path = get_path(file)
        new = os.path.join(path, newfile)
        subprocess.call("ffmpeg -loglevel panic -i " + file + " -ac 1 -f wav " + new)
        sr, song = scipy.io.wavfile.read(new)
        if delete:
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
    if i > 1:
        song = song[start:-i+1]
    else:
        song = song[start:-i]
    return song


def get_filename(address):
    name = address.split("\\")
    return name[-1]


def get_path(address):
    path = address.split("\\")
    return "\\".join(path[:-1]) + "\\"


def get_youtube(link, dest=""):
    yt = YouTube(link)
    t = yt.streams.filter(file_extension='mp4').all()
    t[0].download(filename="youtube", output_path=dest)
    file = os.path.join(dest, "youtube.mp4")
    new = os.path.join(dest, "converted.wav")
    subprocess.call("ffmpeg -loglevel panic -i " + file + " -ac 1 -f wav " + new)
    os.remove(file)




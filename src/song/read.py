import scipy.io.wavfile


def read(file):
    # TODO: Use ffmpeg to convert song to mono and Wav format
    sr, song = scipy.io.wavfile.read(file)
    return sr, song


def startend(song):
    for i in range(len(song)):
        if song[i] != 0:
            break
    start = i
    for i in range(1, len(song)):
        if song[-i] != 0:
            break
    song = song[start:-i]
    print(start, i)
    return song

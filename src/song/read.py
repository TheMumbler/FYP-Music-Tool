import scipy.io.wavfile


def read(file):
    # TODO: Use ffmpeg to convert song to mono and Wav format
    sr, song = scipy.io.wavfile.read(file)
    return sr, song

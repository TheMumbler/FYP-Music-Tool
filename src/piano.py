# from src.song import read
from .song import spectral
from .song import utils
from .song import decomp
from scipy import signal
from scipy.ndimage import median_filter
from scipy.ndimage import maximum_filter
from .song import midi_tools
from librosa.beat import tempo

from .song.spectral import octave_weak, non_zero_average_std

# print("done importing")
#
#
# print("reading file")
# # sr, song = read.read('../Songs/fur_elise.wav')
# sr, song = read.read('../Songs/river_flows_in_you.wav')
# # sr, song = read.read('../Songs/deadmau5.wav')
# # sr, song = read.read('../Songs/crab.wav')
# # sr, song = read.read('../Songs/billie.wav')
# # sr, song = read.read('../Songs/hungarian.wav')
# song = song*1.0
#
#
# weights = [1.0, 0.5, 0.33, 0.25]
#


# _, _, x = signal.stft(song, nperseg=2048, nfft=8192, noverlap=1792)
#
# x, _ = utils.magphase(x, mag_only=True)

#

def piano_ver1(x, name, user, bpm, sr, hp=False, sections=None):
    # current peak pick for log_spec
    # avg = uniform_filter1d(abs(spect[:, frame]), 100)
    # peaks, _ = signal.find_peaks(abs(spect[:, frame]), height=avg, prominence=5)
    x = x*1.0
    bpm = tempo(x, sr=sr)[0]
    # TODO: Remove these lines
    x = x[:sr*30]
    _, _, x = signal.stft(x, nperseg=2048, nfft=8192, noverlap=1792)
    x, _ = utils.magphase(x, mag_only=True)
    if hp:
        x, _ = decomp.hpss(x, 2)
    # TODO: ^^ ^^ ^^

    log = spectral.log_spec(x.copy())
    log = spectral.salience(log)

    for frame in range(len(log.T)):
        f = log[:, frame]
        avg, sd = non_zero_average_std(f)
        f[f < avg] = 0
        octave_weak(f)
        avg, sd = non_zero_average_std(f)
        f[f < avg/2] = 0
        log[:, frame] = f

    mask = median_filter(abs(log), size=(1, 32))
    mask[mask > 0] = 1
    log = mask * log
    log = maximum_filter(abs(log), size=(1, 8))
    log = median_filter(abs(log), size=(1, 16))

    notes = midi_tools.get_notes(log)
    return midi_tools.output_midi(name, notes, bpm, sr, hopsize=256, directory=user)


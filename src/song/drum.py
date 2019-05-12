from sklearn.externals import joblib
from keras.models import load_model
import numpy as np
# from sklearn.preprocessing import StandardScaler
# import keras
# from keras import models
# from keras import layers
import librosa
import os
from src.song import midi_tools
from src.song import read


c = {0: "Clap",
     1: "ClosedHat",
     2: "Crash",
     3: "Kick",
     4: "OpenHat",
     5: "Ride",
     6: "Snare",
     7: "Tom"}


def extract_feats(y, sr):
    features = []
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    features.append(np.mean(chroma_stft))

    rmse = librosa.feature.rmse(y=y)
    features.append(np.mean(rmse))

    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    features.append(np.mean(spec_cent))

    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    features.append(np.mean(spec_bw))

    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    features.append(np.mean(rolloff))

    zcr = librosa.feature.zero_crossing_rate(y)
    features.append(np.mean(zcr))

    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    for e in mfcc:
        features.append(np.mean(e))

    return np.array(features)


def scale_features(feats):
    scaler = joblib.load(os.path.abspath("scaler.save"))
    trans = scaler.transform([feats])
    return trans


def drum_tool(song, name, bpm=None, **kwargs):
    sr, song = read.read(song)
    song = song * 1.0
    scaler = joblib.load(os.path.abspath("scaler.save"))
    model = load_model('drum_model.h5')

    onset_env = librosa.onset.onset_strength(song)
    onset_frames = librosa.onset.onset_detect(song, onset_envelope=onset_env)
    onset_samples = onset_frames * 512

    segments = []
    for ons in onset_samples[:-1]:
        segment = song[ons - 3000:ons + 3000]
        #     windowed = segment * window
        segments.append(segment)

    for i in range(len(segments)):
        segments[i] = extract_feats(segments[i], sr)
    trans = scaler.transform(np.array(segments))

    predictions = (model.predict_proba(trans))

    classes = []
    for prediction in predictions:
        #     print(predict)
        #     highs =(np.argsort(prediction[prediction > .0]))
        #     highest = (c[np.argmax(prediction)])
        #     classes.append([c[x] for x in highs] )
        highest = np.argmax(prediction)
        classes.append(c[highest])
    newclasses = [[x] for x in classes]

    if not bpm:
        bpm = librosa.beat.tempo(song)[0]

    midi_tools.out_midi_drums(name, onset_frames, newclasses, bpm, sr)

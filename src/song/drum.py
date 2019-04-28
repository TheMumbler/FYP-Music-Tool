from sklearn.externals import joblib
from keras.models import load_model
import numpy as np
from sklearn.preprocessing import StandardScaler
import keras
from keras import models
from keras import layers
import librosa
import os


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



import os
import streamlit as st
import joblib
import numpy as np
import librosa
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder

SAMPLE_RATE = 22050
MFCC_COUNT = 13

def extract_mfccs(file_path):
    audio, _ = librosa.load(file_path, sr=SAMPLE_RATE, mono=True)
    mfccs = librosa.feature.mfcc(y=audio, sr=SAMPLE_RATE, n_mfcc=MFCC_COUNT)
    return np.mean(mfccs.T, axis=0)

def predict_audio_class(audio_file, model, le):
    mfcc = extract_mfccs(audio_file)
    mfcc = np.expand_dims(mfcc, axis=0) 
    prediction_prob = model.predict(mfcc)
    prediction = (prediction_prob > 0.5).astype("int32")
    prediction_label = le.inverse_transform(prediction)[0]
    return prediction_label

model = load_model("./model-nd/model.h5")
le = joblib.load("./model-nd/label_encoder.joblib")

st.title("Audio Noise Detector")

audio_file = st.file_uploader("Upload an audio file ", type=['wav', 'mp3', 'flac'])

if audio_file is not None:
    temp_file = "temp_audio.wav"
    with open(temp_file, 'wb') as f:
        f.write(audio_file.read())

    prediction = predict_audio_class(temp_file, model, le)
    st.write(f"The audio is predicted as: {prediction}")
    st.audio(temp_file, format='wav')

    os.remove(temp_file)

import streamlit as st
import keras
import joblib
import librosa
import numpy as np
import os
import soundfile as sf
import Visualization as V
from pydub import AudioSegment
from speechbrain.pretrained import SepformerSeparation as separator
import tempfile
import matplotlib.pyplot as plt
from audiomentations import Compose, AddGaussianNoise, TimeStretch, PitchShift, Shift
import time

SAMPLE_RATE = 22050
MFCC_COUNT = 40
TOP_DB = 20

@st.cache_resource
def get_model_human_speech():
    return keras.models.load_model("HumanSpeechRecognition/model-human-speech-detection/model.h5")

@st.cache_resource
def get_encoder():
    return joblib.load("HumanSpeechRecognition/model-human-speech-detection/label_encoder.joblib")


@st.cache_resource
def get_model_noise():
    return keras.models.load_model("NoiseDetection/model-nd/noise_model.h5")


@st.cache_resource
def get_encoder_noise():
    return joblib.load("NoiseDetection/model-nd/noise_label_encoder.joblib")

@st.cache_resource
def load_model():
    return separator.from_hparams(source="speechbrain/sepformer-whamr-enhancement", savedir='demo/pretrained_models/sepformer-whamr-enhancement')

model = load_model()

model_human_speech = get_model_human_speech()
le_human_speech = get_encoder()

model_noise = get_model_noise()
le_noise = get_encoder_noise()

def delete_file_after_delay(filename, delay=5):

    time.sleep(delay)  
    try:
        os.unlink(filename)  
    except PermissionError:
        pass 

def remove_silence(audio, sr, top_db=TOP_DB):
    y_trimmed, _ = librosa.effects.trim(audio, top_db=top_db)
    return y_trimmed

def augment_audio(audio, sr):
    augmenter = Compose([
        AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=0.3),
        TimeStretch(min_rate=0.8, max_rate=1.25, p=0.3),
        PitchShift(min_semitones=-4, max_semitones=4, p=0.3),
        Shift(min_fraction=-0.5, max_fraction=0.5, p=0.3),
    ])
    audio_augmented = augmenter(samples=audio, sample_rate=sr)
    return audio_augmented

def extract_features(audio, sr):
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=MFCC_COUNT)
    chroma_stft = librosa.feature.chroma_stft(y=audio, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=audio, sr=sr)
    tonnetz = librosa.feature.tonnetz(y=audio, sr=sr)
    return np.concatenate((np.mean(mfccs.T, axis=0), 
                           np.mean(chroma_stft.T, axis=0),
                           np.mean(spectral_contrast.T, axis=0),
                           np.mean(tonnetz.T, axis=0)))

def load_data(data_path, augment=False):
    features = []
    labels = []
    for label in ["human", "other"]:
        folder_path = os.path.join(data_path, label)
        for filename in os.listdir(folder_path):
            if not (filename.endswith('.mp3') or filename.endswith('.wav') or filename.endswith('.flac')):
                continue
            file_path = os.path.join(folder_path, filename)
            audio, _ = librosa.load(file_path, sr=SAMPLE_RATE, mono=True)
            audio = remove_silence(audio, SAMPLE_RATE)
            if augment:
                audio = augment_audio(audio, SAMPLE_RATE)
            feature = extract_features(audio, SAMPLE_RATE)
            features.append(feature)
            labels.append(label)
    return np.array(features), np.array(labels)

def load_audio(audio_file):
    audio, _ = librosa.load(audio_file, sr=SAMPLE_RATE, mono=True)
    return audio


def predict_audio_class(audio_file_path, model, le):
    audio, _ = librosa.load(audio_file_path, sr=SAMPLE_RATE, mono=True)
    audio = remove_silence(audio, SAMPLE_RATE)
    feature = extract_features(audio, SAMPLE_RATE)
    feature = np.expand_dims(feature, axis=0)  # because the model expects 2D array
    prediction_prob = model.predict(feature)
    prediction = (prediction_prob > 0.5).astype("int32")
    prediction_label = le.inverse_transform(prediction)[0]
    return prediction_label

def extract_mfccs(file_path):
    SAMPLE_RATE = 22050
    MFCC_COUNT = 13
    audio, _ = librosa.load(file_path, sr=SAMPLE_RATE, mono=True)
    mfccs = librosa.feature.mfcc(y=audio, sr=SAMPLE_RATE, n_mfcc=MFCC_COUNT)
    return np.mean(mfccs.T, axis=0)

def predict_audio_class_noise(audio_file, model, le):
    mfcc = extract_mfccs(audio_file)
    mfcc = np.expand_dims(mfcc, axis=0) 
    prediction_prob = model.predict(mfcc)
    prediction = (prediction_prob > 0.5).astype("int32")
    prediction_label = le.inverse_transform(prediction)[0]
    return prediction_label

st.title('Human Speech Detection and Enhancement')

uploaded_file = st.file_uploader("Choose an audio file", type=['mp3', 'wav', 'flac'])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(uploaded_file.read())
    audio = load_audio(tfile.name)

    st.audio(audio, format='audio/wav', sample_rate=SAMPLE_RATE)

    #Human speech detected
    prediction = predict_audio_class(tfile.name, model_human_speech, le_human_speech)
    
    

    #st.write(f"The audio is predicted as: {prediction}")
    
    
    if(prediction == "human"):
        st.write(f"Human voice detected! Detecting Quality \n\n")
        with st.spinner("Detecting if audio is noisy..."):
            noise_prediction = predict_audio_class_noise(tfile.name, model_noise, le_noise)
            
        st.write(f"The audio quality is: {noise_prediction}")
        
        if noise_prediction == "noise":
            y_o, sr = librosa.load(tfile.name)
            with st.spinner("Cleaning audio..."):
                enhanced_audio = model.separate_file(path=f"{tfile.name}")
            
            st.divider()
            
            st.write("Cleaned Audio:")
            
            enhanced_data = enhanced_audio[:,:].detach().cpu().squeeze()
            
            
            sf.write("data/clean.wav",enhanced_data,samplerate=8000)
            st.audio("data/clean.wav")
            
            y_e, sr = librosa.load("data/clean.wav")
            
            st.subheader("Visualizations The Cleaned Audio vs Origianl Audio")
            with st.expander("Click to see the comparison"):
                st.write("Original Audio")
                V.show_waveform(y_o/max(y_o),sr, color='blue')
                st.write("Cleaned Audio")
                # set the color differently
                V.show_waveform(y_e,sr, color='red')
                
    else:
        st.write(f"No Human Speech detected \n\n")
    

    #delete_file_after_delay(tfile.name) 
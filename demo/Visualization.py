import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


# load audio file by a function
def load_audio(audio_path):
    y, sr = librosa.load(audio_path)
    return y, sr


# plotting the waveform of the audio file
def plot_waveform(y, sr, color='gray_r'):
    librosa.display.waveshow(y, sr=sr, color=color)


# plotting the spectrogram of the audio file
def plot_spectrogram(y, sr):
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    librosa.display.specshow(D, y_axis='linear')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Linear-frequency power spectrogram')


# plotting the mel-spectrogram of the audio file
def plot_melspectrogram(y, sr):
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max), y_axis='mel', fmax=8000, x_axis='time')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel spectrogram')


# show the plot of the audio file waveform in streamlit
def show_waveform(y, sr, color='gray_r'):
    # st.title("Waveform")
    fig = plt.figure(figsize=(8, 2))
    plot_waveform(y, sr, color)
    st.pyplot(fig)
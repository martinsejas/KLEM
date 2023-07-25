import streamlit as st
import soundfile as sf
from speechbrain.pretrained import SepformerSeparation as separator
import librosa
import speech_recognition as speech_recon
import numpy as np
from audiorecorder import audiorecorder
import Visualization as V
import requests
import utility


DATA_PATH="data/"

@st.cache_resource
def load_model():
    return separator.from_hparams(source="speechbrain/sepformer-whamr-enhancement", savedir='demo/pretrained_models/sepformer-whamr-enhancement')

model = load_model()

st.title("  Clean and Transcribe your audio! ")


audio_file = st.file_uploader(label="Upload audio",type=[".wav"])

if audio_file is not None:
    
    # save the audio_file to DATA_PATH
    with open(f"{DATA_PATH}{audio_file.name}","wb") as f:
        f.write(audio_file.getbuffer())
    
    st.write("Noisy Audio:")
    st.audio(audio_file)
    
    y_o, sr = librosa.load(audio_file)
    # y_o,sr = librosa.load(f"{DATA_PATH}{audio_file.name}")
    
    WRITTEN_PATH = f"{DATA_PATH}sample.wav"

    with st.spinner("Cleaning audio..."):
        enhanced_audio = model.separate_file(path=f"{DATA_PATH}{audio_file.name}")
        
    st.divider()
    
    st.write("Cleaned Audio:")
    
    enhanced_data = enhanced_audio[:,:].detach().cpu().squeeze()
    
    
    sf.write("data/clean.wav",enhanced_data,samplerate=8000)
    #sf.write("data/clean.wav",enhanced_data_resampled,samplerate=16000)
    st.audio("data/clean.wav")
    
    y_e, sr = librosa.load("data/clean.wav")
    
    st.subheader("Visualizations The Cleaned Audio vs Origianl Audio")
    with st.expander("Click to see the comparison"):
        st.write("Original Audio")
        V.show_waveform(y_o/max(y_o),sr, color='blue')
        st.write("Cleaned Audio")
        # set the color differently
        V.show_waveform(y_e,sr, color='red')
    
    
    API_URL_TRANS = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-fr"
    API_TOKEN = utility.API_TOKEN
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    def query_translation(payload):
        response = requests.post(API_URL_TRANS, headers=headers, json=payload)
        return response.json()
    
    # API_URL_2_SPEECH = "https://api-inference.huggingface.co/models/facebook/tts_transformer-fr-cv7_css10"

    # def query_2_speech_fr(filename):
    #     with open(filename, "rb") as f:
    #         data = f.read()
    #     response = requests.post(API_URL_2_SPEECH, headers=headers, json=data)
    #     return response.json()

# output = query({"inputs": "This is a test"})
    
    st.subheader("Transcription")
    r = speech_recon.Recognizer()

    with speech_recon.AudioFile("data/clean.wav") as source:
        audio_text = r.listen(source)
        
        with st.spinner("Transcribing..."):
            final_text = r.recognize_google(audio_data=audio_text)
        
        st.write(final_text)
        
        st.subheader("Translation of the transcription to French")
        output = query_translation({"inputs": final_text})
        translation = output[0]['translation_text']
        st.write(translation)
        
        with open(f"translation/{audio_file.name}.txt", 'w') as f:
            f.write(translation)

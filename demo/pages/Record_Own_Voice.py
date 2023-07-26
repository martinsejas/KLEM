import streamlit as st
import soundfile as sf
from speechbrain.pretrained import SepformerSeparation as separator
import librosa
import speech_recognition as speech_recon
import numpy as np
from audiorecorder import audiorecorder
import wave
from io import BytesIO


DATA_PATH="data/"

@st.cache_resource
def load_model():
    return separator.from_hparams(source="speechbrain/sepformer-whamr-enhancement", savedir='demo/pretrained_models/sepformer-whamr-enhancement')

model = load_model()

st.title("  Clean and Transcribe your audio! ")

st.subheader("Record your own voice!")
audio = audiorecorder()

if len(audio) > 0:
    # To play audio in frontend:
    
    
    
    st.audio(audio.tobytes())
    
    
    sf.write("data/own_voice.wav",audio,samplerate=8000)
    # To save audio to a file:
    # wav_file = open("audio.wav", "wb")

   
  
    
    st.audio("data/own_voice.wav")
    
    # st.write()
    # sf.write("data/clean.wav",audio)
        
    
    # st.write("Noisy Audio:")
    # st.audio(audio.tobytes())
    
    # y,sr = librosa.load(f"data/audio.wav")
    
    # #WRITTEN_PATH = f"{DATA_PATH}sample.wav"

    # with st.spinner("Cleaning audio..."):
    #     enhanced_audio = model.separate_file(path=f"data/audio.wav")
        
    # st.divider()
    
    # st.write("Cleaned Audio:")
    
    # enhanced_data = enhanced_audio[:,:].detach().cpu().squeeze()
    
    
    # sf.write("data/clean.wav",enhanced_data,samplerate=8000)
    # #sf.write("data/clean.wav",enhanced_data_resampled,samplerate=16000)
    # st.audio("data/clean.wav")
    
    # y, sr = librosa.load("data/clean.wav")
    
    
    # st.subheader("Transcription")
    # r = speech_recon.Recognizer()

    # with speech_recon.AudioFile("data/clean.wav") as source:
    #     audio_text = r.listen(source)
        
    #     with st.spinner("Transcribing..."):
    #         final_text = r.recognize_google(audio_data=audio_text)
        
    #     st.write(final_text)
           

    
   
    
     
            
       
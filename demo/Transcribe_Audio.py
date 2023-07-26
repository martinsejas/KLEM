import streamlit as st
import speechbrain as sb
import soundfile as sf
from speechbrain.pretrained import SepformerSeparation as separator
import librosa
import speech_recognition as speech_recon

DATA_PATH="data/"

st.title("  Clean and Transcribe your audio! ")
st.subheader(" For this example we will be loading a sample audio, cleaning it and printing the transcription")

model = separator.from_hparams(source="speechbrain/sepformer-whamr-enhancement", savedir='demo/pretrained_models/sepformer-whamr-enhancement')


audio_file = st.file_uploader(label="Upload audio",type=[".wav"])

if audio_file is not None:
    
   
    st.write("Noisy Audio Example")
    st.audio(audio_file)
    
    y,sr = librosa.load(f"{DATA_PATH}{audio_file.name}")
    
    WRITTEN_PATH = f"{DATA_PATH}sample.wav"

    st.write("Cleaning audio...")
   
    enhanced_audio = model.separate_file(path=f"{DATA_PATH}{audio_file.name}")
    
    st.write("Cleaned Audio Example")
    
    enhanced_data = enhanced_audio[:,:].detach().cpu().squeeze()
    
    sf.write("data/clean.wav",enhanced_data,samplerate=8000)
    st.write("clean audio")
    st.audio("data/clean.wav")
    
    
    st.subheader("Transcription")
    r = speech_recon.Recognizer()

    with speech_recon.AudioFile("data/clean.wav") as source:
        audio_text = r.listen(source)
        
    
        try:
            #text = r.recognize_google(audio_text)
            text = r.recognize_sphinx(audio_text)
            
            st.write("Converting... ")
            st.write(f"Google Transcription: {text}")
           
        except:
            st.write("Error")
            
       

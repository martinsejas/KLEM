import streamlit as st
import pyaudio
import wave
import keyboard
import speech_recognition as speech_recon

SAMPLING_RATE = 44100
CHUNK_SIZE = 1024
filename = "data/own_recording.wav"


audio_format = pyaudio.paInt16
channels = 1# Stereo
p = pyaudio.PyAudio()

stream = p.open(format=audio_format,
                channels=channels,
                rate=SAMPLING_RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE)

st.write("Hold 'r' to record your voice")

frames = []

my_bar = st.progress(0, text="Not Recording")

count = 0

while keyboard.is_pressed('r'):
    count+=1
    if(count == 99):
        count = 1
    data = stream.read(CHUNK_SIZE)
    frames.append(data)
    my_bar.progress(count, text="Recording (Speak Now!)")
    

print("Recording finished.")

stream.stop_stream()
stream.close()
p.terminate()

# Save the audio to a file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(audio_format))
wf.setframerate(SAMPLING_RATE)
wf.writeframes(b''.join(frames))
wf.close()


if count > 0:
    st.audio(filename)
    st.subheader("Transcription")
    r = speech_recon.Recognizer()

    with speech_recon.AudioFile(filename) as source:
        audio_text = r.listen(source)
        
        with st.spinner("Transcribing..."):
            final_text = r.recognize_google(audio_data=audio_text)
        
        st.write(final_text)
           
import streamlit as st
import pyaudio
import wave
import keyboard
import speech_recognition as speech_recon
import openai
import datetime

openai.api_key = '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'

# def your_script(generated_text):
#     generated_text = "Hello Chatgpt tell me a joke about AI"
#     return generated_text

messages = [{"role": "system", "content": "You are a helpful assistant."}]



def send_to_gpt(text):
    global messages
    
    messages.append({"role": "user", "content": text})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages= messages
    )
    return response['choices'][0]['message']['content']

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
    st.subheader("Prompt")
    r = speech_recon.Recognizer()

    with speech_recon.AudioFile(filename) as source:
        audio_text = r.listen(source)
        
        with st.spinner("Transcribing..."):
            final_text = r.recognize_google(audio_data=audio_text)
        
        st.write(final_text)
        chat_gpt_response = send_to_gpt(final_text)
        messages.append( {"role": "system","content":chat_gpt_response})
        
        st.subheader("Chatbot")
        st.write(chat_gpt_response)
       
    with open("chatlogs/main_log.txt","a") as log:
        log.write(f"You|{final_text}£")
        log.write(f"Chat Gpt|{chat_gpt_response}£")
      

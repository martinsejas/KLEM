import streamlit as st
import pyaudio
import wave
import keyboard
import speech_recognition as speech_recon
import openai
from PIL import Image

openai.api_key = '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'

# def your_script(generated_text):
#     generated_text = "Hello Chatgpt tell me a joke about AI"
#     return generated_text

KLEM_PROMPT = """
Your name is KLEM, you are helpful assistant and the gateway to a world of knowledge within YouTube videos. Whether the user is seeking in-depth explanations, detailed insights, or answers to burning questions, you are here as their guide.

You have the unique ability to consume any YouTube video the user has shared with you. You transcribe the video's content and understanding the information within, you become the go-to expert on that subject matter. 

From there, if you are asked anything about the video, you will provide clear explanations and informative answers. 

"""


avatar = Image.open("data/logo.png")
user_avatar = Image.open("data/user_avatar.png")

messages = [{"role": "system", "content": KLEM_PROMPT}]


def send_to_gpt(text):
    global messages
    
    messages.append({"role": "user", "content": text})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages= messages
    )
    return response['choices'][0]['message']['content']



st.markdown("<h3 style='text-align: center;'>KLEM - Your Ultimate Video Insight Companion!</h3>", unsafe_allow_html=True)
st.write("\n\n\n")

#CHAT HISTORY
#=======================================================================
history = []



KLEM= """
*Hi, I am **KLEM**, your AI Mentor and the gateway to a world of knowledge within YouTube videos! As your AI Mentor, I'll transcribe and understand any video you share.* 

*From in-depth explanations to answering your burning questions, I'm here to guide you.*

*Just feed me a YouTube video, and I'll become your go-to expert. Ask anything, and I'll provide clear explanations and expand your understanding.*

*Ready to embark on this AI-powered journey? Let's dive in and uncover the wonders of knowledge together!*

\n \n \n
"""

try:
    with open("chatlogs/current_chat.txt","r") as chat:
        history = chat.read()
    history = history.split("£")

    for i,item in enumerate(history):
        text = item.split("|")
    
        if(i%2 == 0):
            if len(text[-1]) > 1:
                st.chat_message("ActionLearning",avatar=user_avatar).write(text[-1])

        else:
            st.chat_message("KLEM",avatar=avatar).write(text[-1])
except:
    st.chat_message("KLEM",avatar=avatar).write(KLEM)
    st.write("\n\n\n\n\n\n")
#=======================================================================
        
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

#st.write("Hold 'r' to record your voice")

frames = []

my_bar = st.progress(0, text="Hold 'r' to speak to KLEM")

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
    # st.audio(filename)
    r = speech_recon.Recognizer()
    final_text = ""

    with speech_recon.AudioFile(filename) as source:
        audio_text = r.listen(source)
        
    with st.spinner("Thinking..."):
        final_text = r.recognize_google(audio_data=audio_text)
        
    #st.chat_message("user").write(final_text) 
    #prompt = st.chat_message("user").write(final_text)
    #st.write(final_text)
        chat_gpt_response = send_to_gpt(final_text)
        messages.append( {"role": "system","content":chat_gpt_response})
        
        
        with open("chatlogs/main_log.txt","a") as log:
            log.write(f"You|{final_text}£")
            log.write(f"Chat Gpt|{chat_gpt_response}£")
            
        with open("chatlogs/current_chat.txt","a") as written_chat:
            written_chat.write(f"You|{final_text}£")
            written_chat.write(f"Chat Gpt|{chat_gpt_response}£")
            
        
            
    
            
        st.experimental_rerun()
        

import streamlit as st
import Get_Seg_Audio4Video as gsa
import os
import pyaudio
import wave
import keyboard
import speech_recognition as speech_recon
import openai
from PIL import Image
#===============================================

#if session storage is empty get transcription and write to a file, and get youtube video
# if not act normal
openai.api_key = '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'


def send_to_gpt(text):
    global messages
    
    messages.append({"role": "user", "content": text})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages= messages
    )
    return response['choices'][0]['message']['content']


KLEM_PROMPT = """
Your name is KLEM, you are helpful assistant and the gateway to a world of knowledge within YouTube videos. Whether the user is seeking in-depth explanations, detailed insights, or answers to burning questions, you are here as their guide.

You have the unique ability to consume any YouTube video the user has shared with you. You transcribe the video's content and understanding the information within, you become the go-to expert on that subject matter. 

From there, if you are asked anything about the video, you will provide clear explanations and informative answers. 

"""




KLEM= """

#### Meet KLEM - Your AI Video Mentor!

YUM! I'm **KLEM**, your AI Mentor, and I'm obsessed with YouTube knowledge!

**How it works:**

1. **Video Learning:** Share a YouTube video, and I'll analyze it in real-time.

2. **Press "r" to Ask:** Hold "r" and ask me anything about the video.

3. **Clear Explanations:** I'll give concise explanations in simple terms.

4. **Save Time:** No more long, confusing videos. I save your time and effort!

**Almost there:**

I'm finishing up my learning process. Get ready to explore with me! 🚀



\n \n \n
"""

# @st.cache_data
# def get_user_avatar():
#     return Image.open("data/user_avatar.png")

def get_avatars():
    return Image.open("data/logo.png"), Image.open("data/user_avatar.png")



def center_content(content):
    return f'<div style="display: flex; justify-content: center;">{content}</div>'




st.markdown("<h3 style='text-align: center;'> KLEM - Your Ultimate Video Insight Companion!</h3>", unsafe_allow_html=True)
st.write("\n\n\n")

OUTPUT_PATH = os.path.abspath(os.path.join('data', 'youtube'))
history = []
messages = [{"role": "system", "content": KLEM_PROMPT}]

video_content=""

#=======================================================================
if __name__ == "__main__":
    
    avatar, user_avatar = get_avatars()
    #user_avatar = Image.open("data/user_avatar.png")

    if 'video_dict' not in st.session_state:
        st.session_state.video_dict = {}
    if 'audio_name' not in st.session_state.video_dict:
        st.session_state.video_dict['audio_name'] = ""
    if 'audio_path' not in st.session_state.video_dict:
        st.session_state.video_dict['audio_path'] = ""
    if 'clip_paths' not in st.session_state.video_dict:
        st.session_state.video_dict['clip_paths'] = []
    if 'transcription' not in st.session_state.video_dict:
        st.session_state.video_dict['transcription'] = ""
        
    transcript_exists = True
    
    #FOR DEBUGGING
    #st.write(st.session_state.video_dict)
    
    if (st.session_state.video_dict['audio_path'] == ""):
        with open("chatlogs/current_chat.txt","w") as new_chat:
            new_chat.write(".")

 
    if(st.session_state.video_dict['transcription'] != ""):
        #get transcription
        with open(f"transcriptions/transcription.txt","r") as transcription:
            video_content = transcription.read()
        pre_prompt = f"The name of the YouTube video you learned is: {st.session_state.video_dict['audio_name']}. This is the transcript: "
        
        #Read to pre-prompt chat GPT
        messages.append({"role":"system","content":f"{pre_prompt}{video_content}" })
        
        #Load current chat
        try:
            with open("chatlogs/current_chat.txt","r") as chat:
                history = chat.read()
            history = history.split("£")
            for i,item in enumerate(history):
                text = item.split("|")
            
                if(i%2 == 0):
                    if len(text[-1]) > 1:
                        st.chat_message("user").write(text[-1])

                else:
                    st.chat_message("KLEM",avatar=avatar).write(text[-1])
        except:
            with open("chatlogs/current_chat.txt","a") as first_chat:
                first_chat.write(f"You|Analyze this video for me: {st.session_state.video_dict['audio_name']}£")
                first_chat.write(f"Chat Gpt|All analyzed! Ask me anything!£")
            with open("chatlogs/current_chat.txt","r") as chat:
                history = chat.read()
            history = history.split("£")
            user_avatar = Image.open("data/user_avatar.png")
            for i,item in enumerate(history):
                text = item.split("|")
            
                if(i%2 == 0):
                    if len(text[-1]) > 1:
                        st.chat_message("user").write(text[-1])

                else:
                    st.chat_message("KLEM",avatar=avatar).write(text[-1])
                
        
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
            

   
    else:
        # if(transcript_exists):
        #     transcript_exists = False
        #     st.experimental_rerun()
        youtube_url = st.text_input(label='To start, input a YouTube link. :point_down:')

        if st.button('Feed Klem :robot_face:'):
            st.chat_message("KLEM",avatar=avatar).write(KLEM)
            st.write("\n\n\n\n\n\n")
            with st.spinner("KLEM is fetching data from the video..."):
                gsa.download_youtube_audio(youtube_url)


            audio_path = st.session_state.video_dict['audio_path']
            audio_name = st.session_state.video_dict['audio_name']
            with st.spinner("KLEM is analyzing the video..."):
                _, paths = gsa.segment_audio(audio_path, audio_name)
                st.session_state.video_dict['clip_paths'] = gsa.sort_clip_paths_by_order(paths)

            with st.spinner("Klem is learning..."):
                gsa.transcribe_audio_segments()

            output_name = st.session_state.video_dict['audio_name']
            data = st.session_state.video_dict['transcription']
            output_name = output_name.replace("?","").replace("|","")
            with open(f"transcriptions/transcription.txt", "w") as transcription:
                transcription.write(data)    
            st.experimental_rerun()
            

 
        
    


#==============================================================================================

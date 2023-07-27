import streamlit as st
import os
import speech_recognition as speech_recon
import json
from pytube import YouTube
from moviepy.editor import *
from pydub.silence import split_on_silence
from moviepy.editor import *
from pydub import AudioSegment
import concurrent.futures
from tqdm import tqdm

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            print(f"Directory '{directory_path}' created successfully.")
        except OSError as e:
            print(f"Error: Failed to create directory '{directory_path}': {e}")
    else:
        print(f"Directory '{directory_path}' already exists.")

# Example usage:
VIDEO_OUTPUT_PATH = os.path.abspath(os.path.join('data', 'youtube'))
create_directory_if_not_exists(VIDEO_OUTPUT_PATH)

def download_youtube_video(youtube_url: str, output_path=VIDEO_OUTPUT_PATH):
    try:
        yt = YouTube(youtube_url)
        audio_mp4 = yt.streams.filter(only_audio=True)[1].download(output_path=output_path)
        return yt.title, audio_mp4
    except:
        pass

def split_audio_from_video(video_path, output_path=VIDEO_OUTPUT_PATH):
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio_name = os.path.basename(video_path).split('.')[0]
        audio_path = os.path.join(output_path, f'{audio_name}.wav')
        audio.write_audiofile(audio_path)
        return audio_path
    except Exception as e:
        print(e)

def segment_audio(audio_path, audio_name, min_silence_len=700, silence_thresh=-50, output_path=VIDEO_OUTPUT_PATH):
    print(f"Trying to load audio from: {audio_path}")  # Add this print statement
    audio = AudioSegment.from_file(audio_path,format="mp4")
    segments = split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    
    output_directory = os.path.join(output_path, f'{audio_name}_clips')
    output_paths = []
    output_directory = output_directory.replace("\\","/")
    display_path = output_directory.replace("?", "").replace("|","")
    print("Display path:", display_path)   
    output_directory = display_path
    
    try:
        os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist
        # Or do other operations with the original_path
    except OSError as e:
        print("Error:", e)
    
  
    for i, seg in enumerate(segments):
        output_file = os.path.join(output_directory, f'seg{i:04d}.wav')
        try:
            seg.export(output_file, format='wav')
            output_paths.append(output_file)
        except:
            print(f'The path {output_directory} is not valid')
    print(f'Audio segments are saved in {output_directory}')
    return segments, output_paths

def concatenate_audio_segments(audios_path, audio_name, output_path='data/youtube'):
    audios = sorted(audios_path, key=lambda x: int(os.path.basename(x).split('.')[0][-4:]))
    audio_segments = [AudioSegment.from_wav(audio) for audio in audios]
    combined_audio = sum(audio_segments)
    combined_audio.export(os.path.join(output_path, f'{audio_name}_enhanced.wav'), format='wav')

def download_youtube_audio(youtube_url):
    try:
        audio_name, audio_path = download_youtube_video(youtube_url)
        print(f"Downloaded audio path: {audio_path}")  # Add this print statement
        st.session_state.video_dict['audio_name'] = audio_name
        st.session_state.video_dict['audio_path'] = audio_path
        st.text(f'Youtube Video: {audio_name}')
    except:
        st.text('Please enter a valid youtube link')


def sort_clip_paths_by_order(clip_paths):
    return sorted(clip_paths, key=lambda x: int(os.path.basename(x).split('.')[0][-4:]))


def transcribe_audio_segments():
    def transcribe_single_audio(path):
        r = speech_recon.Recognizer()
        with speech_recon.AudioFile(path) as source:
            audio_text = r.listen(source)
            final_text = r.recognize_google(audio_data=audio_text)
            return final_text

    transcription = ''
    clip_paths = st.session_state.video_dict['clip_paths']

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Start transcribing each audio segment concurrently
        futures = [executor.submit(transcribe_single_audio, path) for path in clip_paths]

        # Wait for all transcriptions to complete
        concurrent.futures.wait(futures)

        # Retrieve the results and combine them
        for future in futures:
            final_text = future.result()
            transcription += ' ' + final_text + '\n'

    st.session_state.video_dict['transcription'] = transcription
    # st.text('Transcription has generated. You can read the transcription below or download it.')
    # with st.expander("Transcription"):
    #     st.write(transcription)

def save_to_txt(data: dict, name: str, path: str = VIDEO_OUTPUT_PATH):
    path = path.replace("\\","/")
    name = name.replace("?", "").replace("|","")
    with open(f"{path}/{name}.json", "w") as f:
        json.dump(data, f)
import streamlit as st
import os
import speech_recognition as speech_recon
import json
from pytube import YouTube
from moviepy.editor import *
from pydub.silence import split_on_silence
from moviepy.editor import *
from pydub import AudioSegment
from youtube_transcript_api import YouTubeTranscriptApi as ytt


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
VIDEO_OUTPUT_PATH = os.path.join('data', 'youtube')
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
        output_path = os.path.join(output_path, audio_name)
        audio_path = f'{output_path}.wav'
        audio.write_audiofile(audio_path)
        return audio_path
    except Exception as e:
        print(e)

def segment_audio(audio_path, audio_name, min_silence_len=700, silence_thresh=-50, output_path=VIDEO_OUTPUT_PATH):
    audio = AudioSegment.from_file(audio_path)
    segments = split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    
    output_path = os.path.join(output_path, audio_name)
    output_directory = f'{output_path}_clips'
    output_paths = []
    os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist
    for i, seg in enumerate(segments):
        output_file = os.path.join(output_directory, f'seg{i:04d}.wav')
        try:
            seg.export(output_file, format='wav')
            output_paths.append(output_file)
        except:
            print(f'The path {output_directory} is not valid')
    print(f'Audio segments are saved in {output_directory}')
    return segments, output_paths

def concatenate_audio_segments(audios_path, audio_name, output_path=os.path.join('data', 'youtube')):
    audios = sorted(audios_path, key=lambda x: int(os.path.basename(x).split('.')[0][-4:]))
    audio_segments = [AudioSegment.from_wav(audio) for audio in audios]
    combined_audio = sum(audio_segments)
    output_path = os.path.join(output_path, audio_name)
    combined_audio.export(f'{output_path}_enhanced.wav', format='wav')

def download_youtube_audio(youtube_url):
    try:
        audio_name, audio_path = download_youtube_video(youtube_url)
        st.session_state.video_dict['audio_name'] = audio_name
        st.session_state.video_dict['audio_path'] = audio_path
        st.text(f'Youtube Video: {audio_name}')
    except:
        st.text('Please enter a valid youtube link')


def sort_clip_paths_by_order(clip_paths):
    return sorted(clip_paths, key=lambda x: int(os.path.basename(x).split('.')[0][-4:]))


def transcribe_audio_segments():
    transpcription = '  '
    r = speech_recon.Recognizer()
    for path in st.session_state.video_dict['clip_paths']:
        with speech_recon.AudioFile(path) as source:
            audio_text = r.listen(source)
            final_text = r.recognize_google(audio_data=audio_text)
            transpcription += ' ' + final_text + '\n'
    st.session_state.video_dict['transcription'] = transpcription
    st.text('Transcription has generated. You can read the transcription below or download it.')
    with st.expander("Transcription"):
        st.write(transpcription)

def save_to_txt(data: dict, name: str, path: str = VIDEO_OUTPUT_PATH):
    output_path = os.path.join(path, name)
    with open(f"{path}.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    OUTPUT_PATH = VIDEO_OUTPUT_PATH
    st.title('Tell me your Youtube video:')
    youtube_url = st.text_input(label='Youtube Link')

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


    if st.button('Get the transcription'):
        # if 'audio_path' in st.session_state.video_dict:
        with st.spinner("CLEM is fetching data from the video..."):
            download_youtube_audio(youtube_url)


        # if 'clip_paths' in st.session_state.video_dict and len(st.session_state.video_dict['clip_paths']) != 0:
        audio_path = st.session_state.video_dict['audio_path']
        st.write(f'The audio_path is : {audio_path}')
        print(f'The audio_path is : {audio_path}')
        audio_name = st.session_state.video_dict['audio_name']
        message = st.text("Please wait while CLEM is analyzing the video...")
        with st.spinner("CLEM is analyzing the video..."):
            _, paths = segment_audio(audio_path, audio_name)
            st.session_state.video_dict['clip_paths'] = sort_clip_paths_by_order(paths)
        message.text('Analysis has completed. CLEM is transcribing the video now.')

        # if 'transcription' in st.session_state.video_dict and len(st.session_state.video_dict['transcription']) == 0:
        with st.spinner("Transcribing..."):
            transcribe_audio_segments()

        output_name = st.session_state.video_dict['audio_name']
        data = st.session_state.video_dict['transcription']
        save_to_txt(data, output_name)

        # Provide a download link for the transcribed text
        data_for_doanlowd = data.replace(' ', '%20')
        st.markdown(f'<a href="data:application/octet-stream,{data_for_doanlowd}" download="{output_name}.txt">Download Transcription</a>', unsafe_allow_html=True)

    st.divider()

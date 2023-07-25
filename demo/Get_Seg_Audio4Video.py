from pytube import YouTube
from moviepy.editor import *
from pydub.silence import split_on_silence
from pydub.playback import play
import Upload_Audio as UA
from io import BytesIO
from moviepy.editor import *
from pydub import AudioSegment
import torch
import torchaudio
import os


def download_youtube_video(youtube_url: str, output_path='youtube/'):
    try:
        yt = YouTube(youtube_url)
        audio_mp4 = yt.streams.filter(only_audio=True)[1].download(output_path=output_path)
        return yt._title, audio_mp4
    except:
        pass


def segment_audio(audio_path, audio_name, min_silence_len=400, silence_thresh=-50, output_path='youtube'):
    audio = AudioSegment.from_file(audio_path)
    segments = split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    
    output_directory = f'{output_path}/{audio_name}_enhanced'
    os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist
    for i, seg in enumerate(segments):
        output_file = os.path.join(output_directory, f'seg{i:04d}.wav')
        try:
            seg.export(output_file, format='wav')
        except:
            print(f'The path {output_file} is not valid')
    print(f'Audio segments are saved in {output_directory}')
    return output_directory


def concatenate_audio_segments(audios_path, audio_name, output_path='youtube'):
    audios = [audio for audio in os.listdir(audios_path) if audio.endswith('.wav')]
    audios = sorted(audios, key=lambda x: os.path.basename(x).split('.')[0])
    concatenated_audio = AudioSegment.empty()
    for audio in audios:
        audio_segment = AudioSegment.from_wav(os.path.join(audios_path, audio))
        concatenated_audio += audio_segment
    concatenated_audio.export(os.path.join(output_path, f'{audio_name}_enhanced.wav'))
    
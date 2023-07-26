from pytube import YouTube
from moviepy.editor import *
from pydub.silence import split_on_silence
from moviepy.editor import *
from pydub import AudioSegment
import os


def download_youtube_video(youtube_url: str, output_path='youtube/'):
    try:
        yt = YouTube(youtube_url)
        audio_mp4 = yt.streams.filter(only_audio=True)[1].download(output_path=output_path)
        return yt._title, audio_mp4
    except:
        pass


def split_audio_from_video(video_path, output_path='youtube/'):
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio_name = os.path.basename(video_path).split('.')[0]
        audio_path = f'{output_path}/{audio_name}.wav'
        audio.write_audiofile(audio_path)
        return audio_path
    except Exception as e:
        print(e)


def segment_audio(audio_path, audio_name, min_silence_len=700, silence_thresh=-50, output_path='youtube'):
    audio = AudioSegment.from_file(audio_path)
    segments = split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    
    output_directory = f'{output_path}/{audio_name}_clips'
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


def concatenate_audio_segments(audios_path, audio_name, output_path='youtube'):
    audios = sorted(audios_path, key=lambda x: int(os.path.basename(x).split('.')[0][-4:]))
    audio_segments = [AudioSegment.from_wav(audio) for audio in audios]
    combined_audio = sum(audio_segments)
    combined_audio.export(f'output_path/{audio_name}_enhanced', format='wav')
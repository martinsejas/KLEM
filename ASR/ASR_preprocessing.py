import os
import librosa
import numpy as np
import pandas as pd
from glob import glob

def load_files(data_path='./Data/*.wav'):
    audio_files = glob(data_path)
    labels = []
    
    for file in audio_files:
        labels.append(file.split('/')[-1][:3]) # suppose we have paths like: './Data/user/user.wav'
    return audio_files, labels


def slice_audio(audio, partitions, scaled_sr):
    my_list = [None] * partitions
    for i in range(partitions):
        my_list[i] = audio[i * slice_audio : (i + 1) * slice_audio]
    return np.array(my_list)


def load_and_slice_audio(file_path, slice_duration=3):
    audio, sr = librosa.load(file_path)
    partitions = audio.shape[0] // (sr * slice_duration)
    scaled_sr = sr * slice_duration
    audios = slice_audio(audio, partitions=partitions, scaled_sr=scaled_sr)
    return audios, sr


def retrieve_features_and_labels(audios, sr: int):
    features = []

    for aud in audios:
        mfcc = librosa.feature.mfcc(y=aud,
                                    sr=sr,
                                    n_mfcc=13,
                                    hop_length=512,
                                    n_mels=26)
        features.append(mfcc)
    return features

def mel_freq(data_dir='./Data/') -> (np.ndarray, np.ndarray):
    features = []
    labels = []
    
    for class_label in os.listdir(data_dir):
        class_dir = os.path.join(data_dir, class_label)
        try:
            for filename in os.listdir(class_dir):
                file_path = os.path.join(class_dir, filename)
                
                audio, sr = load_and_slice_audio(file_path)
                
                features.extend(retrieve_features_and_labels(audio, sr))
                labels.append(class_label)
        except FileNotFoundError as e:
            print(e)
    return np.array(features), np.array(labels)


def get_mel_data(data_dir='./Data/'):
    features, labels = mel_freq(data_dir=data_dir)
    
    num_samples = features.shape[0]
    num_mfcc = features[0].shape[0]
    num_frames = features[0].shape[1]
    
    features_2d = np.reshape(features,
                             (num_samples, num_frames * num_mfcc))
    
    label_map = {x: i for i, x in enumerate(labels)}
    labels = [label_map[x] for x in labels]
    
    return features_2d, labels
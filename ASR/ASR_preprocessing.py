import os
import librosa
import numpy as np
import pandas as pd
from glob import glob


# The data files path should be like './Data/user/*.wav'
# so the label of each file should be like 'user'
def load_files(data_path='./Data/*.wav'):
    audio_files = glob(data_path)
    labels = []
    
    for file in audio_files:
        labels.append(file.split('/')[-1][:3]) # suppose we have paths like: './Data/user/user.wav'
    return audio_files, labels


def slice_audio(audio, partitions, sr_scaled):
    my_list = [None] * partitions
    for i in range(partitions):
        my_list[i] = audio[i * sr_scaled : (i + 1) * sr_scaled]
    return np.array(my_list)

# Keep these commented out for now, as I will optimize the code later to make it more easily readable
# def load_and_slice_audio(file_path, slice_duration=3):
#     audio, sr = librosa.load(file_path)
#     partitions = audio.shape[0] // (sr * slice_duration)
#     scaled_sr = sr * slice_duration
#     audios = slice_audio(audio, partitions=partitions, sr_scaled=scaled_sr)
#     return audios, sr


# def retrieve_features_and_labels(audios, sr: int):
#     features = []

#     for aud in audios:
#         mfcc = librosa.feature.mfcc(y=aud,
#                                     sr=sr,
#                                     n_mfcc=13,
#                                     hop_length=512,
#                                     n_mels=26)
#         features.append(mfcc)
#     return features

# def mel_freq(data_dir='./Data/') -> (np.ndarray, np.ndarray):
#     features = []
#     labels = []
    
#     for class_label in os.listdir(data_dir):
#         class_dir = os.path.join(data_dir, class_label)
#         try:
#             for filename in os.listdir(class_dir):
#                 file_path = os.path.join(class_dir, filename)
                
#                 audio, sr = load_and_slice_audio(file_path)
                
#                 features.extend(retrieve_features_and_labels(audio, sr))
#                 labels.append(class_label)
#         except FileNotFoundError as e:
#             print(e)
#     return np.array(features), np.array(labels)


def mel_freq(data_dir='./Data/'):
    features = []
    labels = []
    
    for audio_file in os.listdir(data_dir)[1:]:
        label = audio_file.split('.')[0]
        file_path = os.path.join(data_dir, audio_file)
        # Load the audio file
        audio, sr = librosa.load(file_path)
        partitions = audio.shape[0] // (sr * 3)
        sr_sliced = sr * 3
                
        audios = slice_audio(audio,
                            partitions=partitions,
                            sr_scaled=sr_sliced)

        for aud in audios:
            # Extract MFCC features
            mfcc = librosa.feature.mfcc(y=aud,
                                        sr=sr,
                                        n_mfcc=13,
                                        hop_length=512,
                                        n_mels=26)
            # Append the features and label to the lists
            features.append(mfcc)
            labels.append(label)
    return np.array(features), np.array(labels)


def get_mel_data(data_dir='./Data/'):
    features, labels = mel_freq(data_dir=data_dir)
    
    num_samples = features.shape[0]
    num_mfcc = features[0].shape[0]
    num_frames = features[0].shape[1]
    
    features_2d = np.reshape(features,
                             (num_samples, num_frames * num_mfcc))
    
    label_map = {'NonHuman': 0, 'Human': 1}
    labels = np.array(label_map['NonHuman'] if 'NonSpeech' in value else label_map['Human'] for value in labels)
    
    return features_2d, labels


"""
This is the same as get_mel_data, but for the inference data by default it's in the inference folder.
"""
def get_mel_infer_data(data_dir='./inference/'):
    features_, labels_ = mel_freq(data_dir)
    
    num_samples = features_.shape[0]
    num_mfcc = features_[0].shape[0]
    num_frames = features_[0].shape[1]

    features_inf_2d = np.reshape(features_, (num_samples, num_frames * num_mfcc))
    
    label_map = {'NonHuman': 0, 'Human': 1}
    labels_inf = np.array([label_map['NonHuman'] if 'NonSpeech' in value else label_map['Human'] for value in labels_])
    return features_inf_2d, labels_inf
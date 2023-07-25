import streamlit as st
import Get_Seg_Audio4Video as gsa
import Upload_Audio as UA
import os
import soundfile as sf


st.title('Paste your video link here:')
youtube_url = st.text_input(label='Youtube Link')

try:
    with st.spinner("Downloading audio..."):
        audio_name, audio = gsa.download_youtube_video(youtube_url)
        st.write(f'Youtube video title: {audio_name}')
except:
    st.write('Please enter a valid youtube link')

st.divider()

if st.button('Get Cleaned Audio'):
    segments_root = gsa.segment_audio(audio, audio_name)
    # audio_segments, sr = gsa.segment2bytesio(segments)
    #TODO: Need to pass the audio segments to the model of speech detection first, then pass the segments to speech enhancement model
    # get all files' path in the segments_root
    segments_path = []
    for filename in os.listdir(segments_root):
        dirpath = os.path.join(segments_root, filename)
        segments_path.append(dirpath)
    segments_path = sorted(segments_path, key=lambda x: os.path.basename(x).split('.')[0])
    # Now, I just pass the segments to speech enhancement model
    
    total_length = len(segments_path)
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0)
    
    for i, path in enumerate(segments_path):
        audio_segs_enhanced = UA.model.separate_file(path)
        os.makedirs(f'youtube/{audio_name}_enhanced/', exist_ok=True)
        # enhanced_data = enhanced_audio[:,:].detach().cpu().squeeze()
        # sf.write("data/clean.wav",enhanced_data,samplerate=8000)
        enhanced_data = audio_segs_enhanced[:,:].detach().cpu().squeeze()
        # sf.write(f'youtube/{audio_name}_enhanced/seg{i}.wav', enhanced_data, samplerate=8000)
        
        my_bar.progress((i+1)/total_length)
    
    st.write('Audio Has Segmented')

if st.button('Retrieve Audio Segments'):
    st.write(f'youtube/{audio_name}_enhanced/')
    st.write('Please waite while the audio segments are retrieved...')
    gsa.concatenate_audio_segments(audios_path=f'./youtube/{audio_name}_enhanced', audio_name=audio_name)
    st.write('Audio Segments Has Retrieved')
    st.audio(f'youtube/{audio_name}_enhanced/{audio_name}_enhanced.wav')
    

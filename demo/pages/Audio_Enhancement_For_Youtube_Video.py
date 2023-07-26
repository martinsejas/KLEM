import streamlit as st
import Get_Seg_Audio4Video as gsa
import Upload_Audio as UA
import os
import soundfile as sf
import speech_recognition as speech_recon



st.title('Paste your video link here:')
youtube_url = st.text_input(label='Youtube Link')

if 'clip_paths' not in st.session_state:
    st.session_state.clip_paths = []
# clip_paths = []

# Download the youtube video and save it in the "youtube" folder
try:
    audio_name, audio_path = gsa.download_youtube_video(youtube_url)
    # _, clip_paths = gsa.segment_audio(audio_path, audio_name)
    # clip_paths = sorted(clip_paths, key=lambda x: int(os.path.basename(x).split('.')[0][-4:]))
    st.write(f'Your Youtube video title: {audio_name}')
except:
    st.write('Please enter a valid youtube link')


# clip the audio into segments and sort the clips by the order of the segments

flag = st.button('Get Audio Segments')
if flag:
    st.write("Please wait while the audio segments are being extracted...")
    _, st.session_state.clip_paths = gsa.segment_audio(audio_path, audio_name)
    st.write('Audio Has Segmented')

if st.button('Generate the Transcription'):
    # _, st.session_state.clip_paths = gsa.segment_audio(audio_path, audio_name)
    st.session_state.clip_paths = sorted(st.session_state.clip_paths, key=lambda x: int(os.path.basename(x).split('.')[0][-4:]))
    transpcription = str()
    # flag = False
    with st.spinner("Transcribing audio..."):
        r = speech_recon.Recognizer()
        for i, path in enumerate(st.session_state.clip_paths):
            with speech_recon.AudioFile(path) as source:
                audio_text = r.listen(source)
                final_text = r.recognize_google(audio_data=audio_text)
                if transpcription == '':
                    transpcription += final_text
                transpcription += ' ' + final_text
                st.write(final_text + ' ')

st.divider()

if st.button('Get Cleaned Audio'):
    #TODO: Need to pass the audio segments to the model of speech detection first, then pass the segments to speech enhancement model
    # get all files' path in the segments_root
    st.session_state.clip_paths = sorted(st.session_state.clip_paths, key=lambda x: int(os.path.basename(x).split('.')[0][-4:]))
    # Now, I just pass the segments to speech enhancement model
    
    total_length = len(st.session_state.clip_paths)
    progress_text = "Audio is being cleaned..."
    my_bar = st.progress(0)
    
    os.makedirs(f'youtube/{audio_name}_enhanced/', exist_ok=True)
    for i, path in enumerate(st.session_state.clip_paths):
        clip_name = os.path.basename(path)
        audio_segs_enhanced = UA.model.separate_file(path, savedir=f'youtube/{audio_name}_enhanced/')
        # enhanced_data = audio_segs_enhanced[:,:].detach().cpu().squeeze()
        # sf.write(f'youtube/{audio_name}_enhanced/{clip_name}',enhanced_data,samplerate=8000)
        my_bar.progress((i+1)/total_length, text=progress_text)
    
    st.write('Audio Has Segmented')


st.divider()


if st.button('Retrieve Audio Segments'):
    st.write('Please waite while the audio segments are retrieved...')
    gsa.concatenate_audio_segments(audios_path=st.session_state.clip_paths, audio_name=audio_name)
    st.write('Audio Segments Has Retrieved in One File')
    st.audio(f'youtube/{audio_name}_enhanced.wav')




import streamlit as st
import Get_Seg_Audio4Video as gsa
import Upload_Audio as UA
import os
import soundfile as sf
import speech_recognition as speech_recon
import json


def download_youtube_audio(youtube_url):
    try:
        audio_name, audio_path = gsa.download_youtube_video(youtube_url)
        st.session_state.video_dict['audio_name'] = audio_name
        st.session_state.video_dict['audio_path'] = audio_path
        st.text(f'Youtube Video: {audio_name}')
    except:
        st.text('Please enter a valid youtube link')

def sort_clip_paths_by_order(clip_paths):
    return sorted(clip_paths, key=lambda x: int(os.path.basename(x).split('.')[0][-4:]))

def transcribe_audio_segments():
    with st.spinner("Transcribing audio..."):
        transpcription = ' '
        r = speech_recon.Recognizer()
        for path in st.session_state.video_dict['clip_paths']:
            with speech_recon.AudioFile(path) as source:
                audio_text = r.listen(source)
                final_text = r.recognize_google(audio_data=audio_text)
                transpcription += ' ' + final_text
        st.session_state.video_dict['transcription'] = transpcription
        st.text('Transcription Has Generated')
        with st.expander("Transcription"):
            st.write(transpcription)


def save_to_txt(data: dict, name: str, path: str = 'youtube'):
    with open(f"{path}/{name}.txt", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    OUTPUT_PATH = 'youtube/'
    st.title('Paste your video link here:')
    youtube_url = st.text_input(label='Youtube Link')

    if 'video_dict' not in st.session_state:
        st.session_state.video_dict = {}

    if st.button('Download Audio'):
        download_youtube_audio(youtube_url)

    if 'clip_paths' in st.session_state.video_dict:
        st.text('Segments are already extracted.')
    else:
        st.text('Segments are not extracted yet.')
    
    # Clip the audio into segments and sort the clips by the order of the segments
    if st.button('Get Audio Segments'):
        if 'audio_path' in st.session_state.video_dict and 'audio_name' in st.session_state.video_dict:
            audio_path = st.session_state.video_dict['audio_path']
            audio_name = st.session_state.video_dict['audio_name']
            message = st.text("Please wait while the audio segments are being extracted...")
            _, paths = gsa.segment_audio(audio_path, audio_name)
            st.session_state.video_dict['clip_paths'] = sort_clip_paths_by_order(paths)
            message.text('Audio Has Segmented')
    
    # Generate the transcription
    output_name = st.session_state.video_dict['audio_name']
    data = st.session_state.video_dict['transcription']
    if st.button('Generate the Transcription'):
        if 'clip_paths' in st.session_state.video_dict:
            transcribe_audio_segments()
        save_to_txt(data, output_name)
    st.download_button(label='Download Transcription',
                        data=data,
                        file_name=output_name+'.txt',
                        mime='application/json')
    # st.session_state.clear()
    st.divider()




# if st.button('Get Cleaned Audio'):
#     #TODO: Need to pass the audio segments to the model of speech detection first, then pass the segments to speech enhancement model
#     # get all files' path in the segments_root
#     st.session_state.video_dict['clip_paths'] = sorted(st.session_state.video_dict['clip_paths'], key=lambda x: int(os.path.basename(x).split('.')[0][-4:]))
#     # Now, I just pass the segments to speech enhancement model
    
#     total_length = len(st.session_state.video_dict['clip_paths'])
#     progress_text = "Audio is being cleaned..."
#     my_bar = st.progress(0)
    
#     os.makedirs(f'youtube/{audio_name}_enhanced/', exist_ok=True)
#     for i, path in enumerate(st.session_state.video_dict['clip_paths']):
#         clip_name = os.path.basename(path)
#         audio_segs_enhanced = UA.model.separate_file(path, savedir=f'youtube/{audio_name}_enhanced/')
#         # enhanced_data = audio_segs_enhanced[:,:].detach().cpu().squeeze()
#         # sf.write(f'youtube/{audio_name}_enhanced/{clip_name}',enhanced_data,samplerate=8000)
#         my_bar.progress((i+1)/total_length, text=progress_text)
    
#     st.write('Audio Has Segmented')


# st.divider()


# if st.button('Retrieve Audio Segments'):
#     st.write('Please waite while the audio segments are retrieved...')
#     gsa.concatenate_audio_segments(audios_path=st.session_state.video_dict['clip_paths'], audio_name=audio_name)
#     st.write('Audio Segments Has Retrieved in One File')
#     st.audio(f'youtube/{audio_name}_enhanced.wav')




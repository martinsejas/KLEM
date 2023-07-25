import os
import pyaudio
import wave

def record_audio(filename, duration=15, sample_rate=44100, chunk_size=1024):
    audio_format = pyaudio.paInt16
    channels = 1

    audio = pyaudio.PyAudio()

    stream = audio.open(format=audio_format,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk_size)

    print(f"Recording {filename}...")

    frames = []
    for i in range(0, int(sample_rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)

    print(f"Finished recording {filename}")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recording to a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(audio_format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

if __name__ == "__main__":
    train_folder = "train"
    test_folder = "test"

    if not os.path.exists(train_folder):
        os.makedirs(train_folder)

    if not os.path.exists(test_folder):
        os.makedirs(test_folder)

    num_train_recordings = 20
    num_test_recordings = 5
    recording_duration = 15

    # Record and save files for the train folder
    for i in range(1, num_train_recordings + 1):
        filename = os.path.join(train_folder, f"{i}.wav")
        record_audio(filename, duration=recording_duration)

    # Record and save files for the test folder
    for i in range(num_train_recordings + 1, num_train_recordings + num_test_recordings + 1):
        filename = os.path.join(test_folder, f"{i}.wav")
        record_audio(filename, duration=recording_duration)

    print(f"{num_train_recordings} recordings saved to the 'train' folder.")
    print(f"{num_test_recordings} recordings saved to the 'test' folder.")

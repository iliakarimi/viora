import sounddevice as sd
import numpy as np
import wave
import whisper
import time

# Load Whisper model (tiny for low CPU usage)
model = whisper.load_model("tiny")

# Audio recording settings
SAMPLE_RATE = 16000  # Sampling rate
FRAME_DURATION = 3.0  # Recording duration of each frame (seconds)
SILENCE_THRESHOLD = 450  # Silence detection threshold (less than this value means silence)

def is_silent(audio_chunk):
    """ Checks whether the sound is silence or not. """
    return np.abs(audio_chunk).mean() < SILENCE_THRESHOLD

def record_until_silence(file_path="stt/temp_audio.wav", silence_timeout=1.0):
    """ It records the user's voice and stops when there is silence. """
    print(" Start recording... speak!")

    audio_data = []
    last_sound_time = time.time()

    while True:
        frame = sd.rec(int(SAMPLE_RATE * FRAME_DURATION), samplerate=SAMPLE_RATE, channels=1, dtype=np.int16)
        sd.wait()
        audio_data.append(frame)

        if not is_silent(frame):
            last_sound_time = time.time()  # User is still talking
        elif time.time() - last_sound_time > silence_timeout:
            break  # If there is silence for more than `silence_timeout` seconds, the recording will stop.

    print(" Recording finished! Now processing...")

    # Save to WAV file
    audio_np = np.concatenate(audio_data, axis=0)
    with wave.open(file_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_np.tobytes())

    return file_path

def transcribe_audio(file_path='stt/temp_audio.wav'):
    """ Convert audio file to text using local Whisper model. """
    result = model.transcribe(file_path)
    return result["text"]



from openai import api_key

client = api_key("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")
audio_file = open("/path/to/file/german.mp3", "rb")

translation = client.audio.translations.create(
    model="whisper-1", 
    file=audio_file,
)

print(translation.text)
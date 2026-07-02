import os
import json
import soundfile as sf
import sounddevice as sd
from dotenv import load_dotenv
from deepgram import DeepgramClient


load_dotenv()


with open("configs/tts_setting.json", "r") as r:
    tts_configs = json.load(r)

voice_select = tts_configs["voice_select"]
Sample_Rate = tts_configs["sample_rate"]
encoding = tts_configs["encoding"]



def ttsplayer(file_path):
    """ Play Audio file """
    try:
        data, fs = sf.read(file_path, dtype='float32')  
        sd.play(data, fs)
        status = sd.wait()  # Wait until file is done playing
    except Exception as e:
        print("An error happend: " + e)


def main_tts(text):
    
    SPEAK_TEXT = text
    filename = "logs/response.mp3"

    try:
        load_dotenv()
        client = DeepgramClient(api_key=os.getenv("DEEPGRAM_API"))

        response = client.speak.v1.audio.generate(
            text=SPEAK_TEXT,
            model=voice_select,
            sample_rate=Sample_Rate,
            encoding=encoding
        )

        # Save the audio file
        with open(filename, "wb") as audio_file:
            # Iterate through the generator and write chunks
            for chunk in response:
                audio_file.write(chunk)
        ttsplayer(filename)

    except Exception as e:
        print("An error happend: " + e)

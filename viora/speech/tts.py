import os
import json
import pygame
from dotenv import load_dotenv
from deepgram import DeepgramClient

with open("configs/tts_setting.json", "r") as r:
    tts_configs = json.load(r)


load_dotenv()




TTSvolume = tts_configs["tts_volume"]
voice_select = tts_configs["voice_select"]
Sample_Rate = tts_configs["sample_rate"]
encoding = tts_configs["encoding"]




pygame.mixer.init()
class TTSPlayer:
    def __init__(self):
        self.current_sound = None

    def play(self, file_path):
        """ Play Audio file """
        if self.current_sound:
            self.stop()
        
        self.current_sound = pygame.mixer.Sound(file_path)
        self.current_sound.set_volume(TTSvolume)
        self.current_sound.play()



    def stop(self):
        """ Stop Audio file"""
        if self.current_sound:
            self.current_sound.stop()
            self.current_sound = None
tts_player = TTSPlayer()


def modeltts(respond):
    
    SPEAK_TEXT = respond
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
        tts_player.play(filename)
        while pygame.mixer.get_busy():
            pygame.time.delay(100)
        
    except Exception as e:
        print(f"Exception: {e}")

modeltts("Hey")
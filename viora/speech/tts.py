import os
import json
import pygame
from dotenv import load_dotenv
from deepgram import SpeakOptions
from deepgram import DeepgramClient

with open("configs/tts_setting.json", "r") as r:
    tts_configs = json.load(r)


load_dotenv()

TTSvolume = tts_configs["tts_volume"]
voice_select = tts_configs["voice_select"]

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
    filename = "logs/response.wav"

    try:
        load_dotenv()
        deepgram = DeepgramClient(os.getenv("DEEPGRAM_API"))

        options = SpeakOptions(
            model= voice_select,
        )

        response = deepgram.speak.rest.v("1").save(filename, SPEAK_TEXT, options)
        tts_player.play(filename)
        while pygame.mixer.get_busy():
            pygame.time.delay(100)
        
    except Exception as e:
        print(f"Exception: {e}")

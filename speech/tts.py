import os
import pygame
from dotenv import load_dotenv
from deepgram import SpeakOptions
from deepgram import DeepgramClient


load_dotenv()


pygame.mixer.init()
class TTSPlayer:
    def __init__(self):
        self.current_sound = None

    def play(self, file_path):
        """ Play Audio file """
        if self.current_sound:
            self.stop()
        
        self.current_sound = pygame.mixer.Sound(file_path)
        self.current_sound.set_volume(15.0)
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
            model="aura-2-andromeda-en",
        )

        response = deepgram.speak.rest.v("1").save(filename, SPEAK_TEXT, options)
        tts_player.play(filename)
        while pygame.mixer.get_busy():
            pygame.time.delay(100)
        
    except Exception as e:
        print(f"Exception: {e}")

import os
from time import sleep
import pygame
from deepgram.utils import verboselogs
from deepgram import DeepgramClient, SpeakOptions
from dotenv import load_dotenv

pygame.mixer.init()

class TTSPlayer:
    def __init__(self):
        self.current_sound = None  # Save the played file

    def play(self, file_path):
        """ Play Audio file """
        if self.current_sound:  # If the previous sound has been played, stop.
            self.stop()
        
        self.current_sound = pygame.mixer.Sound(file_path)
        self.current_sound.play()



    def stop(self):
        """ Stop Audio file"""
        if self.current_sound:
            self.current_sound.stop()
            self.current_sound = None


tts_player = TTSPlayer()

def modeltts(respond):
    
    SPEAK_TEXT = respond
    filename = "tts/response.wav"

    try:
        # STEP 1 Create a Deepgram client using the API key from environment variables
        load_dotenv()
        deepgram = DeepgramClient(os.getenv("DEEPGRAM_API"))

        # STEP 2 Call the save method on the speak property
        options = SpeakOptions(
            model="aura-2-andromeda-en",
        )

        response = deepgram.speak.rest.v("1").save(filename, SPEAK_TEXT, options)
        tts_player.play(filename)
        while pygame.mixer.get_busy():
            pygame.time.delay(100)
        
    except Exception as e:
        print(f"Exception: {e}")


import os
import openai
import dotenv
from deepgram import DeepgramClient

def get_openai_key():
    dotenv.load_dotenv()

    openai.api_key = os.getenv("OPENAI_API_KEY")

def get_deepgram_key():
    dotenv.load_dotenv()

    DeepgramClient(os.getenv("DEEPGRAM_API"))
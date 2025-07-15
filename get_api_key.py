import os
import openai
import dotenv


dotenv.load_dotenv()

def get_openai_key():
    openai.api_key = os.getenv("OPENAI_API_KEY")

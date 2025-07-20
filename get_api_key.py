import os
import dotenv


dotenv.load_dotenv()

def get_openai_key():
    os.getenv("OPENAI_API_KEY")

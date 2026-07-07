import os
import json
import dotenv
from utils.encode import encode_image
from utils.snapshot import __screen_picture
from configs.model_sys_text import system_text
from openai import OpenAI, APIConnectionError, RateLimitError, APITimeoutError


dotenv.load_dotenv()

key=str(os.getenv("OPENAI_API_KEY"))


client = OpenAI(
    api_key=key
    )


with open("configs/models.json", "r") as mc:
    model_conf = json.load(mc)

model_name = model_conf["GPT"]



def openai_response(input="", model_name = model_name, stream=False):
    
    __screen_picture()
    image_f = "logs/snapshot.png"
    base64_image = encode_image(image_f)
    
    try:
        response = client.responses.create(
            model=model_name,
            input=[
                {
                    "role": "developer",
                    "content": system_text
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": input},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    ]
                },
            ],
            stream=stream
            )

        model_reply = response.output_text

        with open("logs/response.json", "w") as wr:
            wr.write(model_reply)

    except APIConnectionError as e:

        print(f"API CONNECTION ERROR: {e}")
        
    except RateLimitError as e:
        print(f"OUT OF API RATE LIMIT: {e}")
        
    except APITimeoutError:
        print(f"API TIMEOUT ERROR: {e}")
        
    except Exception as e:
        print(f"Unexcpected Error: {e}")

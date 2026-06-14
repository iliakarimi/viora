import os
import json
import openai
import dotenv
from utils.encode import encode_image
from utils.snapshot import __screen_picture


dotenv.load_dotenv()

key=str(os.getenv("OPENAI_API_KEY"))


client = openai.OpenAI(
    api_key=key
    )


with open("configs/models.json", "r") as mc:
    model_conf = json.load(mc)
with open("configs/user_config.json", "r") as uc:
    user_conf = json.load(uc)


model_name = model_conf["GPT"]

user_os = user_conf["os"]
user_name = user_conf["user_name"]
screen_size = user_conf["screen_size"]


__screen_picture()
image_f = "logs/snapshot.png"
base64_image = encode_image(image_f)


def response_openai(input:str | None, model_name = "gpt-4.1-mini", stream=False):
    try:
        response = client.responses.create(
            model=model_name,
            input=[
                {
                    "role": "developer",
                    "content": user_conf
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
                }
            ],
            stream=stream
            )

        model_reply = response.output_text

        with open("logs/response.json", "w") as wr:
            wr.write(model_reply)

    except:

        if openai.APIConnectionError:
            print(f"API CONNECTION ERROR:")
        
        elif openai.RateLimitError:
            print("OUT OF API RATE LIMIT: Check your Billing Details at https://dashboard.openai.com")
        
        elif openai.APITimeoutError:
            print("API TIMEOUT ERROR: Check Your Internet Connection.")
        
        else:
            print("Unexcpected Error!")

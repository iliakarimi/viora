import os
import json
import openai
import dotenv

dotenv.load_dotenv

key=os.getenv("OPENAI_API_KEY")


client = openai.OpenAI(
    api_key=key
    )


with open("configs/models.json", "r") as mc:
    model_conf = json.load(mc)

model_name = model_conf["GPT"]


def response_openai(input:str | None, model_name = "gpt4.1-mini", stream=False):
    try:
        response = client.responses.create(
            model=model_name,
            input=input,
            stream=stream
            )

        model_reply = response.output_text

        with open("logs/response.json", "w") as wr:
            wr.write(model_reply)

    except:

        if openai.APIConnectionError:
            print("CONNECTION ERROR: ")
        
        elif openai.RateLimitError:
            print("OUT OF API RATE LIMIT: Check your Billing Details at https://dashboard.openai.com")
        
        elif openai.APITimeoutError:
            print("API TIMEOUT ERROR: Check Your Internet Connection.")
        
        else:
            print("Unexcpected Error!")

print(response_openai)
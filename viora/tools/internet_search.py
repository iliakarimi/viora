import os, sys
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

import json
import openai
from utils.cleanurl import clean_urls
from utils.get_api_key import get_openai_key
from memory.short_term_memory import ShortTermMemory


client = openai.OpenAI(
    api_key=get_openai_key()
)


with open("configs/models.json", "r") as modl:
    model_conf = json.load(modl)
with open('configs/initial_agent_data.json', 'r') as file:
    assistant_data = json.load(file)

short_term_memory = ShortTermMemory()

response_form = assistant_data["response_form"]
response_structure = assistant_data["response_structure"]
model_name = model_conf["GPT"]

def search_online(search_term):
    raw_internet_response = client.responses.create(
        model=model_name,
        tools=[{
            "type": "web_search_preview",
            "search_context_size": "low",
        }],
        input=[
            {"role": "user", "content": search_term}
        ],
    )
    raw_online_assistant_reply = raw_internet_response.output_text
    
    with open("logs/raw_online_response.txt", "w") as wr:
        wr.write(raw_online_assistant_reply)
    with open("logs/raw_online_response.txt", "r") as rr:
        raw_text = rr.read()
    raw_online_response_data = clean_urls(raw_text)
    internet_response = client.responses.create(
        model=model_name,
        input=[
            {"role": "system", "content": 
             "summarize the news into a single paragraph under 1800 characters."
             f"Respond {response_form} as instructed, following the {response_structure} for Respones structure."
             f"Respond **only** with a single JSON object, valid according to RFC 8259. "
             f"Use **only** double quotes for all keys and string values. "
             f"Do **not** include any single quotes or text outside the JSON. "
             },
            {"role": "user", "content": raw_online_response_data}
        ],
    )
    online_assistant_response = internet_response.output_text
    
    with open('logs/online_response.json', 'w') as wrfile:
        wrfile.write(online_assistant_response)
    with open('logs/online_response.json', 'r') as rrfile:
        online_response_data = json.load(rrfile)
    
    f_online_assistant_response = online_response_data["response"]
    
    online_assistant_reply = {"text": f"{f_online_assistant_response}"}

    short_term_memory.add_message("assistant", f_online_assistant_response)
    return online_assistant_reply

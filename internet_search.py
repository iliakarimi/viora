import json
import openai
from utils import clean_urls
from get_api_key import get_openai_key
from memory.short_term_memory import ShortTermMemory

client = openai.OpenAI(
    api_key=get_openai_key()
)

with open('configs/initial_agent_data.json', 'r') as file:
    assistant_data = json.load(file)

short_term_memory = ShortTermMemory()

response_form = assistant_data["response_form"]
response_structure = assistant_data["response_structure"]

def search_online(search_term):
    raw_internet_response = client.responses.create(
        model="gpt-4.1-mini",
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
        model="gpt-4.1-mini",
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



def needs_internet_check(user_input):
    internet_check_response = client.responses.create(
        model="gpt-4.1-nano",
        input=[
            {
                "role": "system",
                "content": (
                    "You are a classifier that determines whether the user's message requires real-time or online data to answer accurately.\n"
                    "If it DOES, respond only with 'YES'. If it DOES NOT, respond only with 'NO'.\n"
                    "Avoid any explanations.\n\n"
                    "Say 'YES' for questions that involve:\n"
                    "- Weather forecasts or current weather\n"
                    "- Recent news or trending topics\n"
                    "- Live sports scores or match info\n"
                    "- Flight, train, or bus schedules\n"
                    "- Stock prices, crypto values, or currency exchange rates\n"
                    "- Product availability or online shopping\n"
                    "- Website status or outages\n"
                    "- Real-time traffic or transit\n"
                    "- Searching for people, events, or places that are not widely known\n"
                    "- Looking for the latest information on specific companies, media, or technology\n"
                    "- Anything that depends on up-to-date or changing info\n\n"
                    "Say 'NO' for questions about:\n"
                    "- General knowledge (history, science, math, etc.)\n"
                    "- Definitions, explanations, or concepts\n"
                    "- Programming help or code generation\n"
                    "- Translation, grammar correction, or writing help\n"
                    "- Opinions, advice, or creative content\n"
                    "- Fictional characters or plots\n"
                    "- Anything not requiring recent or online data\n"
                    "- Asking a question by a user to someone who needs the internet, such as: 'Can you check tomorrow's weather in Tehran?', 'anya, can you search for me about iphone 17?'"
                )
            },
            
            {"role": "user", "content": user_input}
        ]
    )
    return internet_check_response.output_text

import os
import json
import openai
import requests
from dotenv import load_dotenv
from memory.short_term_memory import ShortTermMemory

client = openai.OpenAI()

with open('memory/fixed_memory.json', 'r') as file:
    assistant_data = json.load(file)

short_term_memory = ShortTermMemory()

assistant_name = assistant_data["name"]
user_name = assistant_data["user_name"]
about_user = assistant_data["about_user"]
assistant_goal = assistant_data["personality"]

short_term_memory.add_message(
    "system",
    f"You are {assistant_name}, a helpful assistant for {user_name}."
    f"If you wanted to use the word 'there' to call the user, use {user_name}."
    f"If you want to know about Ilia, use {about_user}."
    f"You have short-term memory. You can remember details during this session (short-term memory){short_term_memory}."
    "You only communicate with Ilia."
    "Ilia is your developer."
    "You can search on the Internet."
    f"Respond **only** with a single JSON object, valid according to RFC 8259. "
    f"Use **only** double quotes for all keys and string values. "
    f"Do **not** include any single quotes or text outside the JSON. "
    f"Follow this exact schema:\n"
    f"{{\n"
    f'  "response": "<string>",\n'
    f"}}"
)

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def execute_search_query(search_term):

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

    if not GOOGLE_API_KEY or not SEARCH_ENGINE_ID:
        return {"error": "Missing API keys. Check your environment variables."}

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": search_term,
        "key": GOOGLE_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "num": 3
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching search results: {e}"}

def search_online(search_term):

    search_data = execute_search_query(search_term)
    
    aggregated_details = ""
    if 'items' in search_data:
        details_list = []
        for entry in search_data['items']:
            title = entry.get('title', 'No Title')
            snippet = entry.get('snippet', 'No snippet available')
            link = entry.get('link', 'No link available')
            details = (
                f"Title: {title}\n"
                f"Snippet: {snippet}\n"
                f"Link: {link}\n"
            )
            details_list.append(details)
        aggregated_details = "\n".join(details_list)
    
    prompt_text = (
        f"User Query: {search_term}\n"
        f"Search Results:\n{aggregated_details}"
    )

    short_term_memory.add_message("user", prompt_text)
    internet_response = client.responses.create(
        model="gpt-4.1-mini",
        input=short_term_memory.get_messages()
    )
    online_assistant_reply = internet_response.output_text
    with open("online_response.json", "w") as wr:
        wr.write(online_assistant_reply)
    with open("online_response.json", "r") as rr:
        online_response_data = json.load(rr)
    online_assistant_reply = {"text": f"{online_response_data["response"]}"}

    short_term_memory.add_message("assistant", online_assistant_reply)
    return online_assistant_reply



def needs_internet_check(user_input):
    internet_check_response = client.responses.create(
        model="gpt-4.1-mini",
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



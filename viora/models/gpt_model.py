#This Script find Path Files
import os, sys
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))


import json
from openai import OpenAI
from speech.tts import modeltts
from utils.get_api_key import get_openai_key
from tools.internet_search import search_online
from tools.action import ComputerAnalyze, keyboard_control
from memory.short_term_memory import ShortTermMemory


client = OpenAI(
    api_key = get_openai_key()
    )


with open('configs/initial_agent_data.json', 'r') as file:
    assistant_data = json.load(file)
with open('configs/user_setup.json', 'r') as userfile:
    user_data = json.load(userfile)
short_term_memory = ShortTermMemory()

assistant_name = assistant_data["name"]
user_name = user_data["user_name"]
about_user = user_data["about_user"]
assistant_goal = assistant_data["personality"]
response_form = assistant_data["response_form"]
response_structure = assistant_data["response_structure"]
screen_vision = assistant_data["screen_vision"]
computer_control = assistant_data["computer_control"]
action_scheduling = assistant_data["action_scheduling"]
action_definitions = assistant_data["action_definitions"]
allowed_keys = assistant_data["allowed_keys"]

system_texts = [
    f"You are {assistant_name}, an agentic assistant for {user_name}. You are an agent — please keep going until the user's query is completely resolved before ending your turn. Only yield back when you're sure the task is complete.",
    f"Your personality: {assistant_goal}.",
    f"Refer to the user as '{user_name}' if needed.",
    f"If you need details about Ilia, use: {about_user}.",
    f"You have short-term memory: {short_term_memory}.",
    "You can search the Internet when needed With make 'True' in 'internet_search'.",
    f"Respond {response_form}, strictly following this structure: {response_structure}.",
    "Respond only with a single JSON object, valid according to RFC 8259.",
    "Do not include any single quotes, markdown, or any extra text outside the JSON.",
    "Never wrap responses in ```json or any kind of code block. Return plain raw JSON only.",
    "If you are not sure about file contents or code structure, use your tools to inspect files — do NOT guess.",
    f"{screen_vision}",
    f"{computer_control}",
    f"{action_scheduling}",
    f"{action_definitions}"
    # f"You are only allowed to simulate the following keys: {allowed_keys}"
]
for text in system_texts:
    short_term_memory.add_message("system", text)

import os
os.system("cls")


while True:
    # audio_path = record_until_silence()
    # user_input = transcribe_audio(audio_path)
    user_input = str(input("user: "))
    # print(f"{user_name}: {user_input}")

    short_term_memory.add_message("user", user_input)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=short_term_memory.get_messages()
    )

    assistant_reply = response.output_text

    with open("logs/response.json", "w") as wr:
        wr.write(assistant_reply)
    with open("logs/response.json", "r") as rr:
        response_data = json.load(rr)

    final_response = f"{json.dumps(response_data["response"])}"
    short_term_memory.add_message("assistant", json.dumps(response_data))
    print(f"{assistant_name}: {final_response}")
    modeltts(final_response)


    if response_data["internet_search"] == "True":
        online_assistant_reply = search_online(user_input)
        print(f"{assistant_name}: {online_assistant_reply}")
        modeltts(online_assistant_reply)
        short_term_memory.add_message("assistant", online_assistant_reply)

    while response_data["control_action"] == "True":
        ComputerAnalyze.screen_picture()
        ComputerAnalyze.screen_analyze()
        with open('logs/analyze_screen.txt', 'r') as cr:
            analyze_data = cr.read()
        short_term_memory.add_message("assistant", analyze_data)

        control_response = client.responses.create(
            model="gpt-4.1-mini",
            input=short_term_memory.get_messages()
        )
        control_assistant_reply = control_response.output_text


        with open("logs/response.json", "w") as wc:
            wc.write(control_assistant_reply)
        with open("logs/response.json", "r") as rc:
            gen_control_response = json.load(rc)

        short_term_memory.add_message("assistant", json.dumps(gen_control_response))
        final_control_response = ({"text": f"{gen_control_response["response"]}"})

        print(f"{assistant_name}: {final_control_response}")
        modeltts(final_control_response)

        
        key_word = gen_control_response.get("key", "")
        times_word = gen_control_response.get("times", "")
        write_key = gen_control_response.get("write", "")
        firsthkey_word = gen_control_response.get("firsthkey", "")
        sechkey_word = gen_control_response.get("sechkey", "")
        hotkey_word = gen_control_response.get("hotkey", "")
        
        keyboard_control(
            key= key_word,
            times= times_word,
            write= write_key,
            firsthkey= firsthkey_word,
            sechkey= sechkey_word,
            hotkey= hotkey_word
        )
        
        if gen_control_response["control_action"] == "True":
            continue
        else:
            break

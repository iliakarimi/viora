import os
import json
from openai import OpenAI
from speech.tts import modeltts
from get_api_key import get_openai_key
from memory.short_term_memory import ShortTermMemory
from internet_search import  needs_internet_check, search_online
from action import ComputerAnalyze, keyboard_control

client = OpenAI(
    api_key=get_openai_key()
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

system_texts = [
    f"You are {assistant_name}, a helpful assistant for {user_name}. You are an agent — please keep going until the user's query is completely resolved before ending your turn. Only yield back when you're sure the task is complete.",
    f"Your personality: {assistant_goal}.",
    f"Refer to the user as '{user_name}' if needed.",
    f"If you need details about Ilia, use: {about_user}.",
    f"You have short-term memory: {short_term_memory}.",
    "You can search the Internet when needed.",
    f"Respond {response_form}, strictly following this structure: {response_structure}.",
    "Respond only with a single JSON object, valid according to RFC 8259.",
    "Use only double quotes for all keys and string values.",
    "Do not include any single quotes, markdown, or any extra text outside the JSON.",
    "Never wrap responses in ```json or any kind of code block. Return plain raw JSON only.",
    "If you are not sure about file contents or code structure, use your tools to inspect files — do NOT guess.",
    f"{screen_vision}",
    f"{computer_control}",
    f"{action_scheduling}",
    f"{action_definitions}"
]

for text in system_texts:
    short_term_memory.add_message("system", text)

os.system("cls")

while True:
    # audio_path = record_until_silence()
    # user_input = transcribe_audio(audio_path)
    user_input = str(input("user: "))
    # print(f"{user_name}: {user_input}")

    short_term_memory.add_message("user", user_input)
    internet_check = needs_internet_check(user_input)

    if internet_check == "YES":
        online_assistant_reply = search_online(user_input)
        print(f"{assistant_name}: {online_assistant_reply}")
        modeltts(online_assistant_reply)
        short_term_memory.add_message("assistant", online_assistant_reply)
    elif internet_check == "NO":
        response = client.responses.create(
        model="gpt-4.1-mini",
        input=short_term_memory.get_messages()
        )

        assistant_reply = response.output_text

        with open("logs/response.json", "w") as wr:
            wr.write(assistant_reply)
        with open("logs/response.json", "r") as rr:
            response_data = json.load(rr)

        final_response = {"text": f"{response_data["response"]}"}
        modeltts(final_response)
        print(f"{assistant_name}: {final_response}")

        if response_data["control_action"] == "True":
            key_word = response_data.get("key", "")
            times_word = response_data.get("times", "")
            write_key = response_data.get("write", "")
            firsthkey_word = response_data.get("firsthkey", "")
            sechkey_word = response_data.get("sechkey", "")
            hotkey_word = response_data.get("hotkey", "")

            ComputerAnalyze.screen_picture()
            ComputerAnalyze.screen_analyze()
            with open('logs/analyze_screen.txt', 'r') as cr:
                analyze_data = cr.read()
            short_term_memory.add_message("assistant", analyze_data)
            
            control_response_gen = client.responses.create(
            model="gpt-4.1-mini",
            input=short_term_memory.get_messages()
            )
            control_response = control_response_gen.output_text
            with open("logs/control_response.json", "w") as wc:
                wc.write(control_response)
            with open("logs/control_response.json", "r") as rc:
                gen_control_response = json.load(rc)
            final_control_response = ({"text": f"{gen_control_response["response"]}"})
            modeltts(final_control_response)
            print(f"{assistant_name}: {final_control_response}")
            keyboard_control(
                key= key_word,
                times= times_word,
                write= write_key,
                firsthkey= firsthkey_word,
                sechkey= sechkey_word,
                hotkey= hotkey_word
            )
        else:
            continue

        # if response_data["code_action"] == "True":
        #     try:
        #         code_to_run = response_data.get("code", "")
        #         exec(code_to_run, globals(), locals())
        #     except Exception as e:
        #         e_error = f'{e}'
        #         print(e_error)
        #         command_action = os.system(code_to_run)
        #         command_action
        #         if command_action != 0:
        #             print(f"os.system also failed with exit code {command_action}")
        # else:
        #     continue

        short_term_memory.add_message("assistant", json.dumps(assistant_reply))

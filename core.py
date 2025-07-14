import os
import json
import openai
from speech.tts import modeltts
from get_api_key import get_openai_key
from memory.short_term_memory import ShortTermMemory
from internet_search import  needs_internet_check, search_online
from action import ComputerAnalyze, keyboard_control

client = openai.OpenAI()

get_openai_key()

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


short_term_memory.add_message(
    "system",
    f"You are {assistant_name}, a helpful assistant for {user_name}.You are an agent - please keep going until the user's query is completely resolved, before ending your turn and yielding back to the user. Only terminate your turn when you are sure that the problem is solved."
    f"Your personality: {assistant_goal}."
    f"If you wanted to use the word 'there' to call the user, use {user_name}."
    f"If you want to know about Ilia, use {about_user}."
    f"You have short-term memory. You can remember details during this session (short-term memory){short_term_memory}."
    "You can search on the Internet."
    f"Respond {response_form} as instructed, following the {response_structure} for Respones structure.You can run Code and Command when 'code_action' == 'True' in Computer. for control the ilia's laptop you can use cmd command."
    "Respond **only** with a single JSON object, valid according to RFC 8259."
    "Use **only** double quotes for all keys and string values."
    "Do **not** include any single quotes or text outside the JSON. "
    "Never format your output using markdown code blocks like ```json or ```text. If you need to return structured data such as JSON, just return it as raw plain text without wrapping it in any code block or backticks."
    "If you are not sure about file content or codebase structure pertaining to the user's request, use your tools to read files and gather the relevant information: do NOT guess or make up an answer."
    "{screen_vision}. say wait so you can get screen detail in next response.Be sure make 'control_action == True' for first reponse so you can get screen detail for next response."
)


while True:
    # audio_path = record_until_silence()
    # user_input = transcribe_audio(audio_path)
    user_input = str(input("User: "))
    print(f"{user_name}: {user_input}")

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
            with open('logs/analyze_screen.json', 'r') as cr:
                analyze_data = json.load(cr)
            short_term_memory.add_message("assistant", json.dumps(analyze_data))
            
            control_response_gen = client.responses.create(
            model="gpt-4.1-mini",
            input=short_term_memory.get_messages()
            )
            control_response = control_response_gen.output_text
            final_control_response = {"text": f"{control_response["response"]}"}
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

        if response_data["code_action"] == "True":
            try:
                code_to_run = response_data.get("code", "")
                exec(code_to_run, globals(), locals())
            except Exception as e:
                e_error = f'{e}'
                print(e_error)
                command_action = os.system(code_to_run)
                command_action
                if command_action != 0:
                    print(f"os.system also failed with exit code {command_action}")
        else:
            continue

        short_term_memory.add_message("assistant", json.dumps(assistant_reply))

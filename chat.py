import openai
import json
import os
from dotenv import load_dotenv
from memory_setting.short_term_memory.short_term_memory import ShortTermMemory
# from stt.stt_setting import record_until_silence, transcribe_audio
# from tts.tts_setting import modeltts
# from internet_search import  needs_internet_check, search_online

load_dotenv()

client = openai.OpenAI()

openai.api_key = os.getenv("OPENAI_API_KEY")

with open('memory/fixed_memory.json', 'r') as file:
    assistant_data = json.load(file)

short_term_memory = ShortTermMemory()

assistant_name = assistant_data["name"]
user_name = assistant_data["user_name"]
about_user = assistant_data["about_user"]
assistant_goal = assistant_data["personality"]
response_form = assistant_data["response_form"]
response_structure = assistant_data["response_structure"]

short_term_memory.add_message(
    "system",
    f"You are {assistant_name}, a helpful assistant for {user_name}."
    f"Your personality: {assistant_goal}."
    f"If you wanted to use the word 'there' to call the user, use {user_name}."
    f"If you want to know about Ilia, use {about_user}."
    f"You have short-term memory. You can remember details during this session (short-term memory){short_term_memory}."
    "You only communicate with Ilia."
    "Ilia is your developer."
    "When i talk to you with persian language, you talk and type for me with 'finglish typing' for example(for'سلام' type 'salam')."
    "You can search on the Internet."
    f"Respond {response_form} as instructed, following the {response_structure} for Respones structure.You can run Code and Command when 'code_action' == 'True' in Computer. for control the ilia's laptop you can use cmd command."
)


while True:
    # audio_path = record_until_silence()
    # user_input = transcribe_audio(audio_path)
    user_input = str(input("User: "))
    print(f"{user_name}: {user_input}")

    short_term_memory.add_message("user", user_input)
    # internet_check = needs_internet_check(user_input)

    # if internet_check == "YES":
    #     online_assistant_reply = search_online(user_input)
    #     print(f"{assistant_name}: {online_assistant_reply}")
    #     # modeltts(online_assistant_reply)
    #     short_term_memory.add_message("assistant", online_assistant_reply)
        
    # elif internet_check == "NO":
    response = client.responses.create(
    model="gpt-4.1-mini",
    input=short_term_memory.get_messages()
    )

    assistant_reply = response.output_text

    with open("response.json", "w") as wr:
        wr.write(assistant_reply)
    with open("response.json", "r") as rr:
        response_data = json.load(rr)
        
    final_response = response_data["response"]
        
    print(f"{assistant_name}: {final_response}")
        
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

        # modeltts(final_response)
    short_term_memory.add_message("assistant", assistant_reply)

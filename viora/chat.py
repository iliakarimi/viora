import json
from speech.tts import main_tts
from gpt import openai_response
from tools.action import ComputerControl as cc
from memory.short_term_memory import ShortTermMemory


short_memory = ShortTermMemory()

get_user_memory = short_memory.get_user_messages()
get_agent_memory = short_memory.get_agent_messages()


def generate_res():
    res = openai_response(
        input=get_user_memory,
        memory=get_agent_memory
    )


    with open("logs/response.json", "w") as wr:
        wr.write(res.output_text)



def run_agent():
    while True:

        user_input = input("You: ")


        short_memory.add_user_message(user_input)

        generate_res()

        with open("logs/response.json", "r") as rr:
            response_data = json.load(rr)

        final_response = f"{json.dumps(response_data["response"])}"
        short_memory.add_agent_message(json.dumps(response_data))
        
        print(f"Viora: {final_response}")
        main_tts(final_response)


        control_action = response_data["control_action"]

        while control_action == "True" or "true":

            generate_res()


            short_memory.add_agent_message(json.dumps(response_data))
            final_control_response = ({"text": f"{response_data["response"]}"})

            print(f"Viora: {final_control_response}")
            main_tts(final_control_response)
            
            key_word = response_data.get("key", "")
            times_word = response_data.get("times", "")
            write_key = response_data.get("write", "")
            firsthkey_word = response_data.get("firsthkey", "")
            sechkey_word = response_data.get("sechkey", "")
            hotkey_word = response_data.get("hotkey", "")
            movex_mouse = response_data.get("movex", "")
            movey_mouse = response_data.get("movey", "")
            click_button_mouse = response_data.get("click_button", "")
            click_times_mouse = response_data.get("click_times", "")
            scroll_mouse = response_data.get("scroll", "")

            cc.keyboard_control(
                key= key_word,
                times= times_word,
                write= write_key,
                firsthkey= firsthkey_word,
                sechkey= sechkey_word,
                hotkey= hotkey_word
            )
            cc.mouse_control(
                movex=movex_mouse,
                movey=movey_mouse,
                click_button=click_button_mouse,
                click_times=click_times_mouse,
                scroll=scroll_mouse
            )
            
            if control_action == "True" or "true":
                continue


def main():
    # try:
    #     run_agent()
    # except Exception as e:
    #     print(e)
    run_agent()

if __name__ == "__main__":
    print("════════════════════════════════════════")
    print("        |  Viora Alpha 0.1  |           ")
    print("════════════════════════════════════════")
    print("        For Quit press Ctrl+C         \n")
    main()

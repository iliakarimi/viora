import json
from speech.tts import main_tts
from gpt import openai_response
from utils.clear import cleart
from tools.action import ComputerControl as cc



def run_agent():
    while True:

        user_input = input("You: ")

        res = openai_response(
            input=user_input
        )

        res
        

        with open("logs/response.json", "r") as rr:
            response_data = json.load(rr)

        final_response = f"{json.dumps(response_data["response"])}"
        
        print(f"Viora: {final_response}")
        main_tts(final_response)

        action = False
        if response_data["control_action"] == "True":
            action = True
            while action:

                action_response = openai_response()
                
                action_response


                print(f"Viora: {final_response}")
                main_tts(final_response)
                
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
                    key_settingstimes= times_word,
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
        else:
            action = False



def main():
    try:
        run_agent()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    try:
        cleart()

        print("════════════════════════════════════════")
        print("        |  Viora Alpha 0.1  |           ")
        print("════════════════════════════════════════")
        print("        For Quit press Ctrl+C         \n")

        main()
    
    except KeyboardInterrupt:
        print("\nQuiting Viora.")
    
    except Exception as e:
        print("\nAn unexpected error occurred. Please try again. If the problem persists, please open issue issue on GitHub.")
        print(e)

import json
import openai
import base64
import pyautogui
from get_api_key import get_openai_key

client = openai.OpenAI()
get_openai_key()

with open("configs/user_setup.json", "r") as ur:
    user_setup = json.load(ur)
    test = list(user_setup.values())[0]

screen_size = test["screen_size"]

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


class ComputerAnalyze():
    def __init__(self):
        self.screen_picture
        self.screen_analyze
    def screen_picture():
        pyautogui.screenshot('logs/screenshot.png')
    def screen_analyze():
        image_f = "logs/screenshot.png"
        base64_image = encode_image(image_f)

        analyze_response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    { "type": "input_text", "text": "describe the image and tell what do you see exactly." "Do **not** include any single quotes or text outside the JSON." "Use **only** double quotes for all keys and string values." "Respond **only** with a single JSON object, valid according to RFC 8259." },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
        )
        with open("logs/analyze_screen.json", "w") as ws:
            ws.write(analyze_response.output_text)


class ComputerAction():
    def mouse_control(rightposition : int = None, leftposition : int= None, click : int= None, clickbutton : str= None, scroll : int= None):
        pyautogui.size(int(screen_size))
        pyautogui.moveTo(int(rightposition), int(leftposition))
        pyautogui.scroll(scroll)
        pyautogui.click(button= clickbutton, clicks=int(click))


    def keyboard_control(key):
        pyautogui.size(screen_size)
        pyautogui.typewrite()
        pyautogui.press([key], )
        pyautogui.hotkey()



ComputerAction.mouse_control()

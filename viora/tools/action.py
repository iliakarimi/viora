import os, sys
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

import json
import openai
import base64
import pyautogui
from time import sleep
from utils.get_api_key import get_openai_key





client = openai.OpenAI(
    api_key = get_openai_key()
    )




with open("configs/models.json", "r") as modl:
    model_conf = json.load(modl)

model_name = model_conf["GPT"]



def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
class ComputerAnalyze():
    
    def __init__(self):
        pass
    def screen_picture():
        pyautogui.screenshot('logs/snapshot.png')
    def screen_analyze():
        image_f = "logs/snapshot.png"
        base64_image = encode_image(image_f)

        analyze_response = client.responses.create(
        model=model_name,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Analyze the image and describe exactly what is visible. For every element (text, buttons, icons, images, etc.), provide its precise spatial location on the screen, using relative positions (top-left, center, bottom-right) or coordinates if possible. Do not speculate about function, intent, or aesthetics—only describe the visual structure clearly enough for programmatic interaction using PyAutoGUI."
                            "You are an image analysis assistant. "
                            "Your task is to describe the given image in extreme detail, focusing on spatial relationships, "
                            "object positions, and UI elements that could be interacted with. "
                            "Output must be precise enough for programmatic control (e.g. using pyautogui). "
                            "Do not describe feelings, colors, or aesthetic details unless relevant to object identification."
                            "Use coordinates and relative position terms like 'top-left', 'center-right', 'bottom-middle', etc. "
                            "Return data in structured JSON format for parsing."
                        )
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
        )
        with open("logs/analyze_screen.txt", "w") as ws:
            ws.write(analyze_response.output_text)




class computer_control():
    def __init__(self, key= '', times=1, write= '', firsthkey= '', sechkey= '', hotkey= ''):
        self.key = key
        self.times = times
        self.write = write
        self.firsthkey = firsthkey
        self.sechkey = sechkey
        self.hotkey = hotkey

    def keyboard_control(self, key, times, write, firsthkey, sechkey, hotkey):
        if write:
            pyautogui.write(write)
            return
        if key:
            pyautogui.press(key, presses=int(times) if times else 1)
            return
        if hotkey:
            keys = hotkey.split('+')
            pyautogui.hotkey(*keys)
            return
        if firsthkey and sechkey:
            with pyautogui.hold(firsthkey):
                pyautogui.press(sechkey)
            return

    def mouse_control(self, left_click, right_click, times):
        # pyautogui.leftClick()
        
        # right_click = pyautogui.click()
        # for rc in right_click:
        #     sleep(times)
        #     return rc 
        pass
import os, sys
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

import json
import openai
import pyautogui
from utils.encode import encode_image


client = openai.OpenAI(
    api_key= None
    )


with open("configs/models.json", "r") as modl:
    model_conf = json.load(modl)

model_name = model_conf["GPT"]


class ComputerAnalyze():
    """
    Take an ScreenShot from the Screen
    """

    @classmethod
    def screen_picture(cls):
        pyautogui.screenshot('snapshot.png')

    @classmethod
    def screen_analyze(cls):
        image_f = "logs/snapshot.png"
        base64_image = encode_image(image_f)

        analyze_response = client.responses.create(
        model=model_name,
        input=[
            {
                "role": "developer",
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




class ComputerControl():
    """
    Control Computer
    """

    def __init__(self, key= '', times=1, write= '', firsthkey= '', sechkey= '', hotkey= '', left_click=None, right_click=None, wait_time=None, scroll=None): #The 'None' for mouse Parameter's temperary.
        self.key = key
        self.times = times
        self.write = write
        self.firsthkey = firsthkey
        self.sechkey = sechkey
        self.hotkey = hotkey
        self.left_click = left_click
        self.right_click = right_click
        self.wait_time = wait_time
        self.scroll = scroll

    def keyboard_control(self, key=None, times=None, write=None, firsthkey=None, sechkey=None, hotkey=None):

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

    def mouse_control(self, left_click, right_click, wait_time, scroll):
        # pyautogui.leftClick()
        
        # right_click = pyautogui.click(right_click)
        # for rc in right_click:
        #     sleep(wait_time)
        #     return rc 
        
        # m_scrool = pyautogui.scroll(scroll)
        pass

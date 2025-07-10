import openai
import base64
import pyautogui
from get_api_key import get_openai_key

client = openai.OpenAI()
get_openai_key()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


class ComputerControl():
    def __init__(self, mouse, keyboard):
        self.screen_picture
        self.screen_analyze
        self.mouse_control = mouse
        self.keyboard_control = keyboard
    def screen_picture():
        pass
    def screen_analyze():
        image_f = "logs/s_image.png"
        base64_image = encode_image(image_f)

        response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    { "type": "input_text", "text": "describe the image and tell what do you see exactly." },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
        )
        print(response.output_text)
    def mouse_control():
        pass
    def keyboard_control():
        pass

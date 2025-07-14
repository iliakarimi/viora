import openai
import base64
import pyautogui
from get_api_key import get_openai_key

client = openai.OpenAI()
get_openai_key()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


class ComputerAnalyze():
    def screen_picture():
        pyautogui.screenshot('logs/snapshot.png')
    def screen_analyze():
        image_f = "logs/snapshot.png"
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



def keyboard_control(key= '', times=1, write= '', firsthkey= '', sechkey= '', hotkey= ''):
    pyautogui.press(key, times)
    pyautogui.write(write)

    pyautogui.hotkey(hotkey)
    with pyautogui.hold(firsthkey):
        pyautogui.press(sechkey)

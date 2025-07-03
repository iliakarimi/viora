import base64
import openai

client = openai.OpenAI()

openai.api_key = "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"

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to your image
image_path = "mmeeeom.png"

# Getting the Base64 string
base64_image = encode_image(image_path)


response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": "what's in this image? can you explane copletely of the image like icons, positions and like this?" },
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        }
    ],
)

print(response.output_text)
import requests
import base64

from config import OPENROUTER_API_KEY

VISION_MODEL = "nvidia/nemotron-nano-12b-v2-vl:free"

def analyze_image(image_bytes):

    image_base64 = base64.b64encode(
        image_bytes
    ).decode("utf-8")


    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": VISION_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": 
                            "Analyze this image and create a detailed AI image generation prompt. Describe subject, appearance, colors, lighting, camera, style and quality."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ]
        },
        timeout=60
    )


try:
    data = response.json()
except Exception as e:
    return f"Vision API Error: {e}\n{response.text}"


if "choices" in data:
    return data["choices"][0]["message"]["content"]

return str(data)

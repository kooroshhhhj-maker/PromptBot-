import requests
import base64

from config import OPENROUTER_API_KEY

VISION_MODEL = "nvidia/nemotron-nano-12b-v2-vl:free"


def analyze_image(image_bytes):
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    print("VISION REQUEST START")

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": VISION_MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analyze this image and describe what is happening.",
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                },
                            },
                        ],
                    }
                ],
            },
            timeout=60,
        )

        print("VISION REQUEST FINISHED")

        data = response.json()
        print(data)

        if "choices" in data:
            return data["choices"][0]["message"]["content"]

        return str(data)

    except Exception as e:
        print("VISION ERROR:", e)
        return f"Vision API Error: {e}"


import requests
import base64
from PIL import Image
from io import BytesIO
from ocr import extract_text

from config import OPENROUTER_API_KEY

VISION_MODEL = "nvidia/nemotron-nano-12b-v2-vl:free"


def analyze_image(image_bytes):

    image = Image.open(BytesIO(image_bytes))
    ocr_text = extract_text(image_bytes)

    print("OCR TEXT:")
    print(ocr_text)

    image.thumbnail((768, 768))

    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=85)

    image_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

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
                                "text": f"""Analyze this image carefully.

                                 OCR text found:
                                 ----------------
                                 {ocr_text}

                                 Use both the image and the OCR text to understand the image accurately.
                                """,
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
            timeout=30
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


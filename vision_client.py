import requests
import base64
from PIL import Image
from io import BytesIO

from ocr import extract_text
from config import OPENROUTER_API_KEY
from image_analysis_prompts import get_analysis_prompt


VISION_MODELS = [
    "nvidia/nemotron-nano-12b-v2-vl:free",
    "qwen/qwen2.5-vl-32b-instruct:free"
]


def analyze_image(image_bytes, analysis_type="general"):

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


    for model in VISION_MODELS:

        print("VISION MODEL TRY:", model)

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",

                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },

                json={
                    "model": model,

                    "messages": [
                        {
                            "role": "user",

                            "content": [
                                {
                                    "type": "text",

                                    "text": f"""
{get_analysis_prompt(analysis_type)}

OCR text:
----------------
{ocr_text}

Analyze the image carefully.

After analysis, create a professional AI image generation prompt based on this image.
"""
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

                timeout=40
            )


            data = response.json()

            print(data)


            if "choices" in data:

                print(f"Model {model} worked.")

                return data["choices"][0]["message"]["content"]


            print(f"Model {model} failed:", data)


        except Exception as e:

            print("VISION ERROR:", e)



    return "❌ All vision models failed."

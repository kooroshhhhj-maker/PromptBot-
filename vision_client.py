import requests
import base64
from PIL import Image
from io import BytesIO

from ocr import extract_text
from image_analysis_prompts import get_analysis_prompt
from config import CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID


MODEL = "@cf/llava-hf/llava-1.5-7b-hf"


def analyze_image(image_bytes, analysis_type="general"):

    try:
        print("CLOUDFLARE VISION START")

        image = Image.open(BytesIO(image_bytes))

        ocr_text = extract_text(image_bytes)

        print("OCR TEXT:")
        print(ocr_text)

        image.thumbnail((768, 768))

        buffer = BytesIO()
        image.save(buffer, format="JPEG", quality=85)

        img_base64 = base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")


        url = (
            f"https://api.cloudflare.com/client/v4/accounts/"
            f"{CLOUDFLARE_ACCOUNT_ID}/ai/run/{MODEL}"
        )


        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "image": img_base64,
                "prompt": f"""
{get_analysis_prompt(analysis_type)}

OCR TEXT:
{ocr_text}

Analyze this image carefully.
Create a detailed description.
Also create an AI image generation prompt.
"""
            },
            timeout=120
        )


        print("CLOUDFLARE RESPONSE:", response.status_code)


        data = response.json()

        print(data)


        if data.get("success"):

            return data["result"]["description"]


        return "❌ Cloudflare Vision failed:\n" + str(data)


    except Exception as e:

        print("VISION ERROR:", e)

        return "❌ Vision error:\n" + str(e)

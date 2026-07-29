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
        image = Image.open(BytesIO(image_bytes))

        # تبدیل به RGB برای جلوگیری از خطای decode
        if image.mode != "RGB":
            image = image.convert("RGB")

        # OCR
        ocr_text = extract_text(image_bytes)

        print("OCR TEXT:")
        print(ocr_text)


        # تغییر اندازه
        image.thumbnail((768, 768))


        # تبدیل دوباره به JPEG استاندارد
        buffer = BytesIO()

        image.save(
            buffer,
            format="JPEG",
            quality=85
        )

        buffer.seek(0)


        # Cloudflare نیاز به بایت تصویر دارد
        image_data = list(buffer.getvalue())


        url = (
            f"https://api.cloudflare.com/client/v4/accounts/"
            f"{CLOUDFLARE_ACCOUNT_ID}/ai/run/{MODEL}"
        )


        print("CLOUDFLARE VISION START")


        response = requests.post(

            url,

            headers={
                "Authorization":
                f"Bearer {CLOUDFLARE_API_TOKEN}",

                "Content-Type":
                "application/json"
            },


            json={

                "image": image_data,

                "prompt":
                f"""
{get_analysis_prompt(analysis_type)}

OCR TEXT:
{ocr_text}

Analyze this image.

Describe:
- objects
- people
- environment
- colors
- important details

Then create a professional AI image generation prompt based on this image.
"""
            },

            timeout=120
        )


        data = response.json()

        print(data)


        if data.get("success"):

            return data["result"].get(
                "description",
                str(data["result"])
            )


        return "❌ Cloudflare Vision failed:\n" + str(data)


    except Exception as e:

        return f"❌ Vision Exception: {e}"

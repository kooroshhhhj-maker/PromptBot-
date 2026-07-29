import requests
from config import HUGGING_FACE_API_KEY


API_URL = "https://router.huggingface.co/hf-inference/models/Salesforce/blip-image-captioning-base"


headers = {
    "Authorization": f"Bearer {HUGGING_FACE_API_KEY}",
    "Content-Type": "application/octet-stream"
}


def analyze_image_hf(image_bytes):

    response = requests.post(
        API_URL,
        headers=headers,
        data=image_bytes,
        timeout=120
    )

    try:
        return response.json()
    except Exception:
        return response.text

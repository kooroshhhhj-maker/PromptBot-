from io import BytesIO
import requests
import base64

from config import CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID


def generate_image(prompt):
    try:
        print("Sending to Cloudflare AI:", prompt)

        url = (
            f"https://api.cloudflare.com/client/v4/accounts/"
            f"{CLOUDFLARE_ACCOUNT_ID}/ai/run/"
            "@cf/black-forest-labs/flux-1-schnell"
        )

        headers = {
            "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            url,
            headers=headers,
            json={
                "prompt": prompt
            },
            timeout=120
        )

        print("STATUS:", response.status_code)

        if response.status_code == 200:
            data = response.json()

            img_base64 = data["result"]["image"]

            image_bytes = base64.b64decode(img_base64)

            image = BytesIO(image_bytes)
            image.name = "image.jpg"
            image.seek(0)

            return image

        print(response.text)

    except Exception as e:
        print("IMAGE ERROR:", e)

    return None


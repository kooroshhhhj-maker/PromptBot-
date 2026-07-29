import requests
import base64


def analyze_image(image_bytes, token, account_id):

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    image_data_uri = f"data:image/jpeg;base64,{image_base64}"

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{account_id}/ai/run/@cf/meta/llama-3.2-11b-vision-instruct"
    )

    payload = {
        "image": image_data_uri,
        "prompt": (
            "Analyze this image in detail. "
            "Describe objects, scene, and read any visible text."
        )
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=60
    )

    print("CLOUDFLARE STATUS:", response.status_code)
    print(response.text)

    if response.status_code != 200:
        return None

    data = response.json()

    if "result" in data:
        result = data["result"]

        if isinstance(result, dict):
            return result.get("response")

        return result

    return None

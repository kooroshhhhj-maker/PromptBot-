import requests

from config import CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID

url = (
    f"https://api.cloudflare.com/client/v4/accounts/"
    f"{CLOUDFLARE_ACCOUNT_ID}/ai/models/"
    f"@cf/runwayml/stable-diffusion-v1-5-img2img"
)

headers = {
    "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"
}

r = requests.get(url, headers=headers)

print(r.status_code)
print(r.text)

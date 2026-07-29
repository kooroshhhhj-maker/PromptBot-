import requests
from config import CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID

url = (
    f"https://api.cloudflare.com/client/v4/accounts/"
    f"{CLOUDFLARE_ACCOUNT_ID}/ai/run/@cf/meta/llama-3.2-11b-vision-instruct"
)

headers = {
    "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "prompt": "agree"
}

r = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=60
)

print(r.status_code)
print(r.text)


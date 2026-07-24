import requests
from config import OPENROUTER_API_KEY

url = "https://openrouter.ai/api/v1/models"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}"
}

response = requests.get(url, headers=headers)

data = response.json()

for model in data["data"]:
    pricing = model.get("pricing", {})

    if pricing.get("prompt") == "0" and pricing.get("completion") == "0":
        print(model["id"])

import requests
from config import OPENROUTER_API_KEY, MODEL


def ask_ai(messages):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": messages
            },
            timeout=60
        )

        data = response.json()

        if "choices" in data:
            return data["choices"][0]["message"]["content"]

        return str(data)

    except Exception as e:
        return f"AI Error: {e}"

import requests
from config import OPENROUTER_API_KEY

CHAT_MODEL = "meta-llama/llama-3.1-8b-instruct:free"


def ask_ai(messages):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": CHAT_MODEL,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2000
            },
            timeout=60
        )

        data = response.json()

        if "choices" in data:
            return data["choices"][0]["message"]["content"]

        return f"❌ OpenRouter Error:\n{data}"

    except Exception as e:
        return f"❌ AI Error: {e}"


def write_text(topic, style="professional"):
    messages = [
        {
            "role": "system",
            "content": f"You are a professional writer. Write in a {style} style."
        },
        {
            "role": "user",
            "content": topic
        }
    ]

    return ask_ai(messages)


def brainstorm_ideas(topic, count=5):
    messages = [
        {
            "role": "system",
            "content": "You are a creative brainstorming assistant."
        },
        {
            "role": "user",
            "content": f"Give me {count} creative ideas about: {topic}"
        }
    ]

    return ask_ai(messages)


def generate_prompt(topic, style="detailed"):
    messages = [
        {
            "role": "system",
            "content": "Create detailed AI image generation prompts."
        },
        {
            "role": "user",
            "content": f"Create an image prompt about {topic}. Style: {style}"
        }
    ]

    return ask_ai(messages)

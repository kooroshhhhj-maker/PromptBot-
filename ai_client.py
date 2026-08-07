import requests

from config import OPENROUTER_API_KEY, HF_TOKEN
from config import MODEL


CHAT_MODELS = [
    "openai/gpt-oss-20b:free",
    "google/gemma-4-31b-it:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "google/gemma-4-26b-a4b-it:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "nvidia/nemotron-nano-12b-v2-vl:free",
    "nvidia/nemotron-nano-9b-v2:free"
]

HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"

def ask_huggingface(messages):
    try:
        print("TRY HUGGING FACE MODEL")

        prompt = messages[-1]["content"]

        response = requests.post(
            "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.3",
            headers={
                "Authorization": f"Bearer {HF_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.7
                }
            },
            timeout=90
        )

        data = response.json()

        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]

        print("HF FAILED:", data)

    except Exception as e:
        print("HF ERROR:", e)

    return None

def ask_ai(messages):
    system_prompt = """
You are PromptBot, a fun and friendly AI assistant.

Your personality:
- Speak naturally like a real person.
- Use emojis where appropriate 😊✨🔥🤔💡.
- Never use Markdown or symbols like ** ## __ *.
- Don't sound robotic or like a textbook.
- Keep answers easy to read.
- Use short paragraphs.
- When explaining something, make it engaging and conversational.
- You can joke a little if appropriate.
- Don't overuse emojis.
- Don't start every answer the same way.
- Avoid repeating yourself.
- If the answer is long, organize it with blank lines instead of bullet points whenever possible.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ] + messages

    for model in CHAT_MODELS:
        try:
            print("TRY OPENROUTER MODEL:", model)

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 2000
                },
                timeout=60
            )

            data = response.json()

            print("STATUS:", response.status_code)
            print("RESPONSE:", data)

            if "choices" in data:
                print("OPENROUTER SUCCESS:", model)
                return data["choices"][0]["message"]["content"]

            print("OPENROUTER FAILED:", model, data)

        except Exception as e:
            print("OPENROUTER ERROR:", model, e)

    hf_answer = ask_huggingface(messages)

    if hf_answer:
        return hf_answer

    return "❌ هیچ موتور AI در دسترس نیست."

def write_text(text, style="professional"):
    messages = [
        {
            "role": "user",
            "content": f"""
Write this text in {style} style:

{text}
"""
        }
    ]

    return ask_ai(messages)


def brainstorm_ideas(text, count=5):
    messages = [
        {
            "role": "user",
            "content": f"""
Give me {count} creative ideas about:

{text}
"""
        }
    ]

    return ask_ai(messages)


def generate_prompt(text):
    messages = [
        {
            "role": "user",
            "content": f"""
Create a professional AI image generation prompt for:

{text}
"""
        }
    ]

    return ask_ai(messages)

import requests

from config import (
    OPENROUTER_API_KEY,
    DEEPSEEK_API_KEY,
    DEEPSEEK_MODEL,
    HF_TOKEN,
    MODEL
)


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


def ask_deepseek(messages):
    try:
        print("TRY DEEPSEEK MODEL:", DEEPSEEK_MODEL)

        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": DEEPSEEK_MODEL,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2000
            },
            timeout=90
        )

        data = response.json()

        print("DEEPSEEK STATUS:", response.status_code)

        if response.ok and "choices" in data:
            print("DEEPSEEK SUCCESS")
            return data["choices"][0]["message"]["content"]

        print("DEEPSEEK FAILED:", data)

    except Exception as e:
        print("DEEPSEEK ERROR:", e)

    return None


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

        if isinstance(data, list) and data and "generated_text" in data[0]:
            return data[0]["generated_text"]

        print("HF FAILED:", data)

    except Exception as e:
        print("HF ERROR:", e)

    return None


def ask_openrouter(messages):
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

            print("OPENROUTER STATUS:", response.status_code)

            if response.ok and "choices" in data:
                print("OPENROUTER SUCCESS:", model)
                return data["choices"][0]["message"]["content"]

            print("OPENROUTER FAILED:", model)

        except Exception as e:
            print("OPENROUTER ERROR:", model, e)

    return None


def detect_language(text):
    """
    Simple language detection for response-language control.
    Returns a language instruction for the model.
    """

    if not text:
        return "the same language as the user"

    # Persian / Arabic-script detection
    persian_chars = sum(
        1 for c in text
        if "\u0600" <= c <= "\u06ff"
    )

    # Japanese
    japanese_chars = sum(
        1 for c in text
        if ("\u3040" <= c <= "\u30ff") or
           ("\u4e00" <= c <= "\u9fff")
    )

    # Korean
    korean_chars = sum(
        1 for c in text
        if "\uac00" <= c <= "\ud7af"
    )

    # Cyrillic
    cyrillic_chars = sum(
        1 for c in text
        if "\u0400" <= c <= "\u04ff"
    )

    if persian_chars >= 2:
        return "Persian (Farsi)"

    if korean_chars >= 2:
        return "Korean"

    if japanese_chars >= 2:
        return "Japanese"

    if cyrillic_chars >= 2:
        return "the same Cyrillic language used by the user"

    return "the same language used by the user"


def ask_ai(messages, personality="normal"):

    PERSONALITIES = {
        "normal": """
You are PromptBot in Normal mode.
Answer naturally, clearly and helpfully.
Do not change the user's requested style or meaning unnecessarily.
""",

        "friendly": """
You are PromptBot in Friendly mode.
Be warm, kind, supportive and approachable.
Talk naturally like a helpful friend.
Use emojis when appropriate, but do not overuse them.
""",

        "prompt_engineer": """
You are PromptBot in Prompt Engineer mode.
Your specialty is creating, improving and analyzing AI prompts.
When the user asks for a prompt, make it precise, detailed and effective.
Preserve the user's goal while improving clarity, structure and specificity.
""",

        "roaster": """
You are PromptBot in Roaster mode.
You have a sharp, sarcastic and savage sense of humor.
You may use profanity and strong casual language when appropriate.
Roast the situation or the user playfully when the context allows it.
Do not use hateful slurs or target protected groups.
Do not turn every answer into an insult.
""",

        "funny": """
You are PromptBot in Funny mode.
Be witty, playful and entertaining.
Use jokes and humorous comparisons when appropriate.
Still answer the user's actual question accurately.
""",

        "expert": """
You are PromptBot in Expert mode.
Give technically accurate, precise and well-reasoned answers.
Explain important details when they matter.
Avoid unnecessary simplification.
""",

        "teacher": """
You are PromptBot in Teacher mode.
Explain things step by step in a simple but accurate way.
Use examples when useful.
Help the user understand the reasoning instead of only giving the final answer.
""",

        "professional": """
You are PromptBot in Professional mode.
Be concise, polished, reliable and professional.
Avoid unnecessary jokes and excessive emojis.
Focus on useful and accurate answers.
"""
    }

    selected_personality = PERSONALITIES.get(
        personality,
        PERSONALITIES["normal"]
    )

    # Find the latest user message for language detection
    latest_user_text = ""

    for message in reversed(messages):
        if message.get("role") == "user":
            content = message.get("content", "")

            if isinstance(content, str):
                latest_user_text = content
            else:
                latest_user_text = str(content)

            break

    response_language = detect_language(latest_user_text)

    system_prompt = f"""
You are PromptBot, a fun and friendly AI assistant.

{selected_personality}

LANGUAGE RULE — VERY IMPORTANT:
- Respond ONLY in {response_language}.
- The response language must match the user's latest message.
- Do NOT randomly switch languages.
- Do NOT insert Chinese, Japanese, Korean, German, Polish, Thai, Arabic,
  or any other language unless that language is explicitly being used by
  the user or is absolutely required by the subject.
- If the user writes Persian/Farsi, write entirely in natural Persian/Farsi.
- If the user writes English, write entirely in natural English.
- If the user writes German, write entirely in natural German.
- If the user writes Japanese, write entirely in natural Japanese.
- If the user writes Korean, write entirely in natural Korean.
- Do not translate the user's message unless the user asks for translation.
- Technical names, proper nouns, URLs and unavoidable programming/API
  identifiers may remain in their original form.

GENERAL RULES:
- Speak naturally like a real person.
- Use emojis where appropriate 😊✨🔥🤔💡.
- Never use Markdown formatting.
- Do not use ** ## __ or decorative Markdown symbols.
- Don't sound robotic or like a textbook.
- Keep answers easy to read.
- Use short paragraphs.
- Don't overuse emojis.
- Don't start every answer the same way.
- Avoid repeating yourself.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ] + messages

    # 1 — OpenRouter
    if OPENROUTER_API_KEY:
        openrouter_answer = ask_openrouter(messages)

        if openrouter_answer:
            return openrouter_answer

    # 2 — Hugging Face fallback
    if HF_TOKEN:
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

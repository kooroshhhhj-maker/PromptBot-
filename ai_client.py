import requests
from config import OPENROUTER_API_KEY

# Free AI models from OpenRouter
CHAT_MODEL = "google/gemma-3-27b-it:free"
ADVANCED_MODEL = "google/gemma-3-27b-it:free"

def ask_ai(messages):
    """Ask AI with chat history"""
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
        
        return str(data)
        
    except Exception as e:
        return f"❌ AI Error: {e}"

def write_text(topic, style="professional"):
    """Generate text content"""
    try:
        messages = [
            {
                "role": "system",
                "content": f"You are an expert content writer. Write in a {style} style. Be creative and engaging."
            },
            {
                "role": "user",
                "content": f"Write compelling content about: {topic}\n\nProvide well-structured, engaging text."
            }
        ]
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": ADVANCED_MODEL,
                "messages": messages,
                "temperature": 0.8,
                "max_tokens": 2500
            },
            timeout=60
        )
        
        data = response.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        
        return "❌ Failed to generate text"
        
    except Exception as e:
        return f"❌ Error: {e}"

def brainstorm_ideas(topic, count=5):
    """Generate creative ideas"""
    try:
        messages = [
            {
                "role": "system",
                "content": "You are a creative brainstorming expert. Generate innovative, unique, and actionable ideas."
            },
            {
                "role": "user",
                "content": f"Generate {count} creative ideas about: {topic}\n\nFormat: List each idea with a brief description."
            }
        ]
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": ADVANCED_MODEL,
                "messages": messages,
                "temperature": 0.9,
                "max_tokens": 2000
            },
            timeout=60
        )
        
        data = response.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        
        return "❌ Failed to brainstorm"
        
    except Exception as e:
        return f"❌ Error: {e}"

def generate_prompt(topic, style="detailed"):
    """Generate AI image generation prompt"""
    try:
        messages = [
            {
                "role": "system",
                "content": "You are an expert at creating detailed, vivid AI image generation prompts. Your prompts should be specific, creative, and produce high-quality images."
            },
            {
                "role": "user",
                "content": f"""Create a professional AI image generation prompt for: {topic}

Style: {style}

Include:
- Subject description
- Visual style
- Lighting and mood
- Camera perspective
- Quality and detail level
- Color palette

Format as a single compelling prompt (1-2 sentences)."""
            }
        ]
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": ADVANCED_MODEL,
                "messages": messages,
                "temperature": 0.8,
                "max_tokens": 300
            },
            timeout=60
        )
        
        data = response.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        
        return "❌ Failed to generate prompt"
        
    except Exception as e:
        return f"❌ Error: {e}"

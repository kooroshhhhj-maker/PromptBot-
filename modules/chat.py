def analyze_chat(ocr_text):
    return f"""
Analyze this chat screenshot.

Tasks:
- Summarize the conversation.
- Identify the main topic.
- Explain the tone and emotions.
- Suggest a suitable reply if needed.

Chat text:
{ocr_text}
"""


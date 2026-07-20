def generate_prompt(mode, text):
    if mode == "image_prompt":
        return f"""
Create a detailed image generation prompt.

User request:
{text}

Include:
- subject
- environment
- lighting
- camera angle
- style
- high quality details
"""

    elif mode == "writing":
        return f"""
Help the user write a professional and creative text.

User request:
{text}
"""

    elif mode == "ideas":
        return f"""
Generate creative ideas about this topic:

{text}
"""

    else:
        return text


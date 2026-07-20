def clean_prompt(text):

    text = text.replace("Subject:", "")
    text = text.replace("Appearance:", "")
    text = text.replace("Lighting:", "")
    text = text.replace("Camera:", "")
    text = text.replace("Style:", "")
    text = text.replace("Quality:", "")

    text = text.replace("\n", ", ")

    prompt = (
        "masterpiece, best quality, ultra detailed, "
        "8k, photorealistic, "
        + text
    )

    return prompt


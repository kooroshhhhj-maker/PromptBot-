import re


def detect_image_type(ocr_text: str):

    text = ocr_text.lower()

    if len(text) < 5:
        return {
            "type": "photo",
            "instruction": "Describe this image in detail."
        }

    if any(word in text for word in [
        "invoice",
        "total",
        "price",
        "amount",
        "receipt",
        "rial",
        "toman",
        "ریال",
        "تومان"
    ]):
        return {
            "type": "receipt",
            "instruction": "Extract all prices, products and totals."
        }

    if any(word in text for word in [
        "reply",
        "seen",
        "typing",
        "online"
    ]):
        return {
            "type": "chat",
            "instruction": "Summarize this conversation."
        }

    if len(text) > 300:
        return {
            "type": "document",
            "instruction": "Summarize and analyze this document."
        }

    return {
        "type": "mixed",
        "instruction": "Analyze everything visible in this image."
    }

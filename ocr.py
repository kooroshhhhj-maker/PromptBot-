import pytesseract
from PIL import Image
from io import BytesIO


def extract_text(image_bytes):
    try:
        image = Image.open(BytesIO(image_bytes))

        text = pytesseract.image_to_string(
            image,
            lang="fas+eng"
        )

        return text.strip()

    except Exception as e:
        print("OCR ERROR:", e)
        return ""


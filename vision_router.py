from modules.meme import analyze_meme
from modules.chat import analyze_chat
from modules.receipt import analyze_receipt
from modules.book import analyze_book
from modules.laboratory import analyze_laboratory
from modules.document import analyze_document
from modules.chart import analyze_chart
from modules.product import analyze_product
from modules.formula import analyze_formula
from modules.prescription import analyze_prescription
from modules.microscope import analyze_microscope


def route_image(image_type, ocr_text):

    if image_type == "meme":
        return analyze_meme(ocr_text)

    elif image_type == "chat":
        return analyze_chat(ocr_text)

    elif image_type == "receipt":
        return analyze_receipt(ocr_text)

    elif image_type == "book":
        return analyze_book(ocr_text)

    elif image_type == "laboratory":
        return analyze_laboratory(ocr_text)

    elif image_type == "document":
        return analyze_document(ocr_text)

    elif image_type == "chart":
        return analyze_chart(ocr_text)

    elif image_type == "product":
        return analyze_product(ocr_text)

    elif image_type == "formula":
        return analyze_formula(ocr_text)

    elif image_type == "prescription":
        return analyze_prescription(ocr_text)

    elif image_type == "microscope":
        return analyze_microscope(ocr_text)

    else:
        return "I could not determine the image type."


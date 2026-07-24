def analyze_product(ocr_text):
    return f"""
Analyze this product image.

Tasks:
- Identify the product if possible.
- Extract visible brand and model.
- Describe main features.
- Explain possible usage.
- Identify specifications from labels.
- Compare with similar products if requested.
- Mention uncertainty if the identification is not clear.

Product information:
{ocr_text}
"""

